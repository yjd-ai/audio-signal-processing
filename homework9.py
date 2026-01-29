import threading
import tkinter as tk
import numpy as np
from tkinter import filedialog
import subprocess
import librosa
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import myPackage.signal as sg
import myPackage.widget as wg
#==初始化参数===================
Fs = 0
N = 0
y = 0
t = []
sxx = []
ff, yy = [], []
i = 0
recording_flag = False
recording_thread = None
timer_id = None
ffplay_process = None

#==自定义函数======================
#麦克风
def mic_record_thread():
    global recording_flag, ff, yy
    while recording_flag:
        mic_data = sg.audio_mic(44100, 2048, 1)
        f, y = sg.AmplitudeSpetrum(2048, 44100, mic_data)
        y = sg.normalize(y)
        fig.draw(0.05, f, y, multiple=10)
        for m in range(len(ff)):
            for n in range(len(ff[m])):
                ff[m][n] += 50
                yy[m][n] += 0.15
        ff.append(f[1:])
        yy.append(y[1:])
        drawFunc()

#结束播放
def monitor_ffplay():
    global ffplay_process, timer_id, i
    if ffplay_process:
        # 等待ffplay进程结束
        ffplay_process.wait()
        # 进程结束后，关闭定时任务
        if timer_id:
            root.after_cancel(timer_id)
            global i
            i = 0

def getfigure(win, x0, y0, w, h):
    px=1/plt.rcParams['figure.dpi']
    fig=plt.Figure(figsize=(w * px, h*px))
    fig.patch.set_facecolor('#dbeded')
    chart=FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x = x0, y = y0)
    ax=fig.add_subplot(111)
    #ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_facecolor('#dbeded')
    ax.set_xlabel('Fs', x=0.3, y=0)
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)
    points = [(0, 0), (0.7, 0), (1, 0.8), (0.35, 0.8)]
    border = patches.Polygon(points, transform=ax.transAxes, fill = False)
    ax.add_patch(border)
    ax.set_xlim(0, 5000)
    ax.set_xticks(np.arange(0, 3001, 1000))
    fig.tight_layout()
    return chart, ax

def drawFunc():
    global ff, yy
    ax.clear()
    points = [(0, 0), (0.7, 0), (1, 0.8), (0.35, 0.8)]
    border = patches.Polygon(points, transform=ax.transAxes, fill=False)
    ax.add_patch(border)
    idx = 0
    for x, y in zip(ff, yy):
        line = ax.plot(x, y, color='#00bac7', zorder=idx, linewidth=3)[0]
        fill = ax.fill_between(x, np.min(y), y, alpha=1, color='black', zorder=idx)
        fill.set_clip_path(border)
        line.set_clip_path(border)
        idx += 1
    if len(ff) > 28:
        ff.pop(0)
        yy.pop(0)
    ax.set_xlim(0, 5000)
    ax.set_xticks(np.arange(0, 3001, 1000))
    ax.set_ylim(0, 5)
    ax.set_xlabel('Fs', x = 0.3, y = 0)
    chart.draw_idle()

#==回调函数=================
#开关按钮
def spec(state):
    global recording_flag, recording_thread
    recording_flag = state
    if state == True:
        recording_thread = threading.Thread(target=mic_record_thread, daemon = True)
        recording_thread.start()

# 打开文件
def open_file():
    file_types = [
        ("音视频文件", "*.mp3;*.mp4;*.wav")
    ]
    file_path = filedialog.askopenfilename(
        title="选择音视频文件",
        filetypes=file_types,
        initialdir="E:\DRPython38qt5\data"  # 初始目录
    )
    if file_path:
        file_entry_var.set(file_path)
def show_wave():
    global sxx, i, timer_id, ffplay_process, ff, yy
    if i > len(sxx):
        if timer_id:
            root.after_cancel(timer_id)
            timer_id = None
            i = 0
    f1 = sxx[i][0]
    y1 = sxx[i][1]
    y2 = sg.normalize(y1)
    if ff:
        ff_np = np.array(ff)
        yy_np = np.array(yy)
        ff_np += 50
        yy_np += 0.15
        ff = ff_np.tolist()
        yy = yy_np.tolist()
    ff.append(f1[1:])
    yy.append(y2[1:])
    drawFunc()
    fig.draw(0.04, f1, y2, multiple=100)
    i += 1
    timer_id = root.after(50, show_wave)
    if ffplay_process.poll() is not None:
        # 进程已终止，关闭定时任务
        if timer_id:
            root.after_cancel(timer_id)
            timer_id = None
            i = 0

def play():
    global y, Fs, N, t, sxx, i, timer_id, ffplay_process
    file_path = file_entry_var.get()
    if file_path:
        ffplay_process = subprocess.Popen(["ffplay", file_path])
        y, Fs = librosa.load(file_path, sr=None, mono=True)  # mono=True 转为单声道
        N = len(y)

        t, sxx = sg.STFTAmplitudeSpetrum(Fs, N, y)
        timer_id = root.after(50, show_wave)
        monitor_thread = threading.Thread(target=monitor_ffplay, daemon=True)
        monitor_thread.start()

def clear():
    global ff, yy
    fig.clear();
    ax.clear()
    points = [(0, 0), (0.7, 0), (1, 0.8), (0.35, 0.8)]
    border = patches.Polygon(points, transform=ax.transAxes, fill=False)
    ax.add_patch(border)
    ax.set_xlim(0, 5000)
    ax.set_xticks(np.arange(0, 3001, 1000))
    ax.set_ylim(0, 5)
    ax.set_xlabel('Fs', x=0.3, y=0)
    chart.draw_idle()
    ff = []
    yy = []

# 窗口关闭
def win_close():
    global recording_flag, ffplay_process, timer_id, recording_thread
    if recording_flag:
        recording_flag = False
        recording_thread = None
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None
    if ffplay_process:
        ffplay_process.terminate()
        ffplay_process = None
    root.destroy()

#==创建窗口===============================
root = tk.Tk()
root.geometry("1350x600")
root.config(background='#dbeded')
root.title('谱阵图显示')
root.protocol("WM_DELETE_WINDOW", win_close) # 窗口关闭
#==插入谱阵图显示控件=======================
fig = wg.spectrum_figure(root, x = 20, y = 250, width = 500, height = 380)

#==插入开关标签================================
switch_label = tk.Label(root, text = '麦克风',  bg = '#dbeded', font = ('SimHei', 12), fg = "#324e35")
switch_label.place(x = 700,y = 20,width = 100,height = 32)

#======插入开关麦克风按钮========================
switch = wg.ToggleSwitch(root, x = 660, y = 20, width = 60, height = 30, active_color = "#6C4B43", command = spec)

# ==插入清空按钮======================
play_btn = tk.Button(root, text="清空", bg="#003355", font=12, fg='white', command = clear)
play_btn.place(x=10, y=20, width=120, height=32)

# ==插入播放按钮======================
play_btn = tk.Button(root, text="播放", bg="#003355", font=12, fg='white', command = play)
play_btn.place(x=10, y=100, width=120, height=32)

# ==插入文件按钮================================
file_btn = tk.Button(root, text="文件", bg="#003355", font=12, fg='white', command=open_file)
file_btn.place(x=150, y=100, width=120, height=32)

# ==文件路径编辑框=======================
file_entry_var = tk.StringVar()
file_entry = tk.Entry(root, textvariable=file_entry_var)
file_entry.place(x=300, y=100, width=470, height=32)

# 插入MatplotlibCurve ==============
chart, ax = getfigure(root,800,20,540, 520)

#==显示窗口=================================
root.mainloop()