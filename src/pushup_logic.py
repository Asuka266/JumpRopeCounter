class pushup_logic:
    def __init__(self):
        self.state="up"# 初始状态
        self.count=0# 初始俯卧撑数量
        self.feedback=""

    def do_push(self,detector,img):
        # 首先调用pose_module的函数来获取胳膊弯曲角度
        # 11: 肩膀, 13: 肘部, 15: 手腕
        angle=detector.find_angle(img,11,13,15)

        # 判断是否成功做了一个俯卧撑
        if angle<90:
            if self.state=="up":
                self.state="down"# 状态的一个更新

        if angle>150:
            if self.state=="down":
                self.state="up"# 状态的一个更新
                self.count+=1
                self.feedback="做得好！"

        return self.count,self.feedback

