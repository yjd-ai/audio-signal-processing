import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import myPackage.signal as sg
import statsmodels.api as sm
from scipy import signal

# ===========初始化参数================
N = 1000
Fs = 1000
y = None
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# ==========自定义函数==================
def getfigure(win, x0, y0, w, h):
    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.Figure(figsize=(w * px, h * px))
    fig.patch.set_facecolor('#E2EAF4')
    fig.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, hspace=0)
    chart = FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x=x0, y=y0)
    ax = fig.add_subplot(111)
    return chart, ax

def signal1():
    global Fs, N, y
    t = np.arange(N) / Fs
    f1, f2, f3 = 50, 60, 70
    y1 = np.sin(2 * np.pi * f1 * t)
    y2 = 0.8 * np.sin(2 * np.pi * f2 * t)
    y3 = 0.5 * np.sin(2 * np.pi * f3 * t)
    y_noise = 0.5 * np.random.randn(len(t))
    y = y1+y2+y3+y_noise
    ax.clear()
    ax.plot(t, y)
    chart.draw()

def drawFunc():
    global N, Fs, y
    if y is None:
        return
    f1, A1 = sg.AmplitudeSpetrum(N, Fs, y)
    res, err = sm.regression.linear_model.burg(y, order=256)
    ar = np.append(1, -res)
    w, h = signal.freqz(1, ar)
    fig, ax = plt.subplots(nrows=1, ncols=2)
    ax[0].plot(f1, A1)
    ax[0].set_title('fft')
    ax[1].plot((Fs/2)*(w/np.pi),abs(h))
    ax[1].set_title('高阶AR')
    plt.show()

# =======插入主窗口==================
root = tk.Tk()
root.geometry("800x480")
root.config(background="#E2EAF4")
root.title("稀疏采样")

# =====插入matplotlib====================
chart, ax = getfigure(root, -30, 35, 880, 450)

# =========插入信号按钮===================
signal_btn = tk.Button(root, text="生成信号", bg="#ffe4b0", font=12, fg='black', command=signal1)
signal_btn.place(x=60, y=15, width=90, height=42)

# =========插入fft按钮===================
draw_btn = tk.Button(root, text="频谱图", bg="#ffe4b0", font=12, fg='black', command=drawFunc)
draw_btn.place(x=160, y=15, width=90, height=42)

# =========主窗口循环=================
root.mainloop()