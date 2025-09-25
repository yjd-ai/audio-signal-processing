import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import myPackage.signal as sg
#==自定义函数==================
def drawFunc():
    A = float(amplitude_entry.get())
    P = float(phase_entry.get())
    F = float(frequency_entry.get())
    Fs = 44100
    N = 1000;
    t, y = sg.sinGenerator(Fs,N,A,F,P)
    ax.clear()
    ax.grid()
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlim(0, 0.02)
    ax.plot(t, y)
    chart.draw()

#==控件回调函数=================
def scalFunc(value, entry):
    entry.delete(0, tk.END)
    entry.insert(0, f"{float(value):.1f}")
    drawFunc()

def entryFunc(e, scale):
    value = float(e.widget.get())
    if scale['from'] <= value <= scale['to']:
        scale.set(value)
        drawFunc()

def getfigure(win, x0, y0, w, h):
    px=1/plt.rcParams['figure.dpi']
    fig=plt.Figure(figsize=(w * px, h*px))
    chart=FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x = x0, y = y0)
    ax=fig.add_subplot(111)
    fig.tight_layout()
    return chart, ax

# 建立tkinter GUI 窗口==============
root = tk.Tk()
root.geometry('1200x330')
root.config(bg = "#ebe9d5")
root.wm_title('可调正弦波信号')

# Insert a frame============
param_frame = tk.Frame(root, bd=2, bg = '#ebe9d5', highlightbackground = "black", highlightthickness = 0.5)
param_frame.place(x = 40, y = 40, width = 350, height = 250)

# Insert a label==================
frame_title_label = tk.Label(root, text="参数设置", font=("SimHei", 15), bg = '#ebe9d5', fg="blue")
frame_title_label.place(x=60, y=30)

# Insert three labels============
amplitude_label = tk.Label(root, text = '幅值',  bg = '#ebe9d5', font = ('SimHei', 12), fg = "#324e35")
amplitude_label.place(x = 50,y = 80,width = 100,height = 32)

phase_label = tk.Label(root, text = '初始相位',  bg = '#ebe9d5', font = ('SimHei', 12), fg = "#324e35")
phase_label.place(x = 50,y = 150,width = 100,height = 32)

frequency_label = tk.Label(root, text = '频率',  bg = '#ebe9d5', font = ('SimHei', 12), fg = "#324e35")
frequency_label.place(x = 50, y = 220, width = 100, height = 32)

# Insert three scales
amplitude_svar=tk.DoubleVar()
amplitude_scale=tk.Scale(
    root,
    variable=amplitude_svar,
    from_ = 0,
    to = 1,
    resolution = 0.1,
    orient = tk.HORIZONTAL,
    font = ("SimHei", 8),
    bg = '#ebe9d5')
amplitude_scale.place(x = 150,y = 80,width = 150,height = 35)
amplitude_scale.set(1)

phase_svar=tk.DoubleVar()
phase_scale=tk.Scale(
    root,
    variable = phase_svar,
    from_ = 0,
    to = 180,
    resolution = 1,
    orient = tk.HORIZONTAL,
    font = ("SimHei", 8),
    bg = '#ebe9d5')
phase_scale.place(x = 150, y = 150, width = 150, height = 35)

frequency_svar = tk.DoubleVar()
frequency_scale = tk.Scale(
    root,
    variable = frequency_svar,
    from_ = 100, to=2000,
    resolution = 1,
    orient = tk.HORIZONTAL,
    font = ("SimHei", 8),
    bg = '#ebe9d5')
frequency_scale.place(x = 150, y = 220, width = 150, height = 35)
frequency_scale.set(100)

# Insert three entries
amplitude_entry_var=tk.StringVar()
amplitude_entry=tk.Entry(root, textvariable = amplitude_entry_var)
amplitude_entry.place(x=320, y = 80, width = 50, height = 32)
amplitude_entry.insert(0, 1)

phase_entry_var=tk.StringVar()
phase_entry=tk.Entry(root, textvariable = phase_entry_var)
phase_entry.place(x = 320, y = 150, width = 50, height = 32)
phase_entry.insert(0, 0)

frequency_entry_var=tk.StringVar()
frequency_entry=tk.Entry(root, textvariable = frequency_entry_var)
frequency_entry.place(x = 320, y = 220,width = 50, height = 32)
frequency_entry.insert(0, 100)


#=绑定滑块和输入框==================
amplitude_scale.config(
    command=lambda val: scalFunc(val, amplitude_entry)
)
amplitude_entry.bind(
    "<Return>",
    lambda e: entryFunc(e, amplitude_scale)
)

phase_scale.config(
    command=lambda val: scalFunc(val, phase_entry)
)
phase_entry.bind(
    "<Return>",
    lambda e: entryFunc(e, phase_scale)
)

frequency_scale.config(
    command = lambda val: scalFunc(val, frequency_entry)
)
frequency_entry.bind(
    "<Return>",
    lambda e: entryFunc(e, frequency_scale)
)

# Insert a MatplotlibCurve==============
chart, ax = getfigure(root,450,40,700,250)

#=Tkinter主窗口循环控制==============
root.mainloop()