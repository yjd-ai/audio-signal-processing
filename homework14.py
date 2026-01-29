import tkinter as tk
from tkinter import ttk
import numpy as np
import myPackage.widget as wg
import myPackage.signal as sg

# ==初始化参数=============================
Fs=2048;
N=512
t = np.arange(N) / Fs
A = 1
P = 0
_, y1 = sg.sinGenerator(Fs, N, A, 50, P)
_, y2 = sg.cosGenerator(Fs, N, A, 200, P)
_, y3 = sg.cosGenerator(Fs, N, A, 500, P)
y = y1 + y2 + y3

def draw_ax12():
    global t, y, Fs
    ax1.plot(t, y, color = "yellow")
    chart.draw()

def draw_ax34():
    global t, y, Fs
    ax2.clear()
    ax2.grid()
    LF = float(LF_entry_var.get())
    HF = float(HF_entry_var.get())
    M = int(M_entry_var.get())
    data = sg.FIR_python(M, LF, HF, Fs, y)
    ax2.plot(t, data, color="yellow")
    y4, A = sg.FIR_own(M, LF, HF, Fs, y, combo.current())
    f, A1 = sg.AmplitudeSpetrum(N, Fs, y4)
    ax3.clear()
    ax4.clear()
    ax3.grid()
    ax4.grid()
    ax3.plot(A, color = "yellow")
    ax4.plot(t, y4, color = "yellow")
    chart.draw()

# ==创建窗口===============================
root = tk.Tk()
root.geometry("1000x700")
root.config(background='#dbeded')
root.title('FIR滤波器')

# 插入Matplotlib图表 ==============
chart, ax1, ax2, ax3, ax4 = wg.getfigure4(root, 30, 60, 950, 630)
draw_ax12()

#==插入截取窗选择下拉控件===================
options = ["矩形窗", "巴特利特窗", "汉宁窗", "汉明窗", "布莱克曼窗", "平顶窗"]
combo = ttk.Combobox(root, values=options)
combo.set("矩形窗")
combo.place(x=900,y=20,width=80,height=32)

#插入截取频率范围框===============================
LF_label = tk.Label(root, text="频率下限：", font=8, bg = '#dbeded', fg="black")
LF_label.place(x=20, y=20)
LF_entry_var = tk.StringVar(value='1')
LF_entry = tk.Entry(root, textvariable=LF_entry_var, background="white", fg="black", justify=tk.CENTER)
LF_entry.place(x=110, y=15, width=40, height=32)

HF_label = tk.Label(root, text="频率上限：", font=8, bg = '#dbeded', fg="black")
HF_label.place(x=150, y=20)
HF_entry_var = tk.StringVar(value='100')
HF_entry = tk.Entry(root, textvariable=HF_entry_var, background="white", fg="black", justify=tk.CENTER)
HF_entry.place(x=240, y=15, width=40, height=32)

#插入阶数输入=========================
M_label = tk.Label(root, text="点数(M)：", font=8, bg = '#dbeded', fg="black")
M_label.place(x=300, y=20)
M_entry_var = tk.StringVar(value='51')
M_entry = tk.Entry(root, textvariable=M_entry_var, background="white", fg="black", justify=tk.CENTER)
M_entry.place(x=380, y=15, width=40, height=32)

#插入滤波按钮=========================
filter_btn = tk.Button(root, text="滤波", bg="#ebe9d5", font=8, fg='black', anchor='center', command=draw_ax34)
filter_btn.place(x=500, y=15, width=280, height=32)

# ==显示窗口=================================
root.mainloop()