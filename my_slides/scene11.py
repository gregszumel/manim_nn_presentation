from manim import *
from manim_slides import Slide

from my_slides.shared import *


# ══════════════════════════════════════════════════════════════════
# Slide 11 — Loss Landscape
# ══════════════════════════════════════════════════════════════════
class Slide11LossLandscape(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("how do we train?")
        self.play(FadeIn(title), run_time=0.5)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 5, 1],
            x_length=6.5,
            y_length=4.0,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(DOWN * 0.4)

        x_lbl = Text("weights", font_size=22, color=C_GREY).next_to(
            axes.get_x_axis(), DOWN, buff=0.3
        )
        y_lbl = Text("loss", font_size=22, color=C_GREY).next_to(
            axes.get_y_axis(), LEFT, buff=0.3
        )
        loss_curve = axes.plot(
            lambda x: x**2 + 0.3, x_range=[-2.8, 2.8], color=C_INPUT, stroke_width=2.5
        )

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.7)
        self.play(Create(loss_curve), run_time=0.6)
        self.next_slide()

        sx = 2.5
        dot = Dot(axes.c2p(sx, sx**2 + 0.3), radius=0.14, color=C_YELLOW)
        self.play(FadeIn(dot), run_time=0.4)
        self.next_slide()

        grad_end_x = sx - 0.8
        grad_arrow = Arrow(
            axes.c2p(sx, sx**2 + 0.3),
            axes.c2p(grad_end_x, grad_end_x**2 + 0.3),
            buff=0.05,
            stroke_width=2,
            color=C_ORANGE,
        )
        grad_lbl = MathTex(r"-\frac{d\mathcal{L}}{dw}", font_size=28, color=C_ORANGE)
        grad_lbl.next_to(grad_arrow, UP, buff=0.15)
        self.play(Create(grad_arrow), FadeIn(grad_lbl), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(grad_arrow), FadeOut(grad_lbl), run_time=0.3)
        for nx in [1.8, 1.1, 0.5, 0.1]:
            self.play(dot.animate.move_to(axes.c2p(nx, nx**2 + 0.3)), run_time=0.35)

        bottom = Text(
            "gradient descent — take small steps downhill", font_size=24, color=C_YELLOW
        )
        bottom.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(bottom, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
