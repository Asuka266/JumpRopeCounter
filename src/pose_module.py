import cv2
import mediapipe as mp
import math

# 在类内部定义常用索引
LEFT_HIP = 23
RIGHT_HIP = 24
LEFT_ANKLE = 27
RIGHT_ANKLE = 28

class PoseDetector:
    def __init__(self, detection_con=0.5, track_con=0.5):
        # 1. 初始化 MediaPipe 核心模型
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=detection_con,
                                      min_tracking_confidence=track_con)

    def find_pose(self, img, draw=True):
        """给成员 C 用：在画面上画出人体骨架"""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)
        if self.results.pose_landmarks and draw:
            self.mp_draw.draw_landmarks(img, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return img

    def get_landmarks(self, img):
        """给成员 B 用：提取 33 个关键点的像素坐标"""
        self.lm_list = []
        if self.results and self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # 将 0-1 的相对比例换算成实际像素坐标
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])
        return self.lm_list

    def find_angle(self, img, p1, p2, p3, draw=True):
        """含金量功能：计算身体部位角度（如膝盖弯曲度）"""
        if len(self.lm_list) != 0:
            # 获取三个点的坐标
            x1, y1 = self.lm_list[p1][1:]
            x2, y2 = self.lm_list[p2][1:]
            x3, y3 = self.lm_list[p3][1:]

            # 计算角度
            angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                 math.atan2(y1 - y2, x1 - x2))
            if angle < 0: angle += 360
            if angle > 180: angle = 360 - angle

            # 在图上画出角度值，增加专业感
            # 在图上画出角度值
            if draw:
                cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            return angle
        return 0