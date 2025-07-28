# 现在最新的manim不支持“from manim import *”了，所以我在mymanim.py中from manim import 所有必要项，这样我就可以“from mymanim import *”来包含所有项了

from manim import (
    # 场景
    Scene, ThreeDScene, MovingCameraScene, ZoomedScene,
    # 基本图形
    Circle, Square, Rectangle, Line, Arrow, Dot, Ellipse, Polygon, Arc, Annulus, Sector, 
    # 三维
    ThreeDAxes, Surface, Sphere, Cube, Dot3D, 
    # 坐标轴
    Axes, NumberPlane, 
    # 颜色
    WHITE, BLACK, RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, PINK, GOLD, TEAL, MAROON, 
    # 方向
    UP, DOWN, LEFT, RIGHT, IN, OUT, 
    # 动画
    Create, FadeIn, FadeOut, Write, Transform, ReplacementTransform, ApplyMethod, ApplyFunction, 
    # 文字
    Text, MathTex, Tex, MarkupText, 
    # 组
    VGroup, Group, 
    # 相机
    ThreeDCamera, Camera, 
    # 角度
    DEGREES, PI, TAU,UR,DR,
    # 其他
    ValueTracker, always_redraw,
    # 交互
    smooth,
    # 画布尺寸
    ORIGIN,config,
)
