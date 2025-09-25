import tkinter as tk
import threading
import numpy as np
import myPackage.signal as sg

# ==初始化参数======================
Fs = 44100
N = 88200
A = 1
P = 0
black_buttons, white_buttons = [], []
white_keyboard = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'"]
black_keyboard = ['w', 'e', 't', 'y', 'u', 'o', 'p']
white_key_name = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5']
black_key_name = [0, 1, 3, 4, 5, 7, 8]
white_F = [261.63, 293.66, 329.63, 349.23, 392, 440, 493.88, 523.25, 587.33, 659.25, 698.46]
black_F = [277.18, 311.13, 369.99, 415.3, 466.16, 554.37, 622.25]

# ==音频播放线程函数=======================
def play_audio_thread(func, *args):
    func(*args)

# ==控件回调函数=======================
def play_white_sound(index, is_keyboard=False):
    # 按钮颜色反馈
    white_buttons[index].config(bg= "#bfbfbf")
    root.update()
    # 创建并启动音频播放线程
    thread = threading.Thread(
        target=sg.piano_voice,
        args=(Fs, N, A, white_F[index], P),
        daemon=True
    )
    thread.start()
    root.after(100, lambda: white_buttons[index].config(bg="white"))


def play_black_sound(index, is_keyboard=False):
    # 按钮颜色反馈
    black_buttons[index].config(bg="white")
    root.update()
    # 创建并启动音频播放线程
    thread = threading.Thread(
        target=sg.piano_voice,
        args=(Fs, N, A, black_F[index], P),
        daemon=True
    )
    thread.start()
    # 恢复颜色
    root.after(100, lambda: black_buttons[index].config(bg="black"))


def key_press(event):
    key = event.char
    if key in white_keyboard:
        index = white_keyboard.index(key)
        play_white_sound(index, is_keyboard=True)
    elif key in black_keyboard:
        index = black_keyboard.index(key)
        play_black_sound(index, is_keyboard=True)


# == 建立tkinter GUI 窗口==============
root = tk.Tk()
root.geometry('770x350')
root.config(bg="#dbeded")
root.wm_title('数字电子琴')
root.resizable(False, False)

# ==插入11个白键按钮=====================
for i in range(11):
    btn = tk.Button(root, text=white_key_name[i], bg="white",font=14, fg='grey', anchor="s", pady=50,
                    command=lambda idx=i: play_white_sound(idx))
    btn.place(x=0 + i * 70, y=0, width=70, height=330)
    white_buttons.append(btn)

# ==插入7个黑色按键按钮=========================
for i in range(7):
    btn = tk.Button(root, bg="black", relief=tk.RAISED, bd=3, command=lambda idx=i: play_black_sound(idx))
    btn.place(x=45 + black_key_name[i] * 70, y=0, width=50, height=200)
    black_buttons.append(btn)

# ==插入键盘说明=======================================
root.bind('<KeyPress>', key_press)
instructions = tk.Label(root, text="白键: A S D F G H J K L ; '    黑键: W E T Y U O P",
                        bg="#dbeded", font=("SimHei", 10))
instructions.place(x=10, y=330)

# =Tkinter主窗口循环控制==============
root.mainloop()

