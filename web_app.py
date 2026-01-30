import cv2
import time
from flask import Flask, render_template, Response, request
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


def get_video_stream():
    # 获取摄像头画面并处理
    video_cap = cv2.VideoCapture(0)
    p_time = 0

    while True:
        ret, frame = video_cap.read()
        if not ret:
            print("摄像头读取失败了！")
            break

        # 图像预处理
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (1080, 720))

        # 调用MediaPipe识别骨骼点
        frame = moniter.find_pose(frame)
        landmarks = moniter.get_landmarks(frame)

        # 核心逻辑判断
        if len(landmarks) > 0:
            # 模式判断：改成默认先判断跳绳
            if current_mode == "Jump":
                # 调用跳绳逻辑
                count, is_paused, msg = jump_tool.update(landmarks)
                show_color = (0, 165, 255)  # 橘黄色
            elif current_mode == "Squat":
                # 调用深蹲逻辑
                count, msg = squat_tool.do_squat(moniter, frame)
                show_color = (255, 0, 0)  # 蓝色
            elif current_mode == "Pushup":
                # 调用俯卧撑逻辑
                count, msg = push_tool.do_push(moniter, frame)
                show_color = (0, 255, 0)  # 绿色
            else:
                count, msg = 0, "Unknown Mode"
                show_color = (255, 255, 255)

            # UI绘制
            cv2.putText(frame, "Mode: " + str(current_mode), (50, 60),
                        cv2.FONT_HERSHEY_DUPLEX, 1, show_color, 2)
            cv2.putText(frame, "Count: " + str(count), (50, 130),
                        cv2.FONT_HERSHEY_DUPLEX, 2, show_color, 4)
            cv2.putText(frame, "Feedback: " + str(msg), (50, 200),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

        # 计算FPS
        c_time = time.time()
        fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
        p_time = c_time
        cv2.putText(frame, "FPS: " + str(int(fps)), (950, 50),
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


@app.route('/change_mode')
def change_mode():
    global current_mode
    m = request.args.get('m')
    # 1深蹲，2俯卧撑，3跳绳
    if m == '1':
        current_mode = "Squat"
    elif m == '2':
        current_mode = "Pushup"
    elif m == '3':
        current_mode = "Jump"

    print(f"模式已切换为：{current_mode}")
    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)