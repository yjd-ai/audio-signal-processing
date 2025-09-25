import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import myPackage.signal as sg
import myPackage.widget as wg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#==初始化参数===================
Fs = 44100
N = 40000;
d = 0.5;
P = 0
generator_type = 0;
digital_signal = None
entry_var = []

#==自定义函数==================
def drawFunc():
    global Fs, N, d, P, generator_type, digital_signal
    A = knob_A.get_value()
    F = knob_F.get_value()
    if(1 == generator_type):
        t, y = sg.sinGenerator(Fs,N,A,F,P)
    elif (2 == generator_type):
        t, y = sg.squareGenerator(Fs, N, A, F, P, d)
    elif (3 == generator_type):
        t, y = sg.sawGenerator(Fs, N, A, F, P, d)
    elif (4 == generator_type):
        t, y = sg.noiseGenerator(Fs, N, A)
    else:
        return
    ax.clear()
    digital_signal = y;
    ax.grid(True, color='white', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlim(0, 0.02)
    ax.plot(t, y, color="yellow")
    chart.draw()
    f, Q, pp, R, std, M, kk = sg.signal_param(Fs, N, y)
    entry_var[0].set("频率:" +str(f))
    entry_var[1].set("峰峰值:" + str(pp))
    entry_var[2].set("有效值:" + str(R))
    entry_var[3].set("方差:" + str(std))
    entry_var[4].set("均值:" + str(M))
    entry_var[5].set("峭度:" + str(kk))

#==控件回调函数=================
# 定时器开关
def timeFunc(value):
    global P
    if (True == value):
        P += 10
        if(0 == P % 360):
            P = 0
        drawFunc()
        root.after(100, lambda : timeFunc(timer_switch.get_state()))

# 产生信号按钮
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

# 信号显示框
def getfigure(win, x0, y0, w, h):
    px=1/plt.rcParams['figure.dpi']
    fig=plt.Figure(figsize=(w * px, h*px))
    fig.patch.set_facecolor('blue')
    chart=FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x = x0, y = y0)
    ax=fig.add_subplot(111)
    ax.set_facecolor('black')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='both', colors='white')
    ax.grid(True, color='white', linestyle='--', linewidth=0.5, alpha=0.7)
    fig.tight_layout()
    return chart, ax

# 建立tkinter GUI 窗口==============
root = tk.Tk()
root.geometry('800x480')
root.config(bg = "#dbeded")
root.wm_title('信号发生器')

#==插入电源标签===========================
power_label = tk.Label(root, text = '定时', bg = '#dbeded', font = 12)
power_label.place(x=640,y=20,width=60,height=32)

#==插入定时开关===========================
timer_switch = wg.ToggleSwitch(root, x = 700, y = 20, command = timeFunc)

#==插入信号选择按钮====================
sin_btn = tk.Button(root, text = '正弦波', bg = "#0078d7", font = 12, fg = 'white', command = sinFunc)
sin_btn.place(x=650,y=70,width=120,height=32)

square_btn = tk.Button(root, text = '方波', bg = "#0078d7", font = 12, fg = 'white', command = squareFunc)
square_btn.place(x=650,y=102,width=120,height=32)

saw_btn = tk.Button(root, text = '三角波', bg = "#0078d7", font = 12, fg = 'white', command = sawFunc)
saw_btn.place(x=650,y=134,width=120,height=32)

noise_btn = tk.Button(root, text = '白噪声', bg = "#0078d7", font = 12, fg = 'white', command = noiseFunc)
noise_btn.place(x=650, y=166, width=120, height=32)

#==插入旋钮控件===========================
knob_A = wg.Knob(root, min_val = 0, max_val = 1, size = 100, x = 650, y = 200, text = "幅值", command = reset_param)
knob_F = wg.Knob(root, min_val = 100, max_val = 2000, size = 100, x = 650, y = 322, text = "频率", command = reset_param)

# 插入信号显示框==============
chart, ax = getfigure(root, 50,20, 550,400)

#==插入参数显示框=========================
for i in range(6):
    var = tk.StringVar()
    entry = tk.Entry(root, textvariable = var, state=tk.DISABLED)
    entry.place(x=10 + i * 110, y=430, width=100, height=32)
    entry_var.append(var)
#=Tkinter主窗口循环控制==============
root.mainloop()