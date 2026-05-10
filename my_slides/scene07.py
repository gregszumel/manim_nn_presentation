from manim import *
from manim_slides import Slide
from my_slides import *


# ══════════════════════════════════════════════════════════════════
# Slide 7 — Activation Functions
# ══════════════════════════════════════════════════════════════════
class Slide07Activations(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("activation functions")
        self.play(FadeIn(title), run_time=0.5)

        eq1 = MathTex(r"\mathbf{h} = \sigma(\mathbf{W_0}\,\mathbf{i})", font_size=38)
        eq2 = MathTex(
            r"\mathbf{o} = \mathbf{W_1}\,\sigma(\mathbf{W_0}\,\mathbf{i})", font_size=38
        )
        VGroup(eq1, eq2).arrange(DOWN, buff=0.5).shift(LEFT * 1.5 + UP * 0.6)

        self.play(Write(eq1), run_time=0.7)
        self.next_slide()
        self.play(Write(eq2), run_time=0.7)
        self.next_slide()

        no_collapse = Text(
            "σ blocks the collapse — layers stay distinct", font_size=26, color=C_GREEN
        )
        no_collapse.shift(LEFT * 1.5 + DOWN * 0.8)
        self.play(FadeIn(no_collapse, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-0.3, 2, 0.5],
            x_length=3.5,
            y_length=2.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(RIGHT * 3.2 + DOWN * 0.4)
        relu = axes.plot(
            lambda x: max(0.0, x), x_range=[-2, 2], color=C_ORANGE, stroke_width=2.5
        )
        relu_label = Text("ReLU  —  fires past threshold", font_size=20, color=C_ORANGE)
        relu_label.next_to(axes, DOWN, buff=0.2)

        self.play(Create(axes), run_time=0.5)
        self.play(Create(relu), FadeIn(relu_label), run_time=0.7)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
