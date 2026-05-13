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

        # Same seed / data as scene09 for visual continuity
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

        # NN perfect fit within training range
        fit = axes.plot(poly, x_range=[-1.75, 1.75], color=C_YELLOW, stroke_width=2.5)
        fit_lbl = Text("NN fits perfectly", font_size=24, color=C_YELLOW)
        fit_lbl.to_corner(UR).shift(DOWN * 1.5 + LEFT * 0.3)
        self.play(Create(fit), run_time=0.9)
        self.play(FadeIn(fit_lbl), run_time=0.4)
        self.next_slide()

        # ── Introduce a new test point outside the training range ──
        new_x = 2.0
        nn_y = float(np.clip(poly(new_x), -1.9, 1.9))
        # Genuinely random independent draw — no relation to the training pattern
        true_y = float(rng.uniform(-1.4, 1.4))

        question = Text("what about a new point?", font_size=26, color=C_ORANGE)
        question.to_edge(DOWN, buff=0.5)
        v_line = DashedLine(
            axes.c2p(new_x, -1.85),
            axes.c2p(new_x,  1.85),
            color=C_GREY, stroke_width=1.2, dash_length=0.1,
        )
        self.play(FadeIn(question, shift=UP * 0.1), Create(v_line), run_time=0.5)
        self.next_slide()

        # NN prediction dot (where the polynomial extrapolates to)
        nn_dot = Dot(axes.c2p(new_x, nn_y), radius=0.13, color=C_YELLOW)
        nn_lbl = Text("NN predicts", font_size=20, color=C_YELLOW).next_to(
            nn_dot, LEFT, buff=0.15
        )
        self.play(FadeIn(nn_dot), FadeIn(nn_lbl), run_time=0.5)
        self.next_slide()

        # Actual new random draw — different value, because randomness has no pattern
        true_dot = Dot(axes.c2p(new_x, true_y), radius=0.13, color=C_RED)
        true_lbl = Text("new random draw", font_size=20, color=C_RED).next_to(
            true_dot, LEFT, buff=0.15
        )
        self.play(FadeIn(true_dot), FadeIn(true_lbl), run_time=0.5)
        self.next_slide()

        # Gap arrow showing the mismatch
        gap = DoubleArrow(
            axes.c2p(new_x, nn_y),
            axes.c2p(new_x, true_y),
            buff=0.12,
            color=C_ORANGE,
            stroke_width=2.5,
        )
        self.play(Create(gap), run_time=0.5)
        self.next_slide()

        # Punchline: it memorized, it didn't learn
        punchline = Text(
            "it didn't learn randomness — it memorized the training points",
            font_size=24,
            color=C_ORANGE,
        )
        punchline.to_edge(DOWN, buff=0.4)
        self.play(FadeOut(question), FadeIn(punchline, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
