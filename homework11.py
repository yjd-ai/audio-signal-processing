import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import myPackage.widget as wg
import myPackage.signal as sg

#==初始化参数===================
Fs, N, d, generator_type = 44100, 1000, 0.5, 0

# 自定义函数===================
def getfigure(win, x0, y0, w, h):
    px=1/plt.rcParams['figure.dpi']
    fig=plt.Figure(figsize=(w * px, h*px))
    chart=FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x = x0, y = y0)
    plt.rcParams["font.family"] = ["SimSun"]
    plt.rcParams['axes.unicode_minus'] = False
    ax1 = fig.add_subplot(311)
    ax1.set_title('信号')
    ax2 = fig.add_subplot(312)
    ax2.set_title('基于FFT的相关曲线')
    ax3 = fig.add_subplot(313)
    ax3.set_title('标准算法的相关曲线')
    fig.tight_layout()
    return chart, ax1, ax2, ax3

def drawFunc():
    global Fs, N, d, P, generator_type, digital_signal
    A = knob_A.get_value()
    F = knob_F.get_value()
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
    tt1, cc1 = sg.fftCorr(Fs, N, y, y, 1)
    tt2, cc2 = sg.doCorr(Fs, N, y, y, 1)
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax1.set_title('信号')
    ax1.set_ylim(-1.2, 1.2)
    ax1.plot(t, y)
    ax2.set_title('基于FFT的相关曲线')

    ax2.plot(tt1, cc1)
    ax3.set_title('标准算法的相关曲线')
    #ax3.set_ylim(-1.2, 1.2)
    ax3.plot(tt2, cc2)

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

def reset_param(value):
    drawFunc()

# 建立tkinter GUI 窗口==============
root = tk.Tk()
root.geometry('1000x700')
root.config(bg = '#dbeded')
root.wm_title('相关曲线')

# 插入MatplotlibCurve ==============
chart, ax1, ax2, ax3 = getfigure(root,50,10,700,650)

#==插入信号选择按钮====================
sin_btn = tk.Button(root, text = '正弦波', bg = "white", font = 12, fg = 'black', command = sinFunc)
sin_btn.place(x=800,y=20,width=120,height=32)

square_btn = tk.Button(root, text = '方波', bg = "white", font = 12, fg = 'black', command = squareFunc)
square_btn.place(x=800,y=82,width=120,height=32)

saw_btn = tk.Button(root, text = '三角波', bg = "white", font = 12, fg = 'black', command = sawFunc)
saw_btn.place(x=800,y=144,width=120,height=32)

noise_btn = tk.Button(root, text = '白噪声', bg = "white", font = 12, fg = 'black', command = noiseFunc)
noise_btn.place(x=800, y=206, width=120, height=32)

# 插入旋钮 ============================
knob_A = wg.Knob(root, min_val = 0, max_val = 1, size = 100, x = 800, y = 350,
                 text = "幅值", command = reset_param, color = "#40bbc4")
knob_F = wg.Knob(root, min_val = 100, max_val = 2000, size = 100, x = 800, y = 500,
                 text = "频率", command = reset_param, color = "#40bbc4")

#=Tkinter主窗口循环控制==============
root.mainloop()