from manim import *
from manim_slides import Slide

from my_slides.shared import *


# ══════════════════════════════════════════════════════════════════
# Slide 15 — Overfitting
# ══════════════════════════════════════════════════════════════════
class Slide15Overfitting(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("overfitting")
        self.play(FadeIn(title), run_time=0.5)

        rng = np.random.default_rng(7)
        xs = np.linspace(-2, 2, 12)
        ys = 0.5 * xs + rng.normal(0, 0.35, 12)

        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2, 2, 1],
            x_length=7.5,
            y_length=4.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(DOWN * 0.2)

        dots = VGroup(
            *[
                Dot(axes.c2p(x, y), radius=0.09, color=WHITE, fill_opacity=0.85)
                for x, y in zip(xs, ys)
            ]
        )
        self.play(Create(axes), run_time=0.6)
        self.play(FadeIn(dots), run_time=0.6)
        self.next_slide()

        good_fit = axes.plot(
            lambda x: 0.5 * x, x_range=[-2.3, 2.3], color=C_GREEN, stroke_width=2.5
        )
        good_lbl = Text("good generalization", font_size=22, color=C_GREEN)
        good_lbl.to_corner(UL).shift(DOWN * 1.5 + RIGHT * 0.3)
        self.play(Create(good_fit), FadeIn(good_lbl), run_time=0.7)
        self.next_slide()

        overfit_coeffs = np.polyfit(xs, ys, deg=11)
        overfit_poly = np.poly1d(overfit_coeffs)
        bad_fit = axes.plot(
            overfit_poly, x_range=[-1.95, 1.95], color=C_RED, stroke_width=2.5
        )
        bad_lbl = Text(
            "overfitting — zero training error,\nbad generalization",
            font_size=22,
            color=C_RED,
        )
        bad_lbl.to_corner(UR).shift(DOWN * 1.5 + LEFT * 0.3)
        self.play(Create(bad_fit), FadeIn(bad_lbl), run_time=0.8)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
