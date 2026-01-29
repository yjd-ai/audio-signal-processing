import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sklearn.linear_model import Lasso

# ===========初始化参数================
N = 256
Fs = 256
sparsity = 5  # 降低稀疏度提高稀疏性
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 全局变量
y_origin = None
measurement_matrix = None
transform_matrix = None
sparse_coefficients = None
y_measurements = None
y_reconstruct = None
error_info = None
chart = None
ax = None


# ==========自定义函数==================
def getfigure(win, x0, y0, w, h):
    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.Figure(figsize=(w * px, h * px))
    fig.patch.set_facecolor('#E2EAF4')
    fig.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, hspace=0)
    chart = FigureCanvasTkAgg(fig, win)
    chart.get_tk_widget().place(x=x0, y=y0)
    ax = fig.add_subplot(111)
    return chart, ax


def measurement_martixFunc(N, sr, matrix_type="gaussian"):  # 观测矩阵
    if matrix_type == 'gaussian':
        matrix = np.random.randn(int(N * sr), N) / np.sqrt(int(N * sr))
    return matrix


def transform_matrixFunc(N, transform_type='dct'):  # 稀疏变换矩阵
    if transform_type == 'dct':
        matrix = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                if i == 0:
                    matrix[i, j] = 1 / np.sqrt(N)
                else:
                    matrix[i, j] = np.sqrt(2 / N) * np.cos((np.pi * (2 * j + 1) * i) / (2 * N))
    return matrix


def calculate_measures(measurement_matrix, transform_matrix, original_signal):
    sensing_matrix = np.dot(measurement_matrix, transform_matrix)  # 感知矩阵
    sparse_coefficients = np.dot(transform_matrix.T, original_signal)  # 稀疏系数
    y_measurements = np.dot(sensing_matrix, sparse_coefficients)
    return y_measurements, sparse_coefficients


def reconstruct_signalFunc(measurement_matrix, transform_matrix, measurements, method='lasso', lambda_param=0.0001,
                       max_iter=1000):
    sensing_matrix = np.dot(measurement_matrix, transform_matrix)

    if method == 'lasso':
        lasso = Lasso(alpha=lambda_param, max_iter=max_iter, tol=1e-4)
        lasso.fit(sensing_matrix, measurements)
        reconstructed_coefficients = lasso.coef_
        reconstructed_signal = np.dot(transform_matrix, reconstructed_coefficients)
    else:
        raise ValueError(f"不支持的重构方法: {method}")

    return reconstructed_signal


def calculate_reconstruction_error(original_signal, reconstructed_signal):
    # 计算均方误差
    mse = np.mean((original_signal - reconstructed_signal) ** 2)
    # 计算信噪比
    snr = 10 * np.log10(np.sum(original_signal ** 2) / np.sum((original_signal - reconstructed_signal) ** 2))
    # 相关度误差
    ree = np.linalg.norm(original_signal - reconstructed_signal) / np.linalg.norm(original_signal)
    return {
        'mse': mse,
        'snr': snr,
        'relative_error': ree
    }


# ===========回调函数===============
def signal_1():
    global y_origin, N, Fs, sparsity, measurement_matrix, transform_matrix, sparse_coefficients, y_measurements, y_reconstruct, error_info

    # 生成稀疏正弦信号
    t = np.arange(N) / Fs
    y_origin = np.zeros(N)
    frequencies = np.random.choice(range(1, 30), sparsity, replace=False)

    for freq in frequencies:
        Amp = np.random.randn() * 0.5 + 1.0
        Pha = np.random.rand() * 2 * np.pi
        y_origin += Amp * np.sin(2 * np.pi * freq * t + Pha)

    # 归一化
    max_val = np.max(np.abs(y_origin))
    if max_val > 0:
        y_origin /= max_val

    # 显示原始信号
    ax.clear()
    ax.plot(t, y_origin)
    ax.set_title('原始信号')
    ax.set_xlabel('时间 (s)')
    ax.set_ylabel('振幅')
    ax.grid(True)
    chart.draw()

    # 创建矩阵并执行压缩感知
    measurement_matrix = measurement_martixFunc(N, 0.5)  # 50%采样率
    transform_matrix = transform_matrixFunc(N)
    y_measurements, sparse_coefficients = calculate_measures(measurement_matrix, transform_matrix, y_origin)
    y_reconstruct = reconstruct_signalFunc(measurement_matrix, transform_matrix, y_measurements, lambda_param=0.0005)
    error_info = calculate_reconstruction_error(y_origin, y_reconstruct)


