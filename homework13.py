import time
import tkinter as tk
import numpy as np
from matplotlib.animation import FuncAnimation
import librosa
import simpleaudio as sa
import threading
import time
import myPackage.signal as sg
import myPackage.widget as wg

# ==初始化参数=====================
y1 = None
mySignal = None
Fs = 0
N = 0
t = None
progress_line = None
progress_line_left = None
progress_line_right = None
play_obj = None
is_playing = False
is_playing2 = False
animation = None

# ==自定义函数======================
def draw_ax12():
    global y1, Fs, N, t, f1, A1, progress_line, progress_line_left, progress_line_right
    file_path = file_entry_var.get()
    y1 = None
    y1, Fs = librosa.load(file_path, sr=None, mono=True)
    N = len(y1)
    t = np.arange(N) / Fs
    f1, A1 = sg.AmplitudeSpetrum(N, Fs, y1)
    noise_scale_left.config(from_=0, to=N - 1, command=update_line)
    noise_scale_right.config(from_=0, to=N - 1, command=update_line)
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax1.plot(t, y1, color="yellow")
    ax2.plot(f1, A1, color="yellow")
    ax2.set_xlim(0, 4000)

    # 创建进度线
    progress_line = ax1.axvline(x=0, color='red', linestyle='--', linewidth=2)
    progress_line_left = ax1.axvline(x=0, color='green', linestyle='--', linewidth=2)  # 滑块线
    progress_line_right = ax1.axvline(x=0, color='green', linestyle='--', linewidth=2)  # 滑块线
    chart.draw()

def draw_ax34():
    global y1, Fs, t, N, mySignal
    if y1 is not None:
        n1 = int(noise_svar_left.get())
        n2 = int(noise_svar_right.get())
        y2 = y1[n1:n2+1]
        s = librosa.stft(y1)
        ss = np.abs(s)
        angle = np.angle(s)
        b = np.exp(1.0j * angle)
        ns = librosa.stft(y2)
        nss = np.abs(ns)
        mns = np.mean(nss, axis=1)
        K = float(K_entry_var.get())
        sa = ss - K * mns.reshape((mns.shape[0], 1))
        sa[sa < 0] = 0
        sa0 = sa * b
        mySignal = librosa.istft(sa0)
        n = len(mySignal)
        t2 = np.arange(n) / Fs
        f2, A2 = sg.AmplitudeSpetrum(n, Fs, mySignal)
        ax3.clear()
        ax4.clear()
        ax3.plot(t2, mySignal)
        ax4.set_xlim(0, 4000)
        ax4.plot(f2, A2)
        chart.draw()

# ==回调函数=============================
def open_file():
    file_types = [
        ("音视频文件", "*.mp3;*.mp4;*.wav")
    ]
    file_path = tk.filedialog.askopenfilename(
        title="选择音视频文件",
        filetypes=file_types,
        initialdir="E:\DRPython38qt5\Python38\Lib\site-packages\drvi\dataset"  # 初始目录
    )
    if file_path:
        file_entry_var.set(file_path)
    draw_ax12()

#音频播放线程
def play_audio(data, sr):
    global play_obj
    normalized_signal = sg.normalize(data)
    audio_data = (normalized_signal * 32767).astype(np.int16)
    play_obj = sa.play_buffer(audio_data, 1, 2, sr)
    play_obj.wait_done()
    is_playing = False
    play_audio = None

#播放进度线更新
def update_progress(fram):
    global progress_line, is_playing, start_time, animation, t
    if not is_playing:
        animation = None
        return (progress_line,)
    elapsed_time = time.time() - start_time
    if elapsed_time > t[-1]:
        is_playing = False
        return (progress_line,)
    progress_line.set_xdata([elapsed_time])
    return (progress_line,)

