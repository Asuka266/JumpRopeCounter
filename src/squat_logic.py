class squat_logic:
    def __init__(self):
        self.state="up"# 初始状态
        self.count=0# 计数
        self.feedback=""# 反馈

    def do_squat(self,detector,img):
        # 调用pose_module的函数来获取左腿或右腿的角度
        # 23:左胯，25：左膝，27：左踝
        angle=detector.find_angle(img,23,25,27)

        if angle<100:
            if self.state=="up":
                self.state="down"

        if angle>160:
            if self.state=="down":
                self.state="up"
                self.count+=1
                self.feedback="真棒!"

        return self.count,self.feedback