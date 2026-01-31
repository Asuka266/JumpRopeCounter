AI 健身助手 (AI Fitness Assistant)
这是一个基于 Python Flask 和 MediaPipe 开发的实时健身监测系统。系统通过电脑摄像头捕捉人体骨骼关键点，实时计算动作角度或位移，实现深蹲、俯卧撑和跳绳的自动计数与动作反馈。

🌟 核心功能
多模式运动监测：

深蹲 (Squat)：监测膝盖弯曲角度，确保动作标准。

俯卧撑 (Pushup)：监测手臂肘部角度。

跳绳 (JumpRope)：基于脚踝 Y 轴位移的智能自适应计数。

实时反馈系统：网页端实时显示当前运动计数（Total Count）和动作状态反馈（如 "READY"、"Go Down!" 等）。

交互式 Web 界面：支持一键开启摄像头、动态切换运动模式以及安全关闭系统。

双版本支持：提供本地直接运行的调试版本 (local_app.py) 和基于 Web 浏览器的完整版 (web_app.py)。

🛠️ 环境要求
Python: 3.10+ (推荐)

主要依赖库：

mediapipe==0.10.9 (用于人体姿态识别)

opencv-python (用于视频流处理)

flask (用于构建 Web 后端)

🚀 快速启动
1. 安装依赖
在项目根目录下打开终端，运行：

Bash
pip install -r requirements.txt
2. 启动程序
运行 Web 版本：

Bash
python web_app.py
3. 访问系统
在浏览器中输入 http://127.0.0.1:5000。

点击页面上的 "开启摄像头" 按钮并授权访问。

选择你想要的运动模式，开始健身！

📂 项目结构
Plaintext
JumpRopeCounter/
├── src/                    # 核心逻辑模块
│   ├── pose_module.py      # MediaPipe 姿态检测封装
│   ├── squat_logic.py      # 深蹲计数算法
│   ├── pushup_logic.py     # 俯卧撑计数算法
│   └── counter_logic.py    # 跳绳计数与自适应校准算法
├── templates/              # 网页模板
│   └── index.html          # 前端交互界面
├── web_app.py              # Flask Web 服务器启动文件
├── local_app.py            # 本地 OpenCV 窗口调试文件
└── requirements.txt        # 项目依赖清单
⚠️ 使用注意事项
光线与环境：请确保光线充足，并让摄像头能够完整捕捉到全身（特别是深蹲和跳绳模式下的脚踝部分）。

安全关闭：请使用网页上的 "退出程序" 按钮关闭系统，这会自动释放摄像头硬件资源并停止 Python 进程。

Debug 模式：本系统在 web_app.py 中默认关闭了 debug 模式，以防止多个进程竞争同一个摄像头资源。