#==滑块线进度更新============================
def update_line(val):
    global progress_line_left, progress_line_right, t, N
    if noise_svar_left.get() <= noise_svar_right.get():
        progress_line_left.set_visible(True)
        progress_line_right.set_visible(True)
        progress_line_left.set_xdata([t[int(noise_svar_left.get())]])
        progress_line_right.set_xdata([t[int(noise_svar_right.get())]])
        ax1.figure.canvas.draw_idle()
    else:
        progress_line_left.set_visible(False)
        progress_line_right.set_visible(False)
        ax1.figure.canvas.draw_idle()

def play1():
    global y1, Fs, is_playing, play_obj, start_time, animation, is_playing2
    if y1 is None or is_playing2:
        return
    if is_playing:
        play_obj.stop()
        play_obj = None
        is_playing = False
        animation.event_source.stop()
        return
    is_playing = not is_playing
    audio_thread = threading.Thread(target=play_audio, args=(y1, Fs),daemon=True)
    audio_thread.start()
    start_time = time.time()
    #进度线
    animation = FuncAnimation(
        ax1.figure,
        update_progress,
        interval=50,
        blit=True,
        cache_frame_data=False
    )
def play2():
    global mySignal, Fs, is_playing, play_obj, is_playing2
    if mySignal is None or is_playing:
        return
    if is_playing2:
        play_obj.stop()
        play_obj = None
        is_playing2 = False
        return
    is_playing2 = not is_playing2
    audio_thread2 = threading.Thread(target=play_audio, args=(mySignal, Fs), daemon=True)
    audio_thread2.start()

# ==创建窗口===============================
root = tk.Tk()
root.geometry("1000x700")
root.config(background='#dbeded')
root.title('谱减法降噪')

# ==插入噪声截取按钮======================
get_noise_btn = tk.Button(root, text="噪声截取", bg="#003355", font=12, fg='white', command=draw_ax34)
get_noise_btn.place(x=30, y=20, width=120, height=32)

# ==插入文件按钮================================
file_btn = tk.Button(root, text="文件", bg="#003355", font=12, fg='white', command=open_file)
file_btn.place(x=170, y=20, width=120, height=32)

# ==文件路径编辑框=======================
file_entry_var = tk.StringVar()
file_entry = tk.Entry(root, textvariable=file_entry_var, background="black", fg="white")
file_entry.place(x=300, y=20, width=600, height=32)

# ==降噪因子编辑框=======================
K_label = tk.Label(root, text="K:", font=("SimHei", 15), bg = '#dbeded', fg="blue")
K_label.place(x=920, y=20)
K_entry_var = tk.StringVar(value='2')
K_entry = tk.Entry(root, textvariable=K_entry_var, background="white", fg="black", justify=tk.CENTER)
K_entry.place(x=950, y=20, width=40, height=32)

# 插入Matplotlib图表 ==============
chart, ax1, ax2, ax3, ax4 = wg.getfigure4(root, 30, 60, 950, 630)

# ==插入播放按钮1======================
play_btn1 = tk.Button(root, text="⏯️", bg="#5B97E1", font=8, fg='white', anchor='e', command=play1)
play_btn1.place(x=500, y=62, width=28, height=15)

#==插入滑块=============================
noise_svar_left=tk.DoubleVar()
noise_scale_left=tk.Scale(root,variable=noise_svar_left,resolution = 1,
                         orient = tk.HORIZONTAL ,bg = 'white',troughcolor='#003355', showvalue=0)
noise_scale_left.place(x = 80,y = 62,width = 410,height = 15)
noise_scale_left.set(0)

noise_svar_right=tk.DoubleVar()
noise_scale_right=tk.Scale(root,variable=noise_svar_right,resolution = 1,
                         orient = tk.HORIZONTAL ,bg = 'white',troughcolor='#003355', showvalue=0)
noise_scale_right.place(x = 535,y = 62,width = 420,height = 15)
noise_scale_right.set(0)

# ==插入播放按钮2======================
play_btn2 = tk.Button(root, text="⏯️", bg="#5B97E1", font=8, fg='white', anchor='e', command=play2)
play_btn2.place(x=500, y=520, width=28, height=15)

# ==显示窗口=================================
root.mainloop()