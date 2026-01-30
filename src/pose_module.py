import cv2
import mediapipe as mp
import math

# 定义各个身体部位的索引
LEFT_HIP = 23
RIGHT_HIP = 24
LEFT_KNEE = 25
RIGHT_KNEE = 26
LEFT_ANKLE = 27
RIGHT_ANKLE = 28
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16

class pose_detector:
    def __init__(self, detection_con=0.5, track_con=0.5):
        # 初始化MediaPipe
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=detection_con,
                                      min_tracking_confidence=track_con)

    def find_pose(self, img, draw=True):
        # 具体识别人物
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)# 颜色空间转换
        self.results = self.pose.process(img_rgb)
        if self.results.pose_landmarks and draw:
            self.mp_draw.draw_landmarks(img, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return img

    def get_landmarks(self, img):
        # 将MediaPipe得到的数据转化为具体的像素坐标
        self.lm_list = []
        if self.results and self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # 将0-1的相对比例换算成实际像素坐标
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])
        return self.lm_list

    def find_angle(self, img, p1, p2, p3, draw=True):
        if len(self.lm_list) != 0:
            # 获取三个点的坐标
            x1, y1 = self.lm_list[p1][1:]
            x2, y2 = self.lm_list[p2][1:]
            x3, y3 = self.lm_list[p3][1:]

            # 计算角度
            angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                 math.atan2(y1 - y2, x1 - x2))
            if angle < 0:
                angle += 360
            if angle > 180:
                angle = 360 - angle

            # 在图上画出角度值
            if draw:
                cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            return angle
        return 0