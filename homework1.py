import matplotlib.pyplot as plt
import myPackage.signal as sg
Fs=11025;
N=100;
A = 1
F = [500, 600, 700, 800]
P = 0
plt.rcParams['font.sans-serif'] = ['SimSun'] # 使用黑体，防止中文乱码
plt.rcParams['axes.unicode_minus'] = False # 防止负号乱码
fig,ax=plt.subplots(nrows=4,ncols=1)
for i in range(4):
    t, y = sg.sinGenerator(Fs,N,A,F[i],P)
    ax[i].plot(t, y)
    ax[i].set_xlabel(str(F[i]) + "Hz信号")
plt.tight_layout() # 调整布局
plt.show()