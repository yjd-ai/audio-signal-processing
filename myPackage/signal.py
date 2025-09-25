from scipy import signal
import numpy as np
import simpleaudio as sa
import pyaudio

#===正弦信号================================
def sinGenerator(Fs,N,A,F,P):
    t=np.arange(N)*(1.0/Fs)
    y=A*np.sin(2*np.pi*F*t+P / 180 * np.pi)
    return t,y

#==余弦信号==================================
def cosGenerator(Fs,N,A,F,P):
    t=np.arange(N)*(1.0/Fs)
    y=A*np.cos(2*np.pi*F*t+P / 180 * np.pi)
    return t,y

#==方波信号==================================
def squareGenerator(Fs,N,A,F,P,d):
    t=np.arange(N)*(1.0/Fs)
    y=A*signal.square(2*np.pi*F*t+P / 180 * np.pi,d)
    return t,y

#===三角波信号==================================
def sawGenerator(Fs,N,A,F,P,d):
    t = np.arange(N) * (1.0 / Fs)
    y = A * signal.sawtooth(2 * np.pi * F * t + P / 180 * np.pi, d)
    return t,y

#==白噪声============================================
def noiseGenerator(Fs,N,A):
    t=np.arange(N)*(1.0/Fs)
    y=A*0.333333*np.random.randn(N)
    return t,y

#==数组归一化=========================
def normalize(arr):
    # 创建数组的可写副本
    arr = arr.copy()  # 关键修复：确保数组可写
    max_val = np.max(np.abs(arr))
    if max_val > 0:
        arr1 = arr/max_val
    return arr1

#==数字信号转化成声音信号=================================
def digit_to_voice(digital_signal, Fs):
    if digital_signal is not None:
        # 归一化
        normalized_signal = normalize(digital_signal)
        # 将归一化信号转换为16位整数格式 16位音频的范围是[-32768, 32767]
        audio_data = (normalized_signal * 32767).astype(np.int16)
        # 创建音频播放对象并播放
        play_obj = sa.play_buffer(audio_data, 1, 2, Fs)  # 1表示单声道，2表示16位
        play_obj.wait_done()

#==钢琴音色======================================
def piano_voice(Fs, N, A, F, P = 0):
    # 一、基音
    _, y = cosGenerator(Fs, N, 0.3, F, P)
    # 二、泛音
    harmonic_multipliers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    harmonic_amplitudes = [0.5, 0.3, 0.25, 0.18, 0.15, 0.08, 0.06, 0.03, 0.02, 0.01, 0.008]
    for i, multiplier in enumerate(harmonic_multipliers):
        # 泛音使用不同波形，增强层次感
        if i % 2 == 0:
            _, harmonic = sinGenerator(Fs, N, 0.2, F * multiplier, P)
        else:
            _, harmonic = cosGenerator(Fs, N, 0.2, F * multiplier, P)
        # 高音区泛音强度适当降低
        if F > 500:
            y += harmonic_amplitudes[i] * 0.7 * harmonic
        else:
            y += harmonic_amplitudes[i] * harmonic

    # 三、包络
    N1 = int(N * 300 / 88200)
    N2 = int(N * 1200 / 88200)
    N3 = int(N * 45000 / 88200)
    N4 = N - N1 - N2 - N3
    A1 = np.arange(N1) / N1 * 1.0
    A2 = 1.0 - 0.6 * np.arange(N2) / N2
    A3 = 0.4 - 0.25 * np.arange(N3) / N3
    A4 = 0.15 - 0.14 * np.arange(N4) / N4
    adsr = np.concatenate((A1, A2, A3, A4))
    y *= adsr

    # 四、播放
    digit_to_voice(y, Fs)

#==信号加窗=========================
def winFunction(winT,N):
    if winT==0: w=np.ones(N)
    if winT==1: w=signal.windows.bartlett(N)*2;
    if winT==2: w=signal.windows.hann(N)*2;
    if winT==3: w=signal.windows.hamming(N)*1.852
    if winT==4: w=signal.windows.blackman(N)*2.381
    if winT==5: w=signal.windows.flattop(N)*4.545
    return w

#==幅频谱===================================
def AmplitudeSpetrum(N,Fs,data):
    x=data[:N]
    N2=int(N/2)
    y=np.fft.rfft(x)
    A=np.abs(y[:N2])*(2/N)
    f=np.arange(N2)*(Fs/N);
    return f,A

#==提取麦克风数据=================
def audio_mic(sample_rate, chunk, channel):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=channel,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)
    data = stream.read(chunk, exception_on_overflow=False)
    audio_data = np.frombuffer(data, dtype=np.int16) # 转成整型
    normalized_data = normalize(audio_data)
    return normalized_data


def signal_param(Fs, N, x):
    if len(x) < 4:
        return (0, 0, 0, 0, 0, 0, 0)

    p, q = max(x), min(x)
    at = 0.8 * (p - q) + q
    dt = 1 / Fs
    ti = []
    for k in range(2, len(x) - 2):
        if x[k - 1] < at and x[k] <= at and x[k + 1] > at and x[k + 2] > at:
            ti.append(k)
    if len(ti) >= 2:
        T = (ti[1] - ti[0]) * dt
        F = 1 / T if T else 0
        phase_offset = (ti[0] * dt) % T if T else 0
        Q = 360 * (phase_offset / T) if T else 0
        return (F, Q, p, q, np.std(x), np.mean(x), len(ti))
    else:
        return (0, 0, 0, 0, 0, 0, 0)

    pp = np.max(x) - np.min(x) # 峰峰值
    R = np.sqrt(np.sum(x ** 2) / N) # 有效值
    std = np.std(x) # 方差
    M = np.mean(x) # 均值
    kk = (np.sum(x ** 4) / N) / pow(R, 4) # 峭度
    return F, Q, pp, R, std, M, kk