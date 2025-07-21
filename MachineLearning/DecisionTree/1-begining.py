from manim import *

class DecisionTreeTransition(Scene):
    def construct(self):
        self.camera.background_color = "#282c34"
        english_text = "DecisionTree"
        chinese_text = "决策树"
        english_font = "Century Gothic"
        chinese_font = "SimHei"

        cursor = Rectangle(width=0.06, height=1.2, fill_color=WHITE, fill_opacity=1)
        self.play(Create(cursor))
        self.play(Blink(cursor, run_time=2))

        # 1. 英文逐字生长
        char_mobs = VGroup()
        for i, char in enumerate(english_text):
            new_char = Text(char, font_size=96, color=BLUE_C, font=english_font)
            char_mobs.add(new_char)
            char_mobs.arrange(RIGHT, buff=0.05)
            if len(char_mobs) > 1:
                for mob in char_mobs[1:]:
                    mob.align_to(char_mobs[0], DOWN)
            self.play(
                FadeIn(new_char, shift=UP*0.3),
                char_mobs.animate.move_to(ORIGIN),
                cursor.animate.next_to(char_mobs, RIGHT, buff=0.1),
                run_time=0.15
            )
        self.play(Blink(cursor, run_time=1))

        # 2. 英文逐字删除
        for _ in range(len(english_text)):
            last_char = char_mobs[-1]
            char_mobs.remove(last_char)
            if char_mobs:
                anim_cursor = cursor.animate.next_to(char_mobs, RIGHT, buff=0.1)
            else:
                anim_cursor = cursor.animate.move_to(ORIGIN)
            self.play(
                FadeOut(last_char, shift=DOWN*0.3),
                char_mobs.animate.move_to(ORIGIN),
                anim_cursor,
                run_time=0.05
            )
        self.play(Blink(cursor, run_time=1))

        # 3. 中文逐字生长
        for char in chinese_text:
            new_char = Text(char, font_size=96, color=GREEN_C, font=chinese_font)
            char_mobs.add(new_char)
            char_mobs.arrange(RIGHT, buff=0.05)
            self.play(
                FadeIn(new_char, shift=UP*0.3),
                char_mobs.animate.move_to(ORIGIN),
                cursor.animate.next_to(char_mobs, RIGHT, buff=0.1),
                run_time=0.25
            )
        self.play(Blink(cursor, run_time=1))

        # 4. 结尾动画
        self.play(FadeOut(cursor))
        self.play(char_mobs.animate.scale(1.2).set_color(YELLOW), run_time=0.5)
        self.play(char_mobs.animate.scale(1/1.2).set_color(GREEN_C), run_time=0.5)
        self.wait(1)
