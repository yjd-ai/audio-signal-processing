import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import librosa
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
#==初始化参数=======================
x_left = 0.1
x_right = 0.2
x = []
y = []
#==自定义函数========================
def drawFunc():
    ax1.clear()
    ax2.clear()
    ax1.grid()
    ax2.grid()
    # 绘制完整波形（上半部分）
    ax1.plot(x, y, color='y', linewidth=0.5)
    ax2.plot(x, y, color='y', linewidth=0.5)
    ax2.set_xlim(x_left, x_right)
    # 调整布局并刷新画布
    plt.tight_layout()
    chart.draw()

#==回调函数=========================
def open_file():
    file_types = [
        ("音频文件", "*.mp3; *.wav")
    ]
    file_path = filedialog.askopenfilename(
        title="选择音视频文件",
        filetypes=file_types,
        initialdir="."  # 初始目录
    )
    if file_path:
        file_entry_var.set(file_path)

def show_wave():
    global x, y
    file_path = file_entry_var.get()
    try:
        # 读取音频文件，返回波形数据y和采样率sr
        # sr=None表示保留原始采样率
        y, sr = librosa.load(file_path, sr=None)
        # 计算时间轴x（单位：秒）
        # 时间 = 样本索引 / 采样率
        x = np.arange(len(y)) / sr
        drawFunc()
    except Exception as e:
        print("错误", f"读取音频失败：{str(e)}")
def move_left():
    global x_left, x_right
    a = x_right - x_left
    x_left -= a
    x_right -= a
    drawFunc()
def move_right():
    global x_left, x_right
    a = x_right - x_left
    x_left += a/10
    x_right += a/10
    drawFunc()
def reset():
    global x_left, x_right
    x_left = 0.1
    x_right = 0.2
    drawFunc()

def zoom_out():
    global x_left, x_right
    x_left *= 1.1
    x_right *= 1.1
    drawFunc()

def zoom_in():
    global x_left, x_right
    x_left /= 1.1
    x_right /= 1.1
    drawFunc()

# 建立tkinter GUI 窗口==============
root = tk.Tk()
root.geometry('1000x500')
root.config(bg="#dbeded")
root.wm_title('音频文件波形查看')

# ==插入查看波形按钮========================
stop_btn = tk.Button(root, text="查看", bg="#003355", font=12, fg='white', command = show_wave)
stop_btn.place(x=100, y=20, width=120, height=32)

# ==插入文件按钮================================
file_btn = tk.Button(root, text="文件", bg="#003355", font=12, fg='white', command=open_file)
file_btn.place(x=270, y=20, width=120, height=32)

# ==文件路径编辑框=======================
file_entry_var = tk.StringVar()
file_entry = tk.Entry(root, textvariable=file_entry_var)
file_entry.place(x=400, y=20, width=580, height=32)

#==左右移动按钮=====================
file_btn = tk.Button(root, text="<-", bg="#003355", font=12, fg='white', command=move_left)
file_btn.place(x=355, y=465, width=50, height=20)

file_btn = tk.Button(root, text="->", bg="#003355", font=12, fg='white', command=move_right)
file_btn.place(x=415, y=465, width=50, height=20)

#==重置按钮==================
file_btn = tk.Button(root, text="○", bg="#003355", font=12, fg='white', command=reset)
file_btn.place(x=475, y=465, width=50, height=20)

#==放大缩小按钮================
file_btn = tk.Button(root, text="-", bg="#003355", font=12, fg='white', command=zoom_out)
file_btn.place(x=535, y=465, width=50, height=20)

file_btn = tk.Button(root, text="+", bg="#003355", font=12, fg='white', command=zoom_in)
file_btn.place(x=595, y=465, width=50, height=20)

# 插入信号显示框==============
def set_axis_style(ax):
    ax.set_facecolor('black')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='both', colors='white')
    ax.grid(True, color='white', linestyle='--', linewidth=0.5, alpha=0.7)
    return ax
def getfigure(win, x0, y0, w, h):
    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.Figure(figsize=(w * px, h * px))
    fig.patch.set_facecolor('#003355')
    chart = FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x=x0, y=y0)
    ax1 = set_axis_style(fig.add_subplot(211))
    ax2 = set_axis_style(fig.add_subplot(212))
    fig.tight_layout()
    return chart, ax1, ax2

plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
chart, ax1, ax2 = getfigure(root, 10, 60, 980, 400)

# =Tkinter主窗口循环控制==============
root.mainloop()