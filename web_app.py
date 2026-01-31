import cv2
import time
from flask import Flask, render_template, Response, request, jsonify
# 导入自己写的模块
from src.pose_module import pose_detector
from src.squat_logic import squat_logic
from src.pushup_logic import pushup_logic
from src.counter_logic import CounterLogic

app = Flask(__name__)

# --- 全局变量初始化 ---
moniter = pose_detector(detection_con=0.7, track_con=0.7)
squat_tool = squat_logic()
push_tool = pushup_logic()
jump_tool = CounterLogic(image_height=720)

# 默认模式为跳绳
current_mode = "Jump"

# --- 在函数外部初始化摄像头，确保全局只有一个实例 ---
video_cap = cv2.VideoCapture(0)


def get_video_stream():
    p_time = 0
    # 声明使用外部的全局变量
    global video_cap

    while True:
        ret, frame = video_cap.read()
        if not ret:
            # 如果读取失败，尝试重新开启摄像头
            video_cap.release()
            video_cap = cv2.VideoCapture(0)
            time.sleep(0.5)
            continue

        # 图像预处理
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (1080, 720))

        # 调用MediaPipe识别骨骼点
        frame = moniter.find_pose(frame)
        landmarks = moniter.get_landmarks(frame)

        # 核心逻辑判断
        if len(landmarks) > 0:
            if current_mode == "Jump":
                count, is_paused, msg = jump_tool.update(landmarks)
                show_color = (0, 165, 255)  # 橘黄色
            elif current_mode == "Squat":
                count, msg = squat_tool.do_squat(moniter, frame)
                show_color = (255, 0, 0)  # 蓝色
            elif current_mode == "Pushup":
                count, msg = push_tool.do_push(moniter, frame)
                show_color = (0, 255, 0)  # 绿色
            else:
                count, msg = 0, "Unknown Mode"
                show_color = (255, 255, 255)

            # UI绘制
            cv2.putText(frame, f"Mode: {current_mode}", (50, 60),
                        cv2.FONT_HERSHEY_DUPLEX, 1, show_color, 2)
            cv2.putText(frame, f"Count: {count}", (50, 130),
                        cv2.FONT_HERSHEY_DUPLEX, 2, show_color, 4)
            cv2.putText(frame, f"Feedback: {msg}", (50, 200),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

        # 计算FPS
        c_time = time.time()
        fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
        p_time = c_time
        cv2.putText(frame, f"FPS: {int(fps)}", (950, 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        # 编码并推流
        ret, jpeg_buffer = cv2.imencode('.jpg', frame)
        final_frame = jpeg_buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + final_frame + b'\r\n')


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/video_feed')
def video_display():
    return Response(get_video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_stats')
def get_stats():
    # 根据当前模式动态获取数据
    if current_mode == "Jump":
        return jsonify({
            "mode": "跳绳模式",
            "count": jump_tool.jump_count,
            "status": "Jump!" if jump_tool.state == 'air' else "Steady"
        })
    elif current_mode == "Squat":
        return jsonify({
            "mode": "深蹲模式",
            "count": squat_tool.count,
            "status": squat_tool.feedback
        })
    elif current_mode == "Pushup":
        return jsonify({
            "mode": "俯卧撑模式",
            "count": push_tool.count,
            "status": push_tool.feedback
        })
    return jsonify({"mode": "等待中", "count": 0, "status": "Ready"})


@app.route('/change_mode')
def change_mode():
    global current_mode
    m = request.args.get('m')
    # 切换模式时调用reset避免计数重叠
    if m == '1':
        current_mode = "Squat"
        squat_tool.reset()
    elif m == '2':
        current_mode = "Pushup"
        push_tool.reset()
    elif m == '3':
        current_mode = "Jump"
        jump_tool.reset()

    print(f"模式已切换为：{current_mode}")
    return "OK"


import os
import signal


@app.route('/shutdown', methods=['POST'])
def shutdown():
    print("正在释放摄像头并关闭系统...")
    global video_cap
    if video_cap.isOpened():
        video_cap.release()  # 确保释放硬件占用

    # 延迟一小会儿，确保前端能收到 Response
    import threading
    def kill_later():
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGINT)

    threading.Thread(target=kill_later).start()
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
