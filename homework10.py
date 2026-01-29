import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import librosa
import numpy as np
# 自定义函数===================
def getfigure(win, x0, y0, w, h):
    px=1/plt.rcParams['figure.dpi']
    fig=plt.Figure(figsize=(w * px, h*px))
    chart=FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x = x0, y = y0)
    ax=fig.add_subplot(111)
    fig.tight_layout()
    return chart, ax, fig

# 回调函数 ==========================
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

#查看语谱图
def show():
    file_path = file_entry_var.get()
    if file_path:
        ax.clear()
        data, Fs = librosa.load(file_path, sr=44100, mono=True)  # mono=True 转为单声道
        S = librosa.feature.melspectrogram(y=data, sr=Fs, n_mels=64, fmax=8000, n_fft=2048, hop_length=512)
        S_dB = librosa.power_to_db(S, ref=np.max)
        img = librosa.display.specshow(S_dB, ax=ax, sr=Fs, x_axis='time', y_axis='mel', fmax=8000)
        fig.colorbar(img, ax=ax, format="%+2.f dB", shrink=0.8)
        #ax.set_title('梅尔语谱图')
        plt.tight_layout()
        chart.draw()

# 建立tkinter GUI 窗口==============
root = tk.Tk()
root.geometry('800x480')
root.config(bg = '#dbeded')
root.wm_title('梅尔语谱图')

# ==插入查看按钮======================
play_btn = tk.Button(root, text="查看", bg="#ebe9d5", font=12, fg='black', command = show)
play_btn.place(x=10, y=20, width=120, height=32)

# ==插入文件按钮================================
file_btn = tk.Button(root, text="文件", bg="#ebe9d5", font=12, fg='black', command=open_file)
file_btn.place(x=150, y=20, width=120, height=32)

# ==文件路径编辑框=======================
file_entry_var = tk.StringVar()
file_entry = tk.Entry(root, textvariable=file_entry_var)
file_entry.place(x=300, y=20, width=470, height=32)

# 插入MatplotlibCurve ==============
chart, ax, fig = getfigure(root,50,80,700,350)

#=Tkinter主窗口循环控制==============
root.mainloop()