import tkinter as tk

root = tk.Tk()
root.title("参数设置")

# 创建一个框架作为容器
param_frame = tk.Frame(root,  # 父窗口
                      relief=tk.RAISED,  # 边框样式（凸起）
                      bd=2)  # 边框宽度

# 在框架内添加各种控件
label1 = tk.Label(param_frame, text='幅值', font=('SimHei', 12))
label1.place(x=20, y=20, width=60, height=30)

scale1 = tk.Scale(param_frame, from_=0, to=100, orient=tk.HORIZONTAL)
scale1.place(x=90, y=20, width=150)

entry1 = tk.Entry(param_frame)
entry1.place(x=250, y=20, width=60, height=30)

# 显示框架（设置框架的位置和大小）
param_frame.place(x=50, y=50, width=350, height=200)

root.mainloop()