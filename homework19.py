import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PyEMD import EMD, EEMD, CEEMDAN
from PyLMD import LMD

#======自定义函数================
y = None
def getfigure(win, x0, y0, w, h):
    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.Figure(figsize=(w * px, h * px))
    fig.patch.set_facecolor('#E2EAF4')
    fig.subplots_adjust(left=0.1,right=0.9,bottom=0.1,top=0.9,hspace=0)
    chart = FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x=x0, y=y0)
    ax = fig.add_subplot(111)
    #ax.yaxis.set_visible(False)
    #ax.xaxis.set_visible(False)
    return chart, ax

def EMDFunc():
    global y
    if y is None:
        return
    emd = EMD()
    IMF = emd(y)
    N = IMF.shape[0]
    fig, ax1 = plt.subplots(nrows=1, ncols=1)
    S = np.zeros_like(IMF[0])
    for i in range(N):
        S += IMF[i]
        ax1.plot(IMF[i] - 5 * (i))
    ax1.plot(S - 5 * N)
    ax1.set_title("EMD")
    plt.show()

def LMDFunc():
    global y
    if y is None:
        return
    lmd = LMD()
    IMF,_ = lmd.lmd(y)
    N = IMF.shape[0]
    fig, ax1 = plt.subplots(nrows=1, ncols=1)
    S = np.zeros_like(IMF[0])
    for i in range(N):
        S += IMF[i]
        ax1.plot(IMF[i] - 5 * (i))
    ax1.plot(S - 5 * N)
    ax1.set_title("LMD")
    plt.show()

def EEMDFunc():
    global y
    if y is None:
        return
    eemd = EEMD()
    IMF = eemd(y)
    N = IMF.shape[0]
    fig, ax1 = plt.subplots(nrows=1, ncols=1)
    S = np.zeros_like(IMF[0])
    for i in range(N):
        S += IMF[i]
        ax1.plot(IMF[i] - 5 * (i))
    ax1.plot(S - 5 * N)
    ax1.set_title("EEMD")
    plt.show()

def CEEMDANFunc():
    global y
    if y is None:
        return
    ceemdan = CEEMDAN()
    IMF = ceemdan(y)
    N = IMF.shape[0]
    fig, ax1 = plt.subplots(nrows=1, ncols=1)
    S = np.zeros_like(IMF[0])
    for i in range(N):
        S += IMF[i]
        ax1.plot(IMF[i] - 5 * (i))
    ax1.plot(S - 5 * N)
    ax1.set_title("CEEMDAN")
    plt.show()

def signal1():
    global y
    fs = 1000
    t = np.arange(0, 1, 1 / fs)
    part1 = 8 * t ** 2
    part2 = np.cos(4 * np.pi * t + 10 * np.pi * t ** 2)
    part3 = np.zeros_like(t)
    mask1 = t <= 0.5
    part3[mask1] = np.cos(60 * np.pi * t[mask1])
    mask2 = t > 0.5
    part3[mask2] = np.cos(200 * np.pi * (t[mask2] - 0.5))
    x = part1 + part2 + part3
    n = np.random.randn(len(t))
    y = x + 0.1 * n
    ax.clear()
    ax.plot(t, y)
    chart.draw()

def signal2():
    global y
    Fs = 400
    t = np.arange(0, 0.75 + 1 / Fs, 1 / Fs)
    y1 = np.sin(2 * np.pi * 4 * t)
    y2 = 0.5 * np.sin(2 * np.pi * 120 * t)
    for i in range(len(t)):
        if (t[i] % 0.25 > 0.11) and (t[i] % 0.25 < 0.12):
            pass
        else:
            y2[i] = 0
    y = y1 + y2
    ax.clear()
    ax.plot(t, y)
    chart.draw()

def signal3():
    global y
    N = 512
    T = 1.0
    Fs = N / T
    t = np.arange(N) / Fs
    noise_power = 0.1
    x1 = np.random.normal(0, np.sqrt(noise_power), N)
    x2 = np.sin(2 * np.pi * 50 * t)
    y = x1 + x2
    ax.clear()
    ax.plot(t, y)
    chart.draw()

def signal4():
    global y
    Fs = 400
    T = 10
    N = Fs * T
    t = np.arange(N) / Fs
    y = np.sin(2 * np.pi * (10*t+10) * t)
    ax.clear()
    ax.plot(t, y)
    chart.draw()

#========插入主窗口===========================
root = tk.Tk()
root.geometry("800x480")
root.config(background="#E2EAF4")
root.title("希尔伯特-黄变换")

#========插入matplotlib=====================
chart, ax = getfigure(root, -30, 35, 880, 450)

#========插入分解按钮====================
EMD_btn = tk.Button(root, text = "EMD", bg="#ffe4b0", font=12, fg='black', command=EMDFunc)
EMD_btn.place(x=580, y=5, width=80, height=32)

LMD_btn = tk.Button(root, text = "LMD", bg="#ffe4b0", font=12, fg='black', command=LMDFunc)
LMD_btn.place(x=580, y=45, width=80, height=32)

EEMD_btn = tk.Button(root, text = "EEMD", bg="#ffe4b0", font=12, fg='black', command=EEMDFunc)
EEMD_btn.place(x=680, y=5, width=80, height=32)

CEEMDAN_btn = tk.Button(root, text = "CEEMDAN", bg="#ffe4b0", font=12, fg='black', command=CEEMDANFunc)
CEEMDAN_btn.place(x=680, y=45, width=80, height=32)

#=========插入信号按钮===================
signal1_btn = tk.Button(root, text = "signal_1", bg="#ffe4b0", font=12, fg='black', command=signal1)
signal1_btn.place(x=60, y=5, width=90, height=42)
#signal2_btn = tk.Button(root, text = "signal_2", bg="#ffe4b0", font=12, fg='black')
#signal2_btn.place(x=60, y=45, width=90, height=32)

signal3_btn = tk.Button(root, text = "signal_2", bg="#ffe4b0", font=12, fg='black', command=signal2)
signal3_btn.place(x=160, y=5, width=90, height=42)
signal4_btn = tk.Button(root, text = "signal_4", bg="#ffe4b0", font=12, fg='black', command=signal4)
signal4_btn.place(x=360, y=5, width=90, height=42)

signal5_btn = tk.Button(root, text = "signal_3", bg="#ffe4b0", font=12, fg='black', command=signal3)
signal5_btn.place(x=260, y=5, width=90, height=42)
#signal6_btn = tk.Button(root, text = "signal_6", bg="#ffe4b0", font=12, fg='black')
#signal6_btn.place(x=260, y=45, width=90, height=32)

#========主窗口循环=====================
root.mainloop()