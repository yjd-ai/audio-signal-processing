import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
import threading
import time
import pygame
import numpy as np
import pyaudio
import myPackage.widget as wg
import myPackage.signal as sg

# ==初始化参数===================
Fs, N = 44100, 2048
title = ["时域波形图(长时)", "时域波形图(短时)", ]
is_playing = False  # 播放状态标记
is_recording = False  # 录音状态标记
y = []  # 存储麦克风数据
pygame.mixer.init()  # 初始化pygame音频系统
win = sg.winFunction(2, N) #汉宁窗

#==自定义函数=============================
def drawFunc():
    t = np.arange(N) / Fs
    ax1.clear()
    ax1.grid()
    ax1.plot(t, y, color = 'y')
    ax1.set_title('时域波形图', color = 'white')
    ax1.set_xlim(0.01, 0.02)
    ax1.set_ylim(-1, 1)
    f, y1 = sg.AmplitudeSpetrum(N,Fs,y)
    ax2.clear()
    ax2.grid()
    ax2.plot(f, y1, color='y')
    ax2.set_title("幅频谱图", color = 'white')
    ax2.set_ylim(0, 0.4)

    chart.draw()


def mic_recording_thread():
    global y, is_recording
    while is_recording:
        # 读取麦克风数据
        mic_data = sg.audio_mic(Fs, N, 1)
        if mic_data is not None:
            # 将新数据添加到y列表中
            y = (mic_data) * win
            drawFunc()
        # 短暂休眠，降低CPU占用
        time.sleep(0.01)

# ==播放控制函数=================
def play_thread(file_path):
    global is_playing, is_recording, y
    # 开始播放
    pygame.mixer.music.play()
    # 启动麦克风录制
    is_recording = True
    y = []  # 清空之前的麦克风数据
    threading.Thread(target=mic_recording_thread, daemon=True).start()

    # 循环检查播放状态
    while is_playing and pygame.mixer.music.get_busy():
        time.sleep(0.1)

    # 播放结束，停止录制
    is_playing = False
    is_recording = False


def playFunc():
    global is_playing
    file_path = file_entry_var.get()
    if not file_path:
        return
    if is_playing:
        stopFunc()
    try:
        # 加载音频文件
        pygame.mixer.music.load(file_path)
        is_playing = True
        # 启动播放线程，将file_path作为参数传递
        threading.Thread(target=play_thread, args=(file_path,), daemon=True).start()
    except Exception as e:
        print(f"播放错误: {str(e)}")
        is_playing = False
        is_recording = False


def stopFunc():
    global is_playing, is_recording
    if is_playing:
        pygame.mixer.music.stop()
        is_playing = False
    if is_recording:
        is_recording = False


def open_file():
    file_types = [
        ("音频文件", "*.mp3")
    ]
    file_path = filedialog.askopenfilename(
        title="选择音视频文件",
        filetypes=file_types,
        initialdir="."  # 初始目录
    )
    if file_path:
        file_entry_var.set(file_path)


# 建立tkinter GUI 窗口==============
root = tk.Tk()
root.geometry('1000x500')
root.config(bg="#dbeded")
root.wm_title('音视频文件波形及频谱分析')

# ==插入播放按钮======================
play_btn = tk.Button(root, text="播放", bg="#003355", font=12, fg='white', command=playFunc)
play_btn.place(x=10, y=20, width=120, height=32)

# ==插入停止按钮========================
stop_btn = tk.Button(root, text="停止", bg="#003355", font=12, fg='white', command=stopFunc)
stop_btn.place(x=150, y=20, width=120, height=32)

# ==插入文件按钮================================
file_btn = tk.Button(root, text="文件", bg="#003355", font=12, fg='white', command=open_file)
file_btn.place(x=290, y=20, width=120, height=32)

# ==文件路径编辑框=======================
file_entry_var = tk.StringVar()
file_entry = tk.Entry(root, textvariable=file_entry_var)
file_entry.place(x=430, y=20, width=550, height=32)

# 插入信号显示框==============
def set_axis_style(ax):
    ax.set_facecolor('black')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='both', colors='white')
    ax.grid(True, color='white', linestyle='--', linewidth=0.5, alpha=0.7)
    return ax
def getfigure(win, x0, y0, w, h):
    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.Figure(figsize=(w * px, h * px))
    fig.patch.set_facecolor('#003355')
    chart = FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x=x0, y=y0)
    ax1 = set_axis_style(fig.add_subplot(211))
    ax2 = set_axis_style(fig.add_subplot(212))
    fig.tight_layout()
    return chart, ax1, ax2

plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
chart, ax1, ax2 = getfigure(root, 10, 80, 980, 400)

# =Tkinter主窗口循环控制==============
root.mainloop()