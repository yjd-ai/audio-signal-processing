import tkinter as tk
import math
#===旋钮控件======================================
class Knob(tk.Frame):
    def __init__(self, master=None, min_val=0, max_val=100, start_val=None,
                 size=120, color="#0078d7", x=0, y=0, text="", command=None, **kwargs):
        # 处理起始值默认值
        if start_val is None:
            start_val = (min_val + max_val) / 2
        # 确保使用tk.Frame的背景色处理方式
        if master:
            bg_color = master.cget("bg")
            kwargs.setdefault('bg', bg_color)
        else:
            kwargs.setdefault('bg', '#dbeded')  # 默认背景色
        super().__init__(master, **kwargs)
        # 基本参数设置
        self.min_val, self.max_val = min_val, max_val
        self.value = start_val
        self.size, self.color = size, color
        self.total_angle = self._value_to_angle(start_val)
        self.pos_x, self.pos_y = x, y
        self.center_text = text
        self.command = command
        # 计算尺寸参数
        self.cx = self.cy = size // 2
        self.outer_r, self.inner_r = int(size * 0.42), int(size * 0.29)
        # 获取背景色
        self.bg_color = self.cget("bg")
        # 创建画布
        self.canvas = tk.Canvas(self, width=size, height=size,
                                bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(pady=(5, 0))
        self.value_label = tk.Label(
            self,
            text=f"{start_val:.2f}",
            font=("Segoe UI", int(size * 0.1)),
            bg=self.bg_color
        )
        self.value_label.pack(pady=0, anchor="n")
        # 绑定事件
        for evt, func in [("<Button-1>", self.on_press),
                          ("<B1-Motion>", self.on_drag),
                          ("<MouseWheel>", self.on_scroll),
                          ("<Button-4>", self.on_scroll),
                          ("<Button-5>", self.on_scroll)]:
            self.canvas.bind(evt, func)

        self.dragging = False
        self.indicator_coords = (0, 0)
        self.draw_knob()

        self.place(x=self.pos_x, y=self.pos_y)
    # 角度与值转换方法
    def _value_to_angle(self, value):
        ratio = (value - self.min_val) / (self.max_val - self.min_val)
        return math.radians(135 + ratio * 270)
    def _angle_to_value(self, angle):
        deg = max(135, min(405, math.degrees(angle)))
        return self.min_val + (deg - 135) / 270 * (self.max_val - self.min_val)
    # 绘制旋钮
    def draw_knob(self):
        self.canvas.delete("all")
        # 绘制旋钮主体
        self.canvas.create_oval(
            self.cx - self.outer_r, self.cy - self.outer_r,
            self.cx + self.outer_r, self.cy + self.outer_r,
            fill=self.bg_color, outline=""
        )
        self.canvas.create_oval(
            self.cx - self.outer_r + 3, self.cy - self.outer_r + 3,
            self.cx + self.outer_r - 3, self.cy + self.outer_r - 3,
            fill=self.color, outline=self._lighten_color(self.color, 1.3), width=1
        )
        self.canvas.create_oval(
            self.cx - self.inner_r, self.cy - self.inner_r,
            self.cx + self.inner_r, self.cy + self.inner_r,
            fill=self._darken_color(self.color, 0.7), outline=""
        )
        # 中间文字
        if self.center_text:
            font_size = int(self.inner_r * 0.6)
            self.canvas.create_text(
                self.cx, self.cy,
                text=self.center_text,
                font=("Segoe UI", font_size, "bold"),
                fill="white"
            )
        # 刻度和指示点
        for i in range(24):
            angle = math.radians(135 + i * 11.25)
            r1, r2 = self.outer_r - 8, self.outer_r - 2 if i % 4 == 0 else self.outer_r - 5
            x1, y1 = self.cx + r1 * math.cos(angle), self.cy + r1 * math.sin(angle)
            x2, y2 = self.cx + r2 * math.cos(angle), self.cy + r2 * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2,
                                    width=2 if i % 4 == 0 else 1, fill="white")
        angle = self._value_to_angle(self.value)
        ind_r = (self.outer_r + self.inner_r) / 2
        ix, iy = self.cx + ind_r * math.cos(angle), self.cy + ind_r * math.sin(angle)
        self.indicator_coords = (ix, iy)
        self.canvas.create_oval(ix - 7, iy - 7, ix + 5, iy + 5, fill="#cca700")
        self.canvas.create_oval(ix - 6, iy - 6, ix + 6, iy + 6,
                                fill="#ffd700", outline="#ffffff", width=2)

        self.value_label.config(text=f"{self.value:.2f}")
    # 颜色处理函数
    def _darken_color(self, color, factor):
        r, g, b = [int(color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
        return f'#{int(r * factor):02x}{int(g * factor):02x}{int(b * factor):02x}'
    def _lighten_color(self, color, factor):
        r, g, b = [int(color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
        return f'#{min(255, int(r * factor)):02x}{min(255, int(g * factor)):02x}{min(255, int(b * factor)):02x}'
    # 事件处理方法
    def get_angle(self, x, y):
        return math.atan2(y - self.cy, x - self.cx)
    def is_click_on_indicator(self, x, y):
        ix, iy = self.indicator_coords
        return math.hypot(x - ix, y - iy) <= 6
    def on_press(self, event):
        if self.is_click_on_indicator(event.x, event.y):
            self.dragging = True
            self.last_angle = self.get_angle(event.x, event.y)
    def on_drag(self, event):
        if self.dragging:
            current_angle = self.get_angle(event.x, event.y)
            delta = current_angle - self.last_angle
            if delta > math.pi:
                delta -= 2 * math.pi
            elif delta < -math.pi:
                delta += 2 * math.pi
            self.total_angle += delta * 0.5
            self.value = self._angle_to_value(self.total_angle)
            self.last_angle = current_angle
            self.draw_knob()
            if self.command:
                self.command(self.value)
    def on_scroll(self, event):
        step = (self.max_val - self.min_val) / 200
        if event.delta > 0 or event.num == 4:
            self.value = min(self.max_val, self.value + step)
        else:
            self.value = max(self.min_val, self.value - step)
        self.total_angle = self._value_to_angle(self.value)
        self.draw_knob()
        if self.command:
            self.command(self.value)
    def get_value(self):
        """获取当前旋钮值"""
        return self.value
    def set_position(self, x, y):
        """设置旋钮位置"""
        self.pos_x, self.pos_y = x, y
        self.place(x=x, y=y)
    def set_center_text(self, text):
        """设置旋钮中心文本"""
        self.center_text = text
        self.draw_knob()

#==开关控件=======================================
class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, width=60, height=30, bg_color="#e0e0e0",
                 active_color="#0a4da2", circle_color="#ffffff", x=0, y=0, command=None):
        # 移除了command参数
        super().__init__(parent, width=width, height=height,
                         bg=parent["bg"], highlightthickness=0)
        # 设置开关在父组件中的位置
        self.place(x=x, y=y)
        # 开关属性
        self.w, self.h = width, height
        self.bg, self.active_bg = bg_color, active_color
        self.circle_color = circle_color
        self.active = False  # 默认关闭状态
        self.command = command
        # 绘制开关并绑定事件
        self.draw()
        self.bind("<Button-1>", self.toggle)
    def draw(self):
        """绘制开关组件"""
        self.delete("all")
        r = self.h // 2  # 圆角半径
        # 绘制背景
        self.create_polygon(
            [r, 0, self.w - r, 0, self.w, 0, self.w, r, self.w, self.h - r,
             self.w, self.h, self.w - r, self.h, r, self.h, 0, self.h,
             0, self.h - r, 0, r, 0, 0],
            fill=self.active_bg if self.active else self.bg,
            smooth=True
        )
        # 绘制滑块
        x = r if not self.active else self.w - r
        self.create_oval(
            x - r + 2, r - r + 2,
            x + r - 2, r + r - 2,
            fill=self.circle_color, outline=""
        )
    def toggle(self, event=None):
        """切换开关状态"""
        self.active = not self.active
        self.draw()
        if self.command:
            self.command(self.active)
    def get_state(self):
        """获取当前开关状态"""
        return self.active
    def set_state(self, state):
        """设置开关状态"""
        if self.active != state:
            self.active = state
            self.draw()
#=========================================================