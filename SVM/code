from manim import (
    ThreeDScene, Axes, VGroup, Dot, FadeIn, FadeOut, Create, ValueTracker,
    always_redraw, Line, YELLOW, RED, BLUE, WHITE, Surface, ThreeDAxes, Dot3D,
    DEGREES, MoveToTarget, Text, Transform
)
from manim.utils.rate_functions import linear
import numpy as np

class SVMKernelDemo(ThreeDScene):
    def construct(self):
        # 1. 生成二维数据
        np.random.seed(0)
        n = 20
        # 红色点：外圈（半径2）
        theta_red = np.linspace(0, 2 * np.pi, n, endpoint=False)
        x_red = np.stack([2 * np.cos(theta_red), 2 * np.sin(theta_red)], axis=1) + np.random.normal(0, 0.1, (n, 2))
        # 蓝色点：内圈（半径0.8）
        theta_blue = np.linspace(0, 2 * np.pi, n, endpoint=False)
        x_blue = np.stack([0.8 * np.cos(theta_blue), 0.8 * np.sin(theta_blue)], axis=1) + np.random.normal(0, 0.08, (n, 2))

        # 2. 绘制二维点
        axes2d = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=6, y_length=6, axis_config={"color": WHITE}
        )
        self.play(Create(axes2d))
        red_dots = VGroup(*[Dot(axes2d.coords_to_point(*p), color=RED) for p in x_red])
        blue_dots = VGroup(*[Dot(axes2d.coords_to_point(*p), color=BLUE) for p in x_blue])
        self.play(FadeIn(red_dots), FadeIn(blue_dots))
        self.wait(2)

        # 3. 尝试二维分割线（动态切线+问号）
        r = 1.2
        tracker = ValueTracker(0)
        fixed_length = 5

        def get_tangent():
            theta = tracker.get_value()
            x0, y0 = r * np.cos(theta), r * np.sin(theta)
            # 切线方向向量（与半径垂直）
            dx, dy = -y0, x0
            norm = np.hypot(dx, dy)
            dx, dy = dx / norm, dy / norm
            p1 = axes2d.coords_to_point(x0 + dx * fixed_length / 2, y0 + dy * fixed_length / 2)
            p2 = axes2d.coords_to_point(x0 - dx * fixed_length / 2, y0 - dy * fixed_length / 2)
            return Line(p1, p2, color=YELLOW, stroke_width=4)

        tangent_line = always_redraw(lambda: get_tangent())
        self.play(Create(tangent_line))
        self.wait(0.5)

        # 切线绕内圆一圈
        self.play(tracker.animate.set_value(2 * np.pi), run_time=5 , rate_func=linear)
        self.wait(0.5)

        # 黄线变成问号，并移动到右上角
        theta_final = tracker.get_value()
        x0, y0 = r * np.cos(theta_final), r * np.sin(theta_final)
        center = axes2d.coords_to_point(x0, y0)
        # 目标位置：右上角空白处
        target_pos = axes2d.coords_to_point(2.5, 2.5)
        question = Text("?", font_size=60, color=YELLOW)
        question.move_to(center)
        self.play(Transform(tangent_line, question), run_time=1)
        self.remove(tangent_line)
        self.add(question)
        # 问号移动到右上角
        self.play(question.animate.move_to(target_pos), run_time=0.8)
        self.wait(0.5)
        # 问号和2D点一起淡出
        self.play(FadeOut(question), FadeOut(red_dots), FadeOut(blue_dots))

        # 4. 升维到三维（2D点已淡出，只加3D）
        axes3d = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[0, 10, 2],
            x_length=6, y_length=6, z_length=4
        )
        self.play(Create(axes3d))
        # 用z = x^2 + y^2升维
        red_3d = VGroup(*[Dot3D(axes3d.coords_to_point(p[0], p[1], p[0]**2 + p[1]**2), color=RED) for p in x_red])
        blue_3d = VGroup(*[Dot3D(axes3d.coords_to_point(p[0], p[1], p[0]**2 + p[1]**2), color=BLUE) for p in x_blue])
        self.play(FadeIn(red_3d), FadeIn(blue_3d))
        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES)
        self.wait(1)

        # 计算3D红点和蓝点的平均z值
        red_zs = np.array([p[0]**2 + p[1]**2 for p in x_red])
        blue_zs = np.array([p[0]**2 + p[1]**2 for p in x_blue])
        red_z_mean = red_zs.mean()
        blue_z_mean = blue_zs.mean()
        plane_z = (red_z_mean + blue_z_mean) / 2

        # 5. 三维分割平面（z为红蓝点平均z的中值，颜色为蓝色）
        plane = Surface(
            lambda u, v: axes3d.coords_to_point(u, v, plane_z),
            u_range=[-3, 3], v_range=[-3, 3], fill_opacity=0.5, color=BLUE
        )
        self.play(Create(plane))
        self.wait(1)

        # 视角切换到平面正面（让分割平面变成直线）
        self.move_camera(phi=86 * DEGREES, theta=0 * DEGREES, run_time=2)  # 俯视，分割平面变成直线
        self.wait(3)


        # 6. 降维回二维，显示分割曲线
        self.move_camera(phi=0 * DEGREES, theta=0 * DEGREES, run_time=2)  # 重置相机角度
        self.wait(1)
        # 保持三维坐标系和点，只淡出分割平面并同时显示二维分割线
        circle = axes2d.plot_implicit_curve(lambda x, y: x**2 + y**2 - 3.0, color=YELLOW)
        self.play(FadeOut(plane), Create(circle), run_time=2)
        self.wait(4 )
