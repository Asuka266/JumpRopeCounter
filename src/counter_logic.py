import time


class CounterLogic:
    def __init__(self, image_height=720):  # 可以传进来，或者后续动态获取
        self.state = 'ground'
        self.jump_count = 0
        self.last_movement_time = time.time()
        self.pause_threshold = 5.0
        self.movement_threshold = 8  # 像素位移阈值（根据实际情况调，5~15）

        self.initial_ankle_y = None
        self.jump_threshold = 40  # 初始跳跃阈值（像素），后续可自适应
        self.calibration_frames = 0
        self.calibration_count = 10

        self.prev_ankle_y = None
        self.image_height = image_height  # 用于相对阈值计算（可选）

    def update(self, lm_list):
        """
        lm_list: 来自 pose_module.get_landmarks() 的 [[id, cx, cy], ...] 列表
        返回: (jump_count, is_paused, feedback)
        """
        if not lm_list:
            return self.jump_count, True, "No landmarks"

        # 找左右踝关节（27:left_ankle, 28:right_ankle）
        left_ankle = next((lm for lm in lm_list if lm[0] == 27), None)
        right_ankle = next((lm for lm in lm_list if lm[0] == 28), None)

        if not left_ankle or not right_ankle:
            return self.jump_count, True, "Ankles not detected"

        _, _, left_y = left_ankle
        _, _, right_y = right_ankle
        current_ankle_y = (left_y + right_y) / 2  # 像素坐标，y向下增大

        # 校准阶段
        if self.calibration_frames < self.calibration_count:
            if self.initial_ankle_y is None:
                self.initial_ankle_y = current_ankle_y
            else:
                self.initial_ankle_y = (self.initial_ankle_y * self.calibration_frames + current_ankle_y) / (
                            self.calibration_frames + 1)
            self.calibration_frames += 1

            # 自适应阈值：假设站立时脚在画面下部，跳起时向上移动约画面高度的8-15%
            self.jump_threshold = self.image_height * 0.10  # 或根据实际调 40~80 像素
            self.prev_ankle_y = current_ankle_y
            self.last_movement_time = time.time()
            return self.jump_count, False, f"Calibrating... ({self.calibration_frames}/{self.calibration_count})"

        if self.prev_ankle_y is None:
            self.prev_ankle_y = current_ankle_y
            return self.jump_count, False, ""

        # 检测是否有明显运动（防误判静止）
        displacement = abs(current_ankle_y - self.prev_ankle_y)
        if displacement > self.movement_threshold:
            self.last_movement_time = time.time()

        self.prev_ankle_y = current_ankle_y

        # 状态机（注意：像素坐标 y 向下增大，所以跳起时 y 减小）
        if self.state == 'ground':
            if current_ankle_y < self.initial_ankle_y - self.jump_threshold:
                self.state = 'air'
        elif self.state == 'air':
            if current_ankle_y > self.initial_ankle_y - (self.jump_threshold * 0.4):  # 回落到接近初始位置
                self.state = 'ground'
                self.jump_count += 1

        # 暂停判断
        is_paused = (time.time() - self.last_movement_time > self.pause_threshold)
        feedback = "Paused - keep jumping!" if is_paused else "Good rhythm!" if self.jump_count % 10 == 0 else ""

        return self.jump_count, is_paused, feedback