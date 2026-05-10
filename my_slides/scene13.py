from manim import *
from manim_slides import Slide
from my_slides.shared import *


# ══════════════════════════════════════════════════════════════════
# Slide 13 — Back to the Random Function
# ══════════════════════════════════════════════════════════════════
class Slide13RandomFunction(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("back to the random function…")
        self.play(FadeIn(title), run_time=0.5)

        rng = np.random.default_rng(42)
        rand_xs = np.linspace(-1.8, 1.8, 6)
        rand_ys = rng.uniform(-1.4, 1.4, 6)
        coeffs = np.polyfit(rand_xs, rand_ys, deg=5)
        poly = np.poly1d(coeffs)

        axes = Axes(
            x_range=[-2.2, 2.2, 1],
            y_range=[-2, 2, 1],
            x_length=6.5,
            y_length=4.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(DOWN * 0.3)

        dots = VGroup(
            *[
                Dot(axes.c2p(x, y), radius=0.11, color=C_RED, fill_opacity=0.9)
                for x, y in zip(rand_xs, rand_ys)
            ]
        )
        self.play(Create(axes), run_time=0.6)
        self.play(FadeIn(dots), run_time=0.5)
        self.next_slide()

        fit = axes.plot(poly, x_range=[-1.75, 1.75], color=C_YELLOW, stroke_width=2.5)
        fit_lbl = Text("NN fits perfectly", font_size=24, color=C_YELLOW)
        fit_lbl.to_corner(UR).shift(DOWN * 1.5 + LEFT * 0.3)
        self.play(Create(fit), run_time=0.9)
        self.play(FadeIn(fit_lbl), run_time=0.4)
        self.next_slide()

        question = Text(
            "wait — is it approximating randomness?", font_size=28, color=C_ORANGE
        )
        question.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(question, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