def drawFunc():
    global y_origin, measurement_matrix, transform_matrix, sparse_coefficients, y_measurements, y_reconstruct, error_info

    if y_origin is None:
        print("请先生成信号")
        return

    # 创建新窗口显示结果，使用更大的尺寸
    result_window = tk.Toplevel(root)
    result_window.title("压缩感知结果")
    result_window.geometry("1200x900")  # 增大窗口尺寸

    # 创建画布，使用更大的figsize
    fig = plt.Figure(figsize=(12, 9), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=result_window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # 创建子图，调整布局参数
    fig.subplots_adjust(left=0.08, right=0.95, bottom=0.08, top=0.95, hspace=0.3, wspace=0.2)

    # 创建3x2的子图布局
    ax1 = fig.add_subplot(321)
    ax2 = fig.add_subplot(322)
    ax3 = fig.add_subplot(323)
    ax4 = fig.add_subplot(324)
    ax5 = fig.add_subplot(325)
    ax6 = fig.add_subplot(326)

    t = np.arange(N) / Fs

    # 绘制稀疏系数
    ax1.plot(sparse_coefficients)
    ax1.set_title('稀疏系数', fontsize=12)
    ax1.set_xlabel('系数索引', fontsize=10)
    ax1.set_ylabel('系数值', fontsize=10)
    ax1.grid(True)
    ax1.tick_params(axis='both', labelsize=8)

    # 绘制测量值
    ax2.plot(y_measurements, 'go-', markersize=2)  # 减小点的大小
    ax2.set_title('测量值', fontsize=12)
    ax2.set_xlabel('测量索引', fontsize=10)
    ax2.set_ylabel('测量值', fontsize=10)
    ax2.grid(True)
    ax2.tick_params(axis='both', labelsize=8)

    # 绘制观测矩阵
    display_size = min(40, int(N * 0.5))  # 减小显示尺寸
    im1 = ax3.imshow(measurement_matrix[:display_size, :display_size], cmap='viridis', aspect='auto')
    ax3.set_title('观测矩阵 Φ', fontsize=12)
    ax3.set_xlabel('信号维度', fontsize=10)
    ax3.set_ylabel('测量维度', fontsize=10)
    ax3.tick_params(axis='both', labelsize=8)
    # 添加颜色条
    fig.colorbar(im1, ax=ax3, fraction=0.046, pad=0.04)

    # 绘制变换矩阵
    display_size = min(40, N)  # 减小显示尺寸
    im2 = ax4.imshow(transform_matrix[:display_size, :display_size], cmap='plasma', aspect='auto')
    ax4.set_title('稀疏变换矩阵 Ψ', fontsize=12)
    ax4.set_xlabel('信号维度', fontsize=10)
    ax4.set_ylabel('变换维度', fontsize=10)
    ax4.tick_params(axis='both', labelsize=8)
    # 添加颜色条
    fig.colorbar(im2, ax=ax4, fraction=0.046, pad=0.04)

    # 绘制重构信号
    ax5.plot(t, y_origin, 'b-', label='原始信号', linewidth=1.5, alpha=0.8)
    ax5.plot(t, y_reconstruct, 'r--', label='重构信号', linewidth=1.5, alpha=0.8)
    ax5.set_title('信号对比', fontsize=12)
    ax5.set_xlabel('时间 (s)', fontsize=10)
    ax5.set_ylabel('振幅', fontsize=10)
    ax5.legend(fontsize=9)
    ax5.grid(True)
    ax5.tick_params(axis='both', labelsize=8)

    # 添加误差信息
    error_text = (f"MSE: {error_info['mse']:.6f}\n"
                  f"SNR: {error_info['snr']:.2f} dB\n"
                  f"相对误差: {error_info['relative_error']:.6f}")
    ax5.text(0.05, 0.05, error_text, fontsize=9,
             transform=ax5.transAxes,
             bbox=dict(facecolor='white', alpha=0.8))

    # 第六个子图显示误差信号
    error_signal = y_origin - y_reconstruct
    ax6.plot(t, error_signal, 'm-', linewidth=1.5)
    ax6.set_title('误差信号', fontsize=12)
    ax6.set_xlabel('时间 (s)', fontsize=10)
    ax6.set_ylabel('误差值', fontsize=10)
    ax6.grid(True)
    ax6.tick_params(axis='both', labelsize=8)

    # 调整布局
    plt.tight_layout(pad=2.0)
    canvas.draw()


# =======插入主窗口==================
root = tk.Tk()
root.geometry("800x480")
root.config(background="#E2EAF4")
root.title("稀疏采样")

# =====插入matplotlib====================
chart, ax = getfigure(root, -30, 35, 880, 450)

# =========插入信号按钮===================
signal1_btn = tk.Button(root, text="生成信号", bg="#ffe4b0", font=12, fg='black', command=signal_1)
signal1_btn.place(x=60, y=15, width=90, height=42)

# ============插入压缩感知按钮==========================
draw_btn = tk.Button(root, text="压缩感知", bg="#ffe4b0", font=12, fg='black', command=drawFunc)
draw_btn.place(x=700, y=15, width=90, height=42)

# =========主窗口循环=================
root.mainloop()