import tkinter as tk
from tkinter import filedialog
import librosa
import threading
from threading import Lock
import time
import numpy as np
import sounddevice as sd
from scipy import signal
import myPackage.signal as sg
import myPackage.widget as wg

# ==初始化参数==========================
y = None
Fs = 44100
N = 0
is_playing = False
chunk = 4096
buffer1 = np.zeros(chunk, dtype=np.float32)
buffer2 = np.zeros(chunk, dtype=np.float32)
buffer1_ready = False
buffer2_ready = False
buffer_lock = Lock()
f = [(20, 60), (60, 100), (100, 150), (150, 300), (300, 500), (500, 1000),
     (1000, 2000), (2000, 3000), (3000, 4000), (4000, 5000), (5000, 6000),
     (6000, 8000), (8000, 10000), (10000, 12000), (12000, 16000), (16000, 20000)]
f_center = ["40Hz", "80Hz", "125Hz", "225Hz", "400Hz", "750Hz","1500Hz", "2500Hz","3500Hz","4500Hz","5500Hz","7000Hz",
            "9000Hz","11000Hz","14000Hz","18000Hz"]
scales = []
filter_states = [None] * len(f)  # 存储滤波器状态
# 预计算滤波器系数
filter_coeffs = []
data_finished = False  # 数据结束标志
audio_idx = 0  # 当前播放位置
stream = None  # 音频流对象
play_thread = None  # 播放线程对象
data_thread = None  # 数据处理线程对象


# ==自定义函数==============================
def drawFunc(f, A):
    ax.clear()
    ax.grid()
    ax.set_xlim(0,4000)
    ax.set_ylim(0, 0.2)
    ax.plot(f, A)
    chart.draw_idle()

# ==回调函数================================
def open_file():
    global y, N, filter_states, filter_coeffs, audio_idx
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
        y, _ = librosa.load(file_entry_var.get(), sr=Fs, mono=True)
        N = len(y)
        audio_idx = 0
        filter_states = [None] * len(f)
        filter_coeffs = []
        for idx, band in enumerate(f):
            low, high = band
            b, a = signal.butter(2, [low / (Fs / 2), high / (Fs / 2)], btype='bandpass')
            filter_coeffs.append((b, a))
            zi = signal.lfilter_zi(b, a)
            if zi.ndim > 0:
                filter_states[idx] = np.zeros_like(zi)
            else:
                filter_states[idx] = np.zeros(1)

def read_data():
    global is_playing, buffer1, buffer2, buffer_lock, chunk, buffer1_ready, buffer2_ready, data_finished, audio_idx
    data_finished = False
    while is_playing and audio_idx < N:
        next_idx = min(audio_idx + chunk, N)
        y1 = y[audio_idx:next_idx]
        y2 = modify_audio(y1)
        f, A = sg.AmplitudeSpetrum(len(y2),Fs,y2)
        drawFunc(f,A)
        n = next_idx - audio_idx
        if n < chunk:  # 处理最后一个块
            # 只填充实际数据部分，剩余部分保持为零
            temp_buffer = np.zeros(chunk, dtype=np.float32)
            temp_buffer[:n] = y2
            y2 = temp_buffer

        # 等待缓冲区可用
        while is_playing:
            with buffer_lock:
                if not buffer1_ready:
                    buffer1[:] = y2
                    buffer1_ready = True
                    break
                elif not buffer2_ready:
                    buffer2[:] = y2
                    buffer2_ready = True
                    break
            time.sleep(0.001)
        audio_idx = next_idx
    data_finished = True
    print("数据读取完成")


def audio_callback(outdata, frames, time, status):
    global is_playing, buffer1, buffer2, buffer_lock, buffer1_ready, buffer2_ready, data_finished

    if status:
        print(status)

    with buffer_lock:
        if buffer1_ready:
            #
            outdata[:frames] = buffer1[:frames].reshape(-1, 1)
            buffer1_ready = False
        elif buffer2_ready:
            outdata[:frames] = buffer2[:frames].reshape(-1, 1)
            buffer2_ready = False
        else:
            # 没有数据可用，填充零
            outdata.fill(0)
            # 如果数据已处理完毕，停止播放
            if data_finished:
                raise sd.CallbackStop
            elif is_playing:
                print("Buffer underrun")

def play_audio():
    global is_playing, stream
    try:
        stream = sd.OutputStream(samplerate=Fs, channels=1, callback=audio_callback, blocksize=chunk)
        with stream:
            while is_playing:
                time.sleep(0.1)
    except Exception as e:
        print(f"Audio playback error: {e}")
    finally:
        # 确保播放状态被正确重置
        is_playing = False
        stream = None
        print("音频播放结束")


def play():
    global is_playing, y, N, buffer1_ready, buffer2_ready, filter_states, data_finished, audio_idx, stream, play_thread, data_thread
    # 如果已经在播放，先停止
    if is_playing:
        stop()
        # 等待线程结束
        if data_thread and data_thread.is_alive():
            data_thread.join(0.5)
        if play_thread and play_thread.is_alive():
            play_thread.join(0.5)

    if y is None:
        return

    is_playing = True
    data_finished = False
    audio_idx = 0  # 重置播放位置

    # 重置缓冲区状态
    with buffer_lock:
        buffer1_ready = False
        buffer2_ready = False
        buffer1.fill(0)
        buffer2.fill(0)

    # 重置滤波器状态 - 只在有滤波器系数时进行
    if filter_coeffs:
        for idx in range(len(filter_states)):
            if idx < len(filter_coeffs):
                b, a = filter_coeffs[idx]
                zi = signal.lfilter_zi(b, a)
                if zi.ndim > 0:
                    filter_states[idx] = np.zeros_like(zi)
                else:
                    filter_states[idx] = np.zeros(1)

    # 创建新线程
    data_thread = threading.Thread(target=read_data, daemon=True)
    data_thread.start()
    play_thread = threading.Thread(target=play_audio, daemon=True)
    play_thread.start()


def stop():
    global is_playing, stream, data_thread, play_thread
    is_playing = False
    if stream is not None:
        try:
            stream.stop()
        except:
            pass

    # 等待线程结束
    if data_thread and data_thread.is_alive():
        data_thread.join(0.5)
    if play_thread and play_thread.is_alive():
        play_thread.join(0.5)

    # 重置线程变量
    data_thread = None
    play_thread = None


def modify_audio(data):
    global f, filter_coeffs, filter_states
    if not filter_coeffs:  # 如果没有滤波器系数，直接返回原始数据
        return data

    y_arr = np.zeros_like(data)

    for idx, (b, a) in enumerate(filter_coeffs):
        # 确保状态变量维度正确
        if filter_states[idx] is None:
            # 初始化滤波器状态
            zi = signal.lfilter_zi(b, a)
            if zi.ndim > 0:
                filter_states[idx] = np.zeros_like(zi)
            else:
                filter_states[idx] = np.zeros(1)

        # 应用滤波器
        if filter_states[idx].size > 0:
            z, filter_states[idx] = signal.lfilter(b, a, data, zi=filter_states[idx])
        else:
            z = signal.lfilter(b, a, data)

        # 应用增益
        values = int(scales[idx].get())
        mutiple = 10 ** (values / 20)
        y_arr += z * mutiple

    # 归一化防止削波
    max_val = np.max(np.abs(y_arr))
    if max_val > 1.0:
        y_arr = y_arr / max_val

    return y_arr


# ==创建窗口===============================
root = tk.Tk()
root.geometry("1000x500")
root.config(background='#dbeded')
root.title('数字均衡器')

# ==插入播放按钮======================
play_btn = tk.Button(root, text="播放", bg="#003355", font=12, fg='white', command=play)
play_btn.place(x=10, y=20, width=120, height=32)

# ==插入停止按钮========================
stop_btn = tk.Button(root, text="停止", bg="#003355", font=12, fg='white', command=stop)
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
chart, ax= wg.getfigure1(root, 10, 300, 950, 190)

# ==显示窗口=================================
root.mainloop()