import cv2
import time
import os

from src.pose_module import pose_detector
from src.squat_logic import squat_logic
from src.pushup_logic import pushup_logic


def main():
    # 初始化摄像头
    cap = cv2.VideoCapture(0)

    # 实例化算法类
    detector = pose_detector()
    squat_tool = squat_logic()
    pushup_tool = pushup_logic()

    # 设置初始模式和时间
    current_mode = "Squat"
    p_time = 0

    print("本地调试版已启动！")
    print("操作说明：按 'S' 键切换深蹲，按 'P' 键切换俯卧撑，按 'Q' 键退出。")

    while True:
        success, img = cap.read()
        if not success:
            print("错误：无法获取摄像头画面")
            break

        # 画面预处理：镜像翻转并调整大小
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (1080, 720))

        # 运行MediaPipe
        img = detector.find_pose(img)
        lm_list = detector.get_landmarks(img)

        # 只有看到人才执行
        if len(lm_list) != 0:
            if current_mode == "Squat":
                # 执行深蹲算法
                count, feedback = squat_tool.do_squat(detector, img)
                color = (255, 0, 0)  # 蓝色
            else:
                # 执行俯卧撑算法
                count, feedback = pushup_tool.do_push(detector, img)
                color = (0, 255, 0)  # 绿色

            # 把结果直接画在窗口上
            cv2.putText(img, f"Mode: {current_mode}", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(img, f"Count: {count}", (40, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)
            cv2.putText(img, f"Feedback: {feedback}", (40, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # 显示 FPS
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        cv2.putText(img, f"FPS: {int(fps)}", (900, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # 刷新画面
        cv2.imshow("Local Debugging Window", img)

        # 对应按键切换模式
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or key & 0xFF == ord('Q'):
            break
        elif key & 0xFF == ord('s') or key & 0xFF == ord('S'):
            current_mode = "Squat"
        elif key & 0xFF == ord('p') or key & 0xFF == ord('P'):
            current_mode = "Pushup"

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()