import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
import numpy as np
import myPackage.signal as sg

#==自定义函数===============================
def init_():
    global Fs, t1, t2, y1, y2, coef1, coef2, freqs1, freqs2, coef3, coef4, freqs3, freqs4
    Fs = 3000
    N = 3000
    N1 = int(N / 3)
    _, x1 = sg.sinGenerator(Fs, N1, 1, 100, 0)
    _, x2 = sg.sinGenerator(Fs, N1, 1, 200, 0)
    _, x3 = sg.sinGenerator(Fs, N1, 1, 800, 0)
    y1 = np.concatenate([x1, x2, x3])
    t1 = np.arange(len(y1)) / Fs
    t2 = np.arange(N) / Fs
    f = 100 * t2 + 100
    y2 = np.sin(2 * np.pi * f * t2)

    coef1, freqs1 = sg.cwt_python(y1, Fs, 'morl')
    coef2, freqs2 = sg.cwt_python(y2, Fs, 'morl')
    coef3, freqs3 = sg.cwt_own(y1, Fs, 'morl')
    coef4, freqs4 = sg.cwt_own(y2, Fs, 'morl')

def getfigure(win, x0, y0, w, h):
    px=1/plt.rcParams['figure.dpi']
    fig=plt.Figure(figsize=(w * px, h*px))
    #fig.patch.set_facecolor('#cdcdcd')
    chart=FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x = x0, y = y0)
    gs = GridSpec(2, 2, figure=fig, height_ratios=[1, 3], width_ratios=[1, 1])
    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])
    fig.tight_layout()
    return chart, ax1, ax2, ax3

def drawFunc(val):
    ax1.clear()
    ax2.clear()
    ax3.clear()
    if val == 1:
        t, y, coef, freqs = t1, y1, coef1, freqs1
        coef_, freqs_ = coef3, freqs3
    else:
        t, y, coef, freqs,  = t2, y2, coef2, freqs2
        coef_, freqs_ = coef4, freqs4
    ax1.plot(t, y)
    ax2.pcolormesh(t, freqs, abs(coef))
    ax2.set_ylim(0, 1200)
    #t3, z = mortlet(1, 3000)
    #ax3.plot(t3, z)
    ax3.pcolormesh(t, freqs_, abs(coef_))
    ax3.set_ylim(0, 1200)
    chart.draw_idle()

#=========回调函数================
def drawdf():
    drawFunc(1)

def drawsf():
    drawFunc(2)

#========插入主窗口===========================
root = tk.Tk()
root.geometry("800x480")
root.config(background="#cdcdcd")
root.title("连续小波变换")

#=======插入matplotlib=======================
chart, ax1, ax2, ax3 = getfigure(root,-2,-10,680,500)

#==========插入多频信号按钮=================
df_btn = tk.Button(root, text="多频信号", bg="skyblue", font=12, fg='black', command=drawdf)
df_btn.place(x=680, y=100, width=100, height=32)

#==========插入扫频信号按钮=================
sf_btn = tk.Button(root, text="扫频信号", bg="skyblue", font=12, fg='black',command=drawsf)
sf_btn.place(x=680, y=200, width=100, height=32)

#===初始化参数===============================
init_()

#=======主窗口循环==============================
root.mainloop()