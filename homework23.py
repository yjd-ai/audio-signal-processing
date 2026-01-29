import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import warnings
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller as ADF
from statsmodels.stats.diagnostic import acorr_ljungbox
import statsmodels.api as sm
#from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np

#======初始化==================================
warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
data = None
D_data = None

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

#====回调函数========================
def open_file():
    global data, D_data
    file_types = [
        ("CSV文件", "*.csv")
    ]
    file_path = filedialog.askopenfilename(
        title="选择CSV文件",
        filetypes=file_types,
        initialdir="./"  # 初始目录
    )
    if file_path:
        # 正确读取这个特殊格式的CSV文件
        data = pd.read_csv(file_path)
        # 重命名列，使其更简洁
        data.columns = ['Month', 'Passengers']
        # 转换日期格式
        data['Month'] = pd.to_datetime(data['Month'])
        # 设置索引
        data.set_index('Month', inplace=True)
        ax.clear();
        ax.plot(data.index, data['Passengers'])
        ax.set_title('国际航空公司乘客数量时间序列')
        ax.set_xlabel('日期')
        ax.set_ylabel('乘客数量')
        ax.grid(True)
        chart.draw()

        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
        # 在第一个子图中绘制ACF
        plot_acf(data['Passengers'], ax=ax1)
        ax1.set_title('自相关函数 (ACF)')
        # 在第二个子图中绘制PACF
        plot_pacf(data['Passengers'], ax=ax2)
        ax2.set_title('偏自相关函数 (PACF)')
        # 调整布局
        plt.tight_layout()
        plt.show()
        # 打印ADF检验结果
        print(u'原始序列的ADF检验结果为：', ADF(data[u'Passengers']))
        D_data = None

def diffFunc():
    global data, D_data
    if data is None:
        print("请先加载数据")
        return
    passengers_data = data['Passengers']
    # 计算差分
    tmp_data = passengers_data.diff().dropna()  # 一阶差分并去空列
    D_data = tmp_data.diff().dropna()  # 二阶差分

    # 创建包含时序图的窗口
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

    # 原始序列
    ax1.plot(data.index, passengers_data)
    ax1.set_title('原始序列')
    ax1.grid(True)
    # 一阶差分序列
    ax2.plot(tmp_data.index, tmp_data)
    ax2.set_title('一阶差分序列')
    ax2.grid(True)
    # 二阶差分序列
    ax3.plot(D_data.index, D_data)
    ax3.set_title('二阶差分序列')
    ax3.grid(True)
    plt.tight_layout()
    plt.show()

    # 创建ACF/PACF图
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    # 一阶差分的ACF/PACF
    plot_acf(tmp_data, ax=axes[0, 0], lags=20)
    axes[0, 0].set_title('一阶差分ACF')
    plot_pacf(tmp_data, ax=axes[0, 1], lags=20)
    axes[0, 1].set_title('一阶差分PACF')
    # 二阶差分的ACF/PACF
    plot_acf(D_data, ax=axes[1, 0], lags=20)
    axes[1, 0].set_title('二阶差分ACF')
    plot_pacf(D_data, ax=axes[1, 1], lags=20)
    axes[1, 1].set_title('二阶差分PACF')
    plt.tight_layout()
    plt.show()

    # ADF检验
    print(u'一阶差分序列的ADF检验结果为：', ADF(tmp_data))
    print(u'二阶差分序列的ADF检验结果为：', ADF(D_data))
    print(u'二阶差分序列的白噪声检验结果为：', acorr_ljungbox(D_data, lags=1))

def BIC_and_AIC():
    global D_data
    if D_data is None:
        return
    AIC = sm.tsa.stattools.arma_order_select_ic(D_data, max_ar=4, max_ma=4, ic='aic')['aic_min_order']
    # BIC
    BIC = sm.tsa.stattools.arma_order_select_ic(D_data, max_ar=4, max_ma=4, ic='bic')['bic_min_order']
    print('---AIC与BIC准则定阶---')
    print('the AIC is{}\nthe BIC is{}\n'.format(AIC, BIC), end='')


def pretect():
    global data
    if data is None:
        return

    # 拟合ARIMA模型
    model = SARIMAX(data['Passengers'],
                    order=(2, 2, 4),
                    seasonal_order=(1, 1, 1, 12))  # 添加季节性参数

    res = model.fit(disp=False)

    # 修复预测部分 - 使用正确的时间戳处理方式
    last_date = data.index[-1]
    # 创建未来16个月的日期索引
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=16, freq='M')

    # 预测原始数据范围 + 未来16个月
    df = res.predict(start=data.index[0], end=future_dates[-1])

    # 绘制结果
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Passengers'], label='实际数据')
    plt.plot(df.index, df, label='预测数据', color='red')
    plt.title('ARIMA模型预测')
    plt.xlabel('日期')
    plt.ylabel('乘客数量')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# =======插入主窗口==================
root = tk.Tk()
root.geometry("800x520")
root.config(background="#E2EAF4")
root.title("稀疏采样")

# =====插入matplotlib====================
chart, ax = getfigure(root, -30, 55, 880, 450)

# =========插入信号按钮===================
file_btn = tk.Button(root, text="文件", bg="#ffe4b0", font=12, fg='black', command = open_file)
file_btn.place(x=60, y=15, width=90, height=42)

# ============插入差分按钮==========================
diff_btn = tk.Button(root, text="差分", bg="#ffe4b0", font=12, fg='black', command= diffFunc)
diff_btn.place(x=160, y=15, width=90, height=42)

# ============插入BIC及AIC准测按钮==========================
pq_btn = tk.Button(root, text="BIC及AIC准测", bg="#ffe4b0", font=12, fg='black', command= BIC_and_AIC)
pq_btn.place(x=260, y=15, width=150, height=42)

# ============插入预测按钮==========================
pre_btn = tk.Button(root, text="预测", bg="#ffe4b0", font=12, fg='black', command= pretect)
pre_btn.place(x=420, y=15, width=90, height=42)

# =========主窗口循环=================
root.mainloop()