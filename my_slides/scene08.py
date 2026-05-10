from manim import *
from manim_slides import Slide

from my_slides.shared import *


# ══════════════════════════════════════════════════════════════════
# Slide 8 — XOR Problem
# ══════════════════════════════════════════════════════════════════
class Slide08XOR(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("the XOR problem")
        self.play(FadeIn(title), run_time=0.5)

        axes = Axes(
            x_range=[-0.4, 1.6, 1],
            y_range=[-0.4, 1.6, 1],
            x_length=4.5,
            y_length=4.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(LEFT * 2.2 + DOWN * 0.3)

        x_lbl = MathTex("x_0", font_size=26).next_to(axes.get_x_axis(), DOWN, buff=0.2)
        y_lbl = MathTex("x_1", font_size=26).next_to(axes.get_y_axis(), LEFT, buff=0.2)
        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.7)
        self.next_slide()

        xor_data = [((0, 0), 0), ((1, 1), 0), ((0, 1), 1), ((1, 0), 1)]
        dots = []
        for (x, y), cls in xor_data:
            color = C_RED if cls == 0 else C_INPUT
            d = Dot(axes.c2p(x, y), radius=0.16, color=color, fill_opacity=0.9)
            dots.append(d)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.3), run_time=0.8)
        self.next_slide()

        fail_lines = [
            axes.plot(
                lambda x: 0.5 + 0 * x,
                color=C_GREY,
                stroke_width=1.5,
                stroke_opacity=0.6,
            ),
            axes.plot(lambda x: x, color=C_GREY, stroke_width=1.5, stroke_opacity=0.6),
            axes.plot(
                lambda x: -x + 1, color=C_GREY, stroke_width=1.5, stroke_opacity=0.6
            ),
        ]
        fail_label = Text("no line separates these", font_size=24, color=C_RED)
        fail_label.shift(RIGHT * 3.0 + UP * 0.5)

        for fl in fail_lines:
            self.play(Create(fl), run_time=0.5)
            self.next_slide()
            self.play(fl.animate.set_stroke(opacity=0.2), run_time=0.3)

        self.play(FadeIn(fail_label, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        solution = Text("add hidden layer + activation", font_size=24, color=C_GREEN)
        solution.next_to(fail_label, DOWN, buff=0.4)
        result = Text("→  now separable", font_size=24, color=C_GREEN)
        result.next_to(solution, DOWN, buff=0.2)

        self.play(FadeIn(solution), run_time=0.5)
        self.play(FadeIn(result), run_time=0.5)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
