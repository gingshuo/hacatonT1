import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import shutil
import subprocess
import os
import time
import sys

# 动态获取当前脚本所在的目录
if getattr(sys, 'frozen', False):  # 判断是否为 .exe 文件
    SCRIPT_DIR = os.path.dirname(sys.executable)  # 获取 .exe 文件的路径
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取 Python 脚本的路径

# 设置相对路径，上传的文件将保存到data文件夹
UPLOAD_FOLDER = os.path.join(SCRIPT_DIR, 'data')

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def upload_file():
    """Upload file to specific path，Rename to input.csv"""
    # 打开文件选择对话框
    file_path = filedialog.askopenfilename(title="Select file to upload")
    if file_path:
        # 提取文件名
        file_name = os.path.basename(file_path)
        # 构造目标文件路径，重命名为 input.csv
        destination_path = os.path.join(UPLOAD_FOLDER, 'input.csv')

        # 将文件复制到目标文件夹并重命名
        shutil.copy(file_path, destination_path)
        label_status.config(text=f"File uploaded and renamed as input.csv")
    else:
        label_status.config(text="No file selected")

def run_score_and_max():
    """运行 score_and_max.py 文件"""
    try:
        # 开始计时
        start_time = time.time()

        # 更新状态信息和进度条
        label_status.config(text="Running score_and_max.py ...")
        progressbar.start()

        # 运行 score_and_max.py 文件
        subprocess.run(["python", os.path.join(SCRIPT_DIR, "code", "score_and_max.py")], check=True)

        # 结束计时
        end_time = time.time()
        elapsed_time = end_time - start_time

        # 停止进度条
        progressbar.stop()
        
        # 显示执行成功消息和运行时间
        label_status.config(text=f"Succeeded! Running time: {elapsed_time:.2f} seconds")
    except subprocess.CalledProcessError as e:
        progressbar.stop()
        label_status.config(text=f"Execution error: {e}")

def run_score_and_aggregate():
    """运行 score_and_aggregate.py 文件"""
    try:
        # 开始计时
        start_time = time.time()

        # 更新状态信息和进度条
        label_status.config(text="Running score_and_aggregate.py ...")
        progressbar.start()

        # 运行 score_and_aggregate.py 文件
        subprocess.run(["python", os.path.join(SCRIPT_DIR, "code", "score_and_aggregate.py")], check=True)

        # 结束计时
        end_time = time.time()
        elapsed_time = end_time - start_time

        # 停止进度条
        progressbar.stop()
        
        # 显示执行成功消息和运行时间
        label_status.config(text=f"Succeeded! Running time: {elapsed_time:.2f} seconds")
    except subprocess.CalledProcessError as e:
        progressbar.stop()
        label_status.config(text=f"Execution error: {e}")

def exit_program():
    """退出程序"""
    root.quit()

# 创建主窗口
root = tk.Tk()
root.title("Upload and Run")

# 设置窗口大小和背景颜色
root.geometry("500x400")  # 增加窗口高度，确保按钮显示
root.configure(bg="#f0f0f0")  # 设置背景色为灰白色

# 设置字体样式
font_style = ('Arial', 12)

# 创建并放置按钮和标签
button_upload = tk.Button(root, text="Upload File", command=upload_file, font=font_style, bg="#4CAF50", fg="white", relief="flat", width=20, height=2)
button_upload.pack(pady=15)

button_run_score_and_max = tk.Button(root, text="Simple Find", command=run_score_and_max, font=font_style, bg="#2196F3", fg="white", relief="flat", width=20, height=2)
button_run_score_and_max.pack(pady=10)

button_run_score_and_aggregate = tk.Button(root, text="Complicated Find", command=run_score_and_aggregate, font=font_style, bg="#FF9800", fg="white", relief="flat", width=20, height=2)
button_run_score_and_aggregate.pack(pady=10)

label_status = tk.Label(root, text="Please upload file and select script", fg="#333", bg="#f0f0f0", font=("Arial", 14))
label_status.pack(pady=10)

# 创建进度条
progressbar = ttk.Progressbar(root, orient="horizontal", length=400, mode="indeterminate")
progressbar.pack(pady=20)

# 创建退出按钮，并增加适当的 padding
button_exit = tk.Button(root, text="Exit", command=exit_program, font=font_style, bg="#f44336", fg="white", relief="flat", width=20, height=2)
button_exit.pack(pady=20)  # 增加更多间距，确保退出按钮显示

# 运行主事件循环
root.mainloop()
