from manim import *
from manim_slides import Slide

from my_slides.shared import *


# ══════════════════════════════════════════════════════════════════
# Slide 14 — Memorization
# ══════════════════════════════════════════════════════════════════
class Slide14Memorization(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("memorization")
        self.play(FadeIn(title), run_time=0.5)

        rng = np.random.default_rng(42)
        rand_xs = np.linspace(-1.8, 1.8, 6)
        rand_ys = rng.uniform(-1.4, 1.4, 6)
        coeffs = np.polyfit(rand_xs, rand_ys, deg=5)
        poly = np.poly1d(coeffs)

        ax_l = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2, 2, 1],
            x_length=4.5,
            y_length=3.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.2},
            tips=False,
        ).shift(LEFT * 2.9 + DOWN * 0.4)
        lbl_l = Text("memorized", font_size=22, color=C_RED).next_to(
            ax_l, UP, buff=0.15
        )

        ax_r = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2, 2, 1],
            x_length=4.5,
            y_length=3.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.2},
            tips=False,
        ).shift(RIGHT * 2.9 + DOWN * 0.4)
        lbl_r = Text("learned the function", font_size=22, color=C_GREEN).next_to(
            ax_r, UP, buff=0.15
        )

        self.play(
            Create(ax_l),
            FadeIn(lbl_l),
            Create(ax_r),
            FadeIn(lbl_r),
            run_time=0.7,
        )

        train_dots = VGroup(
            *[
                Dot(ax_l.c2p(x, y), radius=0.1, color=C_RED)
                for x, y in zip(rand_xs, rand_ys)
            ]
        )
        fit_l = ax_l.plot(poly, x_range=[-1.75, 1.75], color=C_YELLOW, stroke_width=2)

        lin_pts_y = 0.7 * rand_xs + 0.1 + rng.normal(0, 0.15, len(rand_xs))
        lin_dots = VGroup(
            *[
                Dot(ax_r.c2p(x, y), radius=0.1, color=C_GREEN)
                for x, y in zip(rand_xs, lin_pts_y)
            ]
        )
        fit_r = ax_r.plot(
            lambda x: 0.7 * x + 0.1, x_range=[-2.3, 2.3], color=C_YELLOW, stroke_width=2
        )

        self.play(
            FadeIn(train_dots),
            Create(fit_l),
            FadeIn(lin_dots),
            Create(fit_r),
            run_time=0.8,
        )
        self.next_slide()

        # New point — memorized model fails
        new_x = 2.1
        clipped_y = float(np.clip(poly(new_x), -1.8, 1.8))
        new_dot_l = Dot(ax_l.c2p(new_x, clipped_y), radius=0.13, color=C_ORANGE)
        fail_lbl = Text("???", font_size=20, color=C_ORANGE).next_to(
            new_dot_l, UP, buff=0.1
        )
        self.play(FadeIn(new_dot_l), FadeIn(fail_lbl), run_time=0.5)
        self.next_slide()

        # New point — linear model extrapolates
        new_dot_r = Dot(ax_r.c2p(new_x, 0.7 * new_x + 0.1), radius=0.13, color=C_GREEN)
        extrap_lbl = Text("extrapolates!", font_size=20, color=C_GREEN).next_to(
            new_dot_r, UP, buff=0.1
        )
        self.play(FadeIn(new_dot_r), FadeIn(extrap_lbl), run_time=0.5)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
