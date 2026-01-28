🏃‍♂️ AI 智能跳绳计数助手 (JumpRopeCounter)
本项目是一款基于 MediaPipe Pose 姿态估计技术的智能跳绳计数应用。通过摄像头实时捕捉人体关键点，自动计算跳绳次数、运动时长，并提供实时反馈。

🛠️ 技术栈
核心算法: Python 3.x + MediaPipe (姿态检测)

视频处理: OpenCV

交互界面: Streamlit (基于 Web 的快速前端框架)

环境管理: Virtualenv (venv)

📂 项目结构说明
app.py: [前端/集成] Streamlit 界面逻辑，负责展示视频流和 UI 交互。

pose_module.py: [核心算法] 封装 MediaPipe 检测类，输出人体关键点坐标。

counter_logic.py: [计数逻辑] 基于坐标高度变化判定跳绳动作并计数。

config.py: [配置中心] 存放视频分辨率、判定阈值等参数。

requirements.txt: [环境清单] 列出了运行本项目所需的依赖包。

🚀 开发者安装指南 (组员必看)
如果你是第一次参与本项目开发，请按照以下步骤配置环境：

克隆项目：

Bash

git clone [你的仓库链接]
创建并激活虚拟环境 (在 PyCharm 中通常会自动完成)：

Bash

python -m venv .venv
一键安装依赖： 在 PyCharm 的终端 (Terminal) 中输入：

Bash

pip install -r requirements.txt
注：如果下载过慢，请使用镜像源： pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

启动程序： 在终端输入以下命令启动网页：

Bash

streamlit run ui/app.py
👥 小组分工
成员 A (组长): 负责总体架构搭建、pose_module.py 核心引擎开发。

成员 B: 负责 counter_logic.py 计数算法实现及逻辑测试。

成员 C: 负责 app.py 前端界面设计与用户交互优化。

成员 D: 负责 环境配置管理、集成测试及文档撰写。