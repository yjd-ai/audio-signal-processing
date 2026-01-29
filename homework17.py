import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import myPackage.signal as sg
import myPackage.widget as wg

#======自定义函数============================
def getfigure6(win, x0, y0, w, h):
    def set_axes_style(ax):
        ax.set_facecolor('white')
        ax.spines['top'].set_linestyle('--')
        ax.spines['top'].set_alpha(0.4)
        ax.yaxis.set_visible(False)
        ax.xaxis.set_visible(False)
    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.Figure(figsize=(w * px, h * px))
    fig.patch.set_facecolor('#E2EAF4')
    fig.subplots_adjust(left=0.1,right=0.9,bottom=0.1,top=0.9,hspace=0)
    chart = FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x=x0, y=y0)
    ax1 = fig.add_subplot(611)
    ax2 = fig.add_subplot(612, sharex=ax1)
    ax3 = fig.add_subplot(613, sharex=ax1)
    ax4 = fig.add_subplot(614, sharex=ax1)
    ax5 = fig.add_subplot(615, sharex=ax1)
    ax6 = fig.add_subplot(616, sharex=ax1)
    set_axes_style(ax1)
    set_axes_style(ax2)
    set_axes_style(ax3)
    set_axes_style(ax4)
    set_axes_style(ax5)
    set_axes_style(ax6)
    ax1.spines['top'].set_linestyle('-')
    ax1.spines['top'].set_alpha(1)
    ax6.xaxis.set_visible(True)
    return chart, ax1, ax2, ax3, ax4, ax5, ax6

def drawFunc(x):
    N = 1000
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()
    ax6.clear()
    d, a = sg.LT53(x)
    ad, aa = sg.LT53(a)
    aad, aaa = sg.LT53(aa)
    aa1 = sg.ILT53(aad, aaa)
    a1 = sg.ILT53(ad, aa1)
    y = sg.ILT53(d, a1)
    ax1.plot(x)
    ax1.set_xlim(0, N)
    ax2.plot(d)
    ax2.set_xlim(0, N)
    ax3.plot(ad)
    ax3.set_xlim(0, N)
    ax4.plot(aad)
    ax4.set_xlim(0, N)
    ax5.plot(aaa)
    ax5.set_xlim(0, N)
    ax6.plot(y)
    ax6.set_xlim(0, N)
    chart.draw()

def signal_1():
    Fs = 5120
    t = np.arange(350) * (1 / Fs)
    x1 = np.sin(2 * np.pi * 100 * t)
    x2 = np.sin(2 * np.pi * 1000 * t)
    x3 = np.sin(2 * np.pi * 2 * 2000 * t)
    x = np.concatenate([x1, x2, x3])
    drawFunc(x)

def signal_2():
    Fs = 5120
    t = np.arange(1000) * (1 / Fs)
    f = 3000 * t + 100
    x = np.sin(2 * np.pi * 2 * f * t)
    drawFunc(x)

#========插入主窗口===========================
root = tk.Tk()
root.geometry("800x480")
root.config(background="#E2EAF4")
root.title("小波包变换")

#=======插入matplotlib=======================
chart, ax1, ax2, ax3, ax4, ax5, ax6 = getfigure6(root,-85,-10,965,510)

#======插入按钮================================
mf_btn = tk.Button(root, text="多频信号", bg="#EFD8B7", font=12, fg='black', command=signal_1)
mf_btn.place(x=250, y=0, width=120, height=40)

#======插入按钮================================
sf_btn = tk.Button(root, text="扫频信号", bg="#EFD8B7", font=12, fg='black', command=signal_2)
sf_btn.place(x=430, y=0, width=120, height=40)

#=======主窗口循环==============================
root.mainloop()