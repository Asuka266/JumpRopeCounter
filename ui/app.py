import streamlit as st
import sys
import os

# 核心：告诉 Python 去上一级目录的 src 文件夹里找代码
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 预留给成员 B 和 A 的接口
# from src.pose_module import PoseDetector
# from src.counter_logic import JumpCounter

st.title("🏃 AI 跳绳计数器 - 核心框架已就绪")
st.info("成员 A 已完成目录重构，请各成员在对应文件夹编写代码。")