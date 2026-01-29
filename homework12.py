import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import myPackage.signal as sg

#==初始化参数===================
Fs, N, A, F, d, generator_type = 44100, 4096, 1, 400, 0.5, 0

# 自定义函数===================
def getfigure(win, x0, y0, w, h):
    px=1/plt.rcParams['figure.dpi']
    fig=plt.Figure(figsize=(w * px, h*px))
    plt.rcParams["font.family"] = ["SimSun"]
    plt.rcParams['axes.unicode_minus'] = False
    chart=FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x = x0, y = y0)
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(323)
    ax3 = fig.add_subplot(324)
    ax4 = fig.add_subplot(325)
    ax5 = fig.add_subplot(326)
    ax1.set_title('标准信号')
    ax2.set_title('概率密度--自定义函数')
    ax3.set_title('分布曲线--自定义函数')
    ax4.set_title('概率密度--python库函数')
    ax5.set_title('分布曲线--python库函数')
    fig.tight_layout()
    return chart, ax1, ax2, ax3, ax4, ax5

def drawFunc():
    global Fs, N, d, P, generator_type, digital_signal
    if (1 == generator_type):
        t, y = sg.sinGenerator(Fs, N, A, F, 0)
    elif (2 == generator_type):
        t, y = sg.squareGenerator(Fs, N, A, F, 0, d)
    elif (3 == generator_type):
        t, y = sg.sawGenerator(Fs, N, A, F, 0, d)
    elif (4 == generator_type):
        t, y = sg.noiseGenerator(Fs, N, A)
    else:
        return
    x1, p1, c1 = sg.doPdfCdf_own(N, y, 50, -1, 1)
    x2, p2, c2 = sg.doPdfCdf(N, y, 50, -1, 1)
    ax1.clear(); ax2.clear(); ax3.clear(); ax4.clear(); ax5.clear()
    ax1.set_title('标准信号')
    ax2.set_title('概率密度--自定义函数')
    ax3.set_title('分布曲线--自定义函数')
    ax4.set_title('概率密度--python库函数')
    ax5.set_title('分布曲线--python库函数')
    ax1.plot(t, y)
    ax2.plot(x1, p1)
    ax3.plot(x1, c1)
    ax4.plot(x2, p2)
    ax5.plot(x2, c2)
    chart.draw()


# 回调函数 ==========================
def sinFunc():
    global generator_type
    generator_type = 1
    drawFunc()

def squareFunc():
    global generator_type
    generator_type = 2
    drawFunc()

def sawFunc():
    global generator_type
    generator_type = 3
    drawFunc()

def noiseFunc():
    global generator_type
    generator_type = 4
    drawFunc()

# 建立tkinter GUI 窗口==============
root = tk.Tk()
root.geometry('1000x700')
root.config(bg = '#dbeded')
root.wm_title('相关曲线')

# 插入MatplotlibCurve ==============
chart, ax1, ax2, ax3, ax4, ax5 = getfigure(root,50,10,700, 700)

#==插入信号选择按钮====================
sin_btn = tk.Button(root, text = '正弦波', bg = "white", font = 12, fg = 'black', command = sinFunc)
sin_btn.place(x=800,y=100,width=120,height=32)

square_btn = tk.Button(root, text = '方波', bg = "white", font = 12, fg = 'black', command = squareFunc)
square_btn.place(x=800,y=200,width=120,height=32)

saw_btn = tk.Button(root, text = '三角波', bg = "white", font = 12, fg = 'black', command = sawFunc)
saw_btn.place(x=800,y=300,width=120,height=32)

noise_btn = tk.Button(root, text = '白噪声', bg = "white", font = 12, fg = 'black', command = noiseFunc)
noise_btn.place(x=800, y=400, width=120, height=32)

#=Tkinter主窗口循环控制==============
root.mainloop()