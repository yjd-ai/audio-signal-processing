import tkinter as tk
from tkinter import filedialog
import librosa
import numpy as np
from sklearn.decomposition import FastICA
import simpleaudio as sa
import threading
import myPackage.widget as wg
import myPackage.signal as sg

#======初始化参数====================
y11 = None
y12 = None
y13 = None
X = None
SE = None
Fs = 44100
play_obj = None
is_playing1 = False
is_playing2 = False
is_playing3 = False
#====自定义函数======================
def open_file():
    file_types = [
        ("音视频文件", "*.mp3; *.wav; *.mp4")
    ]
    file_path = filedialog.askopenfilename(
        title="选择音视频文件",
        filetypes=file_types,
        initialdir="."
    )
    return file_path

def mixed_seperate():
    global y11, y12, y13, X, SE
    if y11 is None or y12 is None or y13 is None:
        return
    max_len = max(len(y11), len(y12), len(y13))
    y11_pad = np.pad(y11, (0, max_len - len(y11)), mode='constant')
    y12_pad = np.pad(y12, (0, max_len - len(y12)), mode='constant')
    y13_pad = np.pad(y13, (0, max_len - len(y13)), mode='constant')
    Y = np.c_[y11_pad, y12_pad, y13_pad]
    Y /= Y.std(axis=0)
    A = np.array([
        [0.7, 0.3, 0.2],
        [0.2, 0.6, 0.3],
        [0.3, 0.2, 0.8]
    ])
    X = np.dot(Y, A.T)
    X = X / np.max(np.abs(X), axis=0)
    ica = FastICA(n_components=3)
    SE = ica.fit_transform(X)
    SE = SE / np.max(np.abs(SE), axis=0)

def show(y1,index,ax, signal_var):
    global X, SE, Fs
    ax.clear()
    val = signal_var.get()
    if val == "original":
        if y1 is not None:
            t = np.arange(len(y1)) / Fs
            ax.plot(t, y1)
    elif val == "mixed":
        if X is not None:
            y = X[:,index]
            t = np.arange(len(y)) / Fs
            ax.plot(t,y)
    elif val == "separated":
        if SE is not None:
            y = SE[:, index]
            t = np.arange(len(y)) / Fs
            ax.plot(t, y)
    ax.grid()
    chart.draw_idle()

def play_audio(data, sr, is_playing, btn):
    global play_obj
    normalized_signal = sg.normalize(data)
    audio_data = (normalized_signal * 32767).astype(np.int16)
    play_obj = sa.play_buffer(audio_data, 1, 2, sr)
    play_obj.wait_done()
    is_playing = False
    play_audio = None
    btn.config(text = "▶")

def wav(signal_var, index, y1):
    val = signal_var.get()
    y = None
    if val == "original":
        if y1 is not None:
            y = y1
    elif val == "mixed":
        if X is not None:
            y = X[:, index]
    elif val == "separated":
        if SE is not None:
            y = SE[:, index]
    return y

#=============回调函数======================
def file1():
    global y11, Fs
    file_path = open_file()
    if file_path:
        y11, _ = librosa.load(file_path, sr=Fs, mono=True)
        signal1_var.set("original")
        show(y11,0,ax1, signal1_var)
        mixed_seperate()

def file2():
    global y12, Fs
    file_path = open_file()
    if file_path:
        y12, _ = librosa.load(file_path, sr=Fs, mono=True)
        signal2_var.set("original")
        show(y12,0,ax2, signal2_var)
        mixed_seperate()

def file3():
    global y13, Fs
    file_path = open_file()
    if file_path:
        y13, _ = librosa.load(file_path, sr=Fs, mono=True)
        mixed_seperate()
        signal3_var.set("original")
        show(y13,0,ax3, signal3_var)

def play1():
    global y11, Fs, is_playing1, is_playing2, is_playing3, play_obj,signal1_var
    if is_playing2 or is_playing3:
        return
    y = wav(signal1_var,0,y11)
    if is_playing1:
        play_obj.stop()
        play_obj = None
        is_playing1 = False
        play1_btn.config(text="▶")
        return
    if y is None:
        return
    is_playing1 = True
    play1_btn.config(text="◾")
    threading.Thread(target=play_audio,args=(y, Fs, is_playing1, play1_btn),daemon=True).start()
def play2():
    global y12, Fs, is_playing1, is_playing2, is_playing3, play_obj,signal2_var
    if is_playing1 or is_playing3:
        return
    y = wav(signal2_var, 1, y12)
    if is_playing2:
        play_obj.stop()
        play_obj = None
        is_playing2 = False
        play2_btn.config(text="▶")
        return
    if y is None:
        return
    is_playing2 = True
    play2_btn.config(text="◾")
    threading.Thread(target=play_audio, args=(y, Fs, is_playing2, play2_btn), daemon=True).start()

def play3():
    global y13, Fs, is_playing1, is_playing2, is_playing3, play_obj, signal3_var
    if is_playing1 or is_playing2:
        return
    y = wav(signal3_var, 2, y13)
    if is_playing3:
        play_obj.stop()
        play_obj = None
        is_playing3 = False
        play3_btn.config(text="▶")
        return
    if y is None:
        return
    is_playing3 = True
    play3_btn.config(text="◾")
    threading.Thread(target=play_audio, args=(y, Fs, is_playing3, play3_btn), daemon=True).start()

def show1():
    global y11,ax1,signal1_var
    show(y11,0,ax1,signal1_var)

def show2():
    global y12,ax2,signal2_var
    show(y12,1,ax2,signal2_var)

def show3():
    global y13,ax3,signal3_var
    show(y13,2,ax3,signal3_var)

def win_close():
    global play_obj
    if play_obj is not None:
        play_obj.stop()
        play_obj = None
    root.destroy()

#========插入主窗口===========================
root = tk.Tk()
root.geometry("800x480")
root.config(background="#E2EAF4")
root.title("盲源分离")
root.protocol("WM_DELETE_WINDOW", win_close)

#=====插入matplotlib========================
chart, ax1, ax2, ax3 = wg.getfigure3(root, 10, 10, 700, 450)

#===插入播放按钮=============================
play1_btn = tk.Button(root, text = "▶", bg="#409eff", font=12, fg='white',command=play1)
play1_btn.place(x=690, y=70, width=20, height=23)

play2_btn = tk.Button(root,text = "▶", bg="#409eff", font=12, fg='white',command=play2)
play2_btn.place(x=690, y=220, width=20, height=23)

play3_btn = tk.Button(root,text = "▶", bg="#409eff", font=12, fg='white',command=play3)
play3_btn.place(x=690, y=370, width=20, height=23)

#===插入文件按钮=============================
file1_btn = tk.Button(root,text = "音频1", bg="#409eff", font=12, fg='white', command=file1)
file1_btn.place(x=330, y=150, width=80, height=20)

file2_btn = tk.Button(root,text = "音频2", bg="#409eff", font=12, fg='white', command=file2)
file2_btn.place(x=330, y=295, width=80, height=20)

file3_btn = tk.Button(root,text = "音频3", bg="#409eff", font=12, fg='white', command=file3)
file3_btn.place(x=330, y=435, width=80, height=20)

#===插入选择框=================================
signal1_var = tk.StringVar()
signal1_var.set("original")
rb11 = tk.Radiobutton(root, text="原始", variable=signal1_var, value="original", anchor="w", command=show1)
rb12 = tk.Radiobutton(root, text="混合", variable=signal1_var, value="mixed", anchor="w",command=show1)
rb13 = tk.Radiobutton(root, text="分离", variable=signal1_var, value="separated", anchor="w",command=show1)
rb11.place(x=720, y=15, width=60, height=20)
rb12.place(x=720, y=55, width=60, height=20)
rb13.place(x=720, y=95, width=60, height=20)

signal2_var = tk.StringVar()
signal2_var.set("original")
rb21 = tk.Radiobutton(root, text="原始", variable=signal2_var, value="original", anchor="w",command=show2)
rb22 = tk.Radiobutton(root, text="混合", variable=signal2_var, value="mixed", anchor="w",command=show2)
rb23 = tk.Radiobutton(root, text="分离", variable=signal2_var, value="separated", anchor="w",command=show2)
rb21.place(x=720, y=175, width=60, height=20)
rb22.place(x=720, y=215, width=60, height=20)
rb23.place(x=720, y=255, width=60, height=20)

signal3_var = tk.StringVar()
signal3_var.set("original")
rb31 = tk.Radiobutton(root, text="原始", variable=signal3_var, value="original", anchor="w",command=show3)
rb32 = tk.Radiobutton(root, text="混合", variable=signal3_var, value="mixed", anchor="w",command=show3)
rb33 = tk.Radiobutton(root, text="分离", variable=signal3_var, value="separated", anchor="w",command=show3)
rb31.place(x=720, y=325, width=60, height=20)
rb32.place(x=720, y=365, width=60, height=20)
rb33.place(x=720, y=405, width=60, height=20)

#============主窗口循环=======================
root.mainloop()