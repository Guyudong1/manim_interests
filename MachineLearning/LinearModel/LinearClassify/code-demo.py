# -*- coding: utf-8 -*-
from manim import BOLD
from mymanim import *
import numpy as np
config.frame_width = 25
config.frame_height = 10

class LogisticRegressionDemo(Scene):
    def construct(self):
        # 1. 生成两类二维点（让数据线性可分）
        np.random.seed(0)
        n_points = 20
        X1 = np.random.randn(n_points, 2) * 1.0 + np.array([2, 2])  # 两类点中心更近
        X2 = np.random.randn(n_points, 2) * 1.0 + np.array([6, 6])
        X = np.vstack([X1, X2])
        y = np.array([0]*n_points + [1]*n_points)

        # 2. 创建坐标轴
        axes = Axes(
            x_range=[-2, 10, 1],
            y_range=[-2, 10, 1],
            axis_config={"color": WHITE},
            x_length=10,
            y_length=10,
        ).move_to(LEFT*4)  # 坐标轴整体左移
        self.play(Create(axes))
        # 不再添加x1, x2标签

        # 3. 绘制数据点
        dots1 = VGroup(*[Dot(axes.c2p(*pt), color=BLUE) for pt in X1])
        dots2 = VGroup(*[Dot(axes.c2p(*pt), color=RED) for pt in X2])
        self.play(FadeIn(dots1, lag_ratio=0.1), FadeIn(dots2, lag_ratio=0.1))
        self.wait(0.5)

        # 4. 初始化分割线参数
        w_tracker = ValueTracker(1)
        v_tracker = ValueTracker(-1)
        b_tracker = ValueTracker(0)

        # 5. 绘制分割线
        def get_line():
            w1 = w_tracker.get_value()
            w2 = v_tracker.get_value()
            b0 = b_tracker.get_value()
            if abs(w2) < 1e-3:
                w2 = 1e-3
            if abs(w1) < 1e-3:
                w1 = 1e-3
            def y_func(x): return -(w1/w2)*x - b0/w2
            x_vals = []
            for x in np.linspace(0, 8, 200):
                y = y_func(x)
                if 0 < y < 8:
                    x_vals.append(x)
            # 计算有效区间长度
            if len(x_vals) < 2:
                return VGroup()
            length = x_vals[-1] - x_vals[0]
            # 线段长度小于0.5时，逐渐变透明
            if length < 0.5:
                alpha = max(0.1, length / 0.5)  # 最低0.1透明度
            else:
                alpha = 1.0
            return axes.plot(y_func, color=YELLOW, x_range=[x_vals[0], x_vals[-1]], stroke_opacity=alpha)
        sep_line = always_redraw(get_line)
        self.add(sep_line)

        # 定义sigmoid和get_loss函数
        def sigmoid(z):
            return 1/(1+np.exp(-z))
        def get_loss():
            w1 = w_tracker.get_value()
            w2 = v_tracker.get_value()
            b0 = b_tracker.get_value()
            z = w1*X[:,0] + w2*X[:,1] + b0
            y_pred = sigmoid(z)
            loss = -np.mean(y*np.log(y_pred+1e-8)+(1-y)*np.log(1-y_pred+1e-8))
            return loss

        # 用于记录上一次损失值
        loss_history = ValueTracker(get_loss())

        # 连续不变计数器
        unchanged_count = [0]
        last_loss = [get_loss()]

        def get_loss_color():
            curr_loss = get_loss()
            if abs(curr_loss - last_loss[0]) < 1e-8:
                unchanged_count[0] += 1
            else:
                unchanged_count[0] = 0
            last_loss[0] = curr_loss
            # 连续10帧都未变化才变黄
            if unchanged_count[0] >= 10:
                return YELLOW
            else:
                return WHITE

        # 只保留动态损失值，放在坐标轴下方
        loss_text = always_redraw(lambda: Text(
            f"当前损失: {get_loss():.3f}", font_size=44, color=get_loss_color(), weight=BOLD
        ).next_to(axes, DOWN, buff=0.5))
        self.add(loss_text)

        lr = 0.1

        lr_text = always_redraw(lambda: Text(
            f"学习率：{lr}", font_size=44, color=WHITE, weight=BOLD
        ).next_to(axes, UP, buff=0.5))
        self.add(lr_text)

        # 新增：损失曲线坐标系和动态曲线
        steps = 200
        loss_history_list = []
        max_loss = get_loss()
        loss_axes = Axes(
            x_range=[0, steps, 10],
            y_range=[0, max_loss*1.5 if max_loss > 0 else 1.5, max_loss/5 if max_loss > 0 else 0.3],
            x_length=8,
            y_length=4,
        )
        loss_axes.next_to(axes, RIGHT, buff=1.2)
        loss_axes.align_to(axes, DOWN)
        loss_axes.shift(UP*1.3)  # 损失曲线图整体再向上
        # loss_axes.add_coordinates()  # 注释或删除这一行
        x_label = Text("训练步数", font_size=28)
        x_label.next_to(loss_axes.x_axis, DOWN, buff=0.3)
        y_label = Text("损失", font_size=28)
        y_label.next_to(loss_axes.y_axis, LEFT, buff=0.3)
        y_label.align_to(loss_axes.y_axis, UP)
        y_label.shift(UP*0.5)  # 标签也整体向上
        self.add(loss_axes, x_label, y_label)
        def get_loss_curve():
            if len(loss_history_list) < 2:
                return VGroup()
            x_vals = np.arange(len(loss_history_list))
            y_vals = np.array(loss_history_list)
            return loss_axes.plot_line_graph(
                x_values=x_vals,
                y_values=y_vals,
                add_vertex_dots=False,
                line_color=YELLOW
            )
        loss_curve = always_redraw(get_loss_curve)
        self.add(loss_curve)

        # 8. 梯度下降动画
        for i in range(steps):
            w1 = w_tracker.get_value()
            w2 = v_tracker.get_value()
            b0 = b_tracker.get_value()
            z = w1*X[:,0] + w2*X[:,1] + b0
            y_pred = sigmoid(z)
            grad_w1 = np.mean((y_pred - y) * X[:,0])
            grad_w2 = np.mean((y_pred - y) * X[:,1])
            grad_b = np.mean(y_pred - y)
            new_w1 = w1 - lr * grad_w1
            new_w2 = w2 - lr * grad_w2
            new_b = b0 - lr * grad_b
            self.play(
                w_tracker.animate.set_value(new_w1),
                v_tracker.animate.set_value(new_w2),
                b_tracker.animate.set_value(new_b),
                run_time=0.035
            )
            if i == 0:
                self.wait(0.2)
            # 记录损失
            loss_history_list.append(get_loss())
        self.wait(0.5)

        # 9. 结束前将损失值变黄
        self.remove(loss_text)
        final_loss_text = Text(
            f"当前损失: {get_loss():.3f}", font_size=44, color=YELLOW, weight=BOLD
        ).next_to(axes, DOWN, buff=0.5)
        self.add(final_loss_text)
        self.wait(5) 
