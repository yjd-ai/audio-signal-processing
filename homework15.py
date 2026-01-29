import tkinter as tk
from tkinter import filedialog
import librosa
import threading
import numpy as np
from scipy import signal
import simpleaudio as sa
import myPackage.signal as sg
import myPackage.widget as wg

#==初始化参数==========================
y = None
y1 = None
Fs = 0
N = 0
is_playing = False
play_obj = None
f = [(20, 60), (60, 100), (100, 150), (150, 300), (300, 500), (500, 1000),(1000, 2000), (2000, 3000), (3000, 4000),
     (4000, 5000), (5000, 6000), (6000, 8000), (8000, 10000), (10000, 12000), (12000, 16000), (16000, 20000)]
f_center = ["40Hz", "80Hz", "125Hz", "225Hz", "400Hz", "750Hz","1500Hz", "2500Hz","3500Hz","4500Hz","5500Hz","7000Hz",
            "9000Hz","11000Hz","14000Hz","18000Hz"]
scales = []
#==自定义函数==============================
def drawFunc(t, y):
    ax2.clear()
    ax2.grid()
    ax2.plot(t, y)
    ax2.set_ylim(-1, 1)
    chart.draw()

#==回调函数================================
def open_file():
    global y, Fs, N
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
        y, Fs = librosa.load(file_entry_var.get(), sr=None, mono=True)
        N = len(y)
        t = np.arange(N) / Fs
        ax1.plot(t, y)
        ax1.set_ylim(-1, 1)
        chart.draw()

def play_audio(Fs, y):
    global is_playing, play_obj
    normalized_signal = sg.normalize(y)
    audio_data = (normalized_signal * 32767).astype(np.int16)
    play_obj = sa.play_buffer(audio_data, 1, 2, Fs)
    play_obj.wait_done()
    is_playing = False
    play_obj = None
    play_btn.config(text="播放")

def play():
    global is_playing,y,Fs,y1,play_obj
    if y1 is None:
        return
    if not is_playing:
        play_btn.config(text="停止")
        is_playing = True
        play_thread = threading.Thread(target=play_audio, args=(Fs, y1) ,daemon=True)
        play_thread.start()
    else:
        play_btn.config(text="播放")
        is_playing = False
        play_obj.stop()
        play_obj = None

def filter():
    global Fs, y, y1
    if y is None:
        return
    y1 = None
    y1 = modify_audio(y, Fs)
    t = np.arange(len(y1)) / Fs
    drawFunc(t, y1)

def modify_audio(y, Fs):
    global f
    y_arr = np.zeros_like(y)
    k = 0
    for i in f:
        z, _ = sg.FIR_own(51, i[0], i[1], 44100, y, 2)
        values = int(scales[k].get())
        mutiple = 10 ** (values/20)
        y_arr += z * mutiple
        k += 1
    return y_arr / 2

# ==创建窗口===============================
root = tk.Tk()
root.geometry("1000x650")
root.config(background='#dbeded')
root.title('数字均衡器')

# ==插入播放按钮======================
play_btn = tk.Button(root, text="播放", bg="#003355", font=12, fg='white', command=play)
play_btn.place(x=10, y=20, width=120, height=32)

# ==插入滤波按钮========================
stop_btn = tk.Button(root, text="滤波", bg="#003355", font=12, fg='white', command=filter)
stop_btn.place(x=150, y=20, width=120, height=32)

# ==插入文件按钮================================
file_btn = tk.Button(root, text="文件", bg="#003355", font=12, fg='white', command=open_file)
file_btn.place(x=290, y=20, width=120, height=32)

# ==文件路径编辑框=======================
file_entry_var = tk.StringVar()
file_entry = tk.Entry(root, textvariable=file_entry_var)
file_entry.place(x=430, y=20, width=550, height=32)

#插入均衡器滑块==================================
for i in range(len(f)):
    scale=tk.Scale(root,resolution = 1,orient = tk.VERTICAL ,from_=12, to=-12, bg = 'white',troughcolor='#003355', showvalue=0)
    scale.place(x = 30 + i * 60 ,y = 65,width = 15,height = 200)
    scale.set(0)
    scales.append(scale)
    scale_label = tk.Label(root, text=f_center[i], font=("SimHei", 8), bg='#dbeded', fg="black")
    scale_label.place(x=20 + i * 60, y=270)
#插入滑块标签===============================
scale_label1 = tk.Label(root, text="-12DB", font=("SimHei", 10), bg = '#dbeded', fg="blue")
scale_label1.place(x=950, y=245)

scale_label2 = tk.Label(root, text="+12DB", font=("SimHei", 10), bg = '#dbeded', fg="blue")
scale_label2.place(x=950, y=60)

# 插入Matplotlib图表 ==============
chart, ax1, ax2 = wg.getfigure2(root, 10, 300, 950, 300)

# ==显示窗口=================================
root.mainloop()