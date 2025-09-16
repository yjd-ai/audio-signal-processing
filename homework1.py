import numpy as np
import matplotlib.pyplot as plt
Fs=11025;
N=100;
dt=1.0/Fs
t=np.arange(N)*dt
x1=np.sin(2*np.pi*500*t)
x2=np.sin(2*np.pi*600*t)
x3=np.sin(2*np.pi*700*t)
x4=np.sin(2*np.pi*800*t)
plt.rcParams['font.sans-serif'] = ['SimSun'] # 使用黑体，防止中文乱码
plt.rcParams['axes.unicode_minus'] = False # 防止负号乱码
fig,ax=plt.subplots(nrows=2,ncols=2)
ax[0][0].plot(t,x1)
ax[0][0].set_xlabel("500Hz信号")
ax[0][1].plot(t,x2)
ax[0][1].set_xlabel("600Hz信号")
ax[1][0].plot(t,x3)
ax[1][0].set_xlabel("700Hz信号")
ax[1][1].plot(t,x4)
ax[1][1].set_xlabel("800Hz信号")
plt.tight_layout() # 调整布局
plt.show()