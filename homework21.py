import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.misc import electrocardiogram
from scipy.linalg import svd
from scipy.linalg import hankel
import numpy as np
#================自定义函数==================
Y = []
def getfigure(win, x0, y0, w, h):
    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.Figure(figsize=(w * px, h * px))
    fig.patch.set_facecolor('#E2EAF4')
    fig.subplots_adjust(left=0.1,right=0.9,bottom=0.1,top=0.9,hspace=0)
    chart = FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x=x0, y=y0)
    ax = fig.add_subplot(111)
    #ax.yaxis.set_visible(False)
    #ax.xaxis.set_visible(False)
    return chart, ax

def drawnFunc():
    global x
    ecg = electrocardiogram()
    x = ecg[0:1024]
    ax.plot(x)
    chart.draw();

#====回调函数=============================
def separate():
    global a, Y
    fig, ax1 = plt.subplots(nrows=1, ncols=1)
    ax1.yaxis.set_visible(False)
    ax1.xaxis.set_visible(False)
    K = int(K_entry_var.get())
    A = hankel(x)
    U, S, Vt = svd(A)
    Y = []
    for k in range(K):
        EL = np.zeros((U.shape[1], Vt.shape[0]))
        D = np.diag(S)
        EL[k, k] = D[k, k]
        AA = U @ EL @ Vt
        Y.append(AA[0, :])
        ax1.plot(AA[0, :] - k * 5)
    plt.show()

def reset():
    global Y
    if not Y:
        return
    K = [(int(i)-1) for i in K2_entry_var.get().split(',')]
    y = np.zeros_like(Y[0])
    for i in K:
        y += Y[i]
    fig, ax2 = plt.subplots(nrows=1, ncols=1)
    ax2.yaxis.set_visible(False)
    ax2.xaxis.set_visible(False)
    ax2.plot(y)
    plt.show()

#========插入主窗口===========================
root = tk.Tk()
root.geometry("800x480")
root.config(background="#E2EAF4")
root.title("PCD分解与重构心电图")

#========插入matplotlib=====================
chart, ax = getfigure(root, -30, 35, 880, 450)
drawnFunc()

#=========插入阶数K输入框==================
K_label = tk.Label(root, text="阶数(K):", bg = '#E2EAF4', fg="black", font=("", 14))
K_label.place(x=10, y=25)
K_entry_var = tk.StringVar(value='10')
K_entry = tk.Entry(root, textvariable=K_entry_var, background="white", fg="black", font=("", 14), justify=tk.CENTER)
K_entry.place(x=90, y=10, width=80, height=50)

#========插入分解按钮========================
separate_btn = tk.Button(root, text = "分解", bg="#ffe4b0", font=12, fg='black', command=separate)
separate_btn.place(x=200, y=10, width=80, height=50)

#========插入重构按钮======================
reset_btn = tk.Button(root, text = "重构", bg="#ffe4b0", font=12, fg='black', command=reset)
reset_btn.place(x=350, y=10, width=80, height=50)

#=========插入奇异值输入框==================
K2_label = tk.Label(root, text="奇异值:", bg = '#E2EAF4', fg="black", font=("", 14))
K2_label.place(x=450, y=25)
K2_entry_var = tk.StringVar(value='1,2,3,4,5,6,7,8,9,10')
K2_entry = tk.Entry(root, textvariable=K2_entry_var, background="white", fg="black", font=("", 14), justify=tk.CENTER)
K2_entry.place(x=530, y=10, width=250, height=50)

#==========主窗口循环=====================
root.mainloop()