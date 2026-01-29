import tkinter as tk
from tkinter import scrolledtext, messagebox
import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt
import myPackage.widget as wg

#============回调函数====================
def drawFunc():
    code = code_input.get(1.0, tk.END).strip()
    if not code:
        messagebox.showwarning("警告", "请先输入代码！")
        return
    local_vars = {}
    try:
        exec(code, globals(), local_vars)
    except Exception as e:
        messagebox.showerror("代码执行错误", f"输入的代码有误：\n{str(e)}")
        return
    try:
        t = local_vars['t']
        y = local_vars['y']
        Fs = local_vars['Fs']
    except KeyError as e:
        messagebox.showerror("变量错误", f"缺少必要变量：{str(e)}")
        return
    try:
        z = hilbert(y)
        Ainst = np.abs(z)
        Pinst = np.unwrap(np.angle(z))
        Finst = (np.diff(Pinst) / (2.0 * np.pi) * Fs)
        Finst = np.clip(Finst, 0, np.max(Finst))
        y_min = np.min(y)
        Ainst_z = np.full_like(Ainst, y_min)
        F_max = np.max(Finst) + 10
        Finst_z = np.full_like(Finst, F_max)
        M = len(Finst)
        # 绘图
        fig = plt.figure(figsize=(10, 8))
        ax = plt.axes(projection='3d')
        ax.plot3D(t[0:M], Finst_z, y[0:M], 'red')
        ax.plot3D(t[0:M], Finst, Ainst[0:M], 'green')
        ax.plot3D(t[0:M], Finst, Ainst_z[0:M], 'blue')
        ax.set_xlabel('t(s)')
        ax.set_ylabel('f(Hz)')
        ax.set_zlabel('A')
        plt.show()
    except Exception as e:
        messagebox.showerror("绘图错误", f"绘图过程出错：\n{str(e)}")

def signal_sf():
    code = """Fs = 1000 
N = 1000
dt = 1.0 / Fs
t = np.arange(N) * dt
y = np.sin(2 * np.pi * 100 * t * t)"""
    code_input.insert(tk.END, code)

def signal_mf():
    code = """Fs = 5120
x = np.arange(350) * (1 / Fs)
y1 = np.sin(2 * np.pi * 100 * x)
y2 = np.sin(2 * np.pi * 1000 * x)
y3 = np.sin(2 * np.pi * 2000 * x)
y = np.concatenate([y1, y2, y3])
t = np.arange(len(y)) * (1 / Fs)"""
    code_input.insert(tk.END, code)

def clear():
    code_input.delete(1.0, tk.END)

#========插入主窗口===========================
root = tk.Tk()
root.geometry("800x480")
root.config(background="#E2EAF4")
root.title("希尔伯特变换----自变量t,因变量y, 采样率Fs")

#======插入代码输入框============================
code_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 14))
code_input.place(x= 10, y= 10, w= 700, h=450)

#======插入画图按钮================================
draw_btn = tk.Button(root, text="确定", bg="#EFD8B7", font=12, fg='black', command=drawFunc)
draw_btn.place(x=720, y=10, width=70, height=40)

#===插入扫频信号按钮=============================
draw_btn = tk.Button(root, text="扫频信号", bg="#EFD8B7", font=12, fg='black', command=signal_sf)
draw_btn.place(x=715, y=90, width=80, height=40)

#===插入多频信号按钮=============================
draw_btn = tk.Button(root, text="多频信号", bg="#EFD8B7", font=12, fg='black', command=signal_mf)
draw_btn.place(x=715, y=140, width=80, height=40)

#===插入清空按钮=============================
draw_btn = tk.Button(root, text="清空", bg="#EFD8B7", font=12, fg='black', command=clear)
draw_btn.place(x=720, y=400, width=70, height=40)

#============主窗口循环=======================
root.mainloop()