import tkinter as tk
import matplotlib.pyplot as plt
import myPackage.signal as sg
import myPackage.widget as wg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#==初始化参数===================
Fs, N, A, P, d, generator_type  = 1024, 1024, 1, 0, 0.5, -1
win, signal_button, win_button, graph = [] , [], [], []
signal_button_name = ["正弦波", "方波", "三角波", "白噪声"]
win_button_name = ["矩形窗", "巴特利特窗", "汉宁窗", "汉明窗", "布莱克曼窗", "平顶窗"]
title = ["时域波形图", "加窗的波形图", "幅频谱图"]
#==自定义函数==================
def drawFunc():
    F = knob_F.get_value()
    if(0 == generator_type):    t, y = sg.sinGenerator(Fs,N,A,F,P)
    elif (1 == generator_type): t, y = sg.squareGenerator(Fs, N, A, F, P, d)
    elif (2 == generator_type): t, y = sg.sawGenerator(Fs, N, A, F, P, d)
    elif (3 == generator_type): t, y = sg.noiseGenerator(Fs, N, A)
    else:return
    for i in range(3):
        graph[i][1].clear()
        graph[i][1].grid()
        graph[i][1].set_title(title[i])
    graph[0][1].plot(t, y)
    graph[0][0].draw()
    if len(win) > 0:
        y = y * win
        graph[1][1].plot(t, y)
        graph[1][0].draw()
    f, yA = sg.AmplitudeSpetrum(N, Fs, y)
    graph[2][1].plot(f, yA)
    graph[2][0].draw()

#==控件回调函数=================
def signalGenerator(idx):
    global generator_type
    generator_type = idx
    drawFunc()

def winFunc(idx):
    global win
    win = sg.winFunction(idx, N)
    drawFunc()

def reset_param(value):
    drawFunc()

# 信号显示框
def getfigure(win, x0, y0, w, h):
    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.Figure(figsize=(w * px, h * px))
    fig.subplots_adjust(left=0.07, bottom=0.15, right=0.98, top=0.8, wspace=0, hspace=0)
    chart = FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x=x0, y=y0)
    ax = fig.add_subplot(111)
    ax.grid()
    return chart, ax

# 建立tkinter GUI 窗口==============
root = tk.Tk()
root.geometry('800x700')
root.config(bg = "#dbeded")
root.wm_title('加窗及傅里叶变换')

#==插入信号选择按钮====================
for i in range(4):
    btn = tk.Button(root, text = signal_button_name[i], bg = "#13ce66", font = 12, fg = 'blue',
                    command = lambda idx = i: signalGenerator(idx))
    btn.place(x=660, y=20 + i * 32, width=120, height=32)
    signal_button.append(btn)


#==插入窗口选择按钮====================
for i in range(6):
    btn = tk.Button(root, text=win_button_name[i], bg="#efac4d", font=12, fg='blue', command = lambda idx = i : winFunc(idx))
    btn.place(x=660, y = 200 + i * 32, width=120, height=32)
    win_button.append(btn)

#==插入旋钮控件===========================
knob_F = wg.Knob(root, min_val = 0, max_val = 100, size = 100, x = 670, y = 400,color = "#c0e4fa", text = "频率", command = reset_param)

# 插入信号显示框==============
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
for i in range(3):
    chart, ax = getfigure(root, 10,20 + i * 220, 630,200)
    ax.set_title(title[i])
    graph.append([chart, ax])
#=Tkinter主窗口循环控制==============
root.mainloop()