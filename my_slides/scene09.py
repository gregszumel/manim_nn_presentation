from manim import *
from manim_slides import Slide
from my_slides.shared import *


# ══════════════════════════════════════════════════════════════════
# Slide 9 — Universal Function Approximators
# ══════════════════════════════════════════════════════════════════
class Slide09UniversalApprox(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("universal function approximators")
        self.play(FadeIn(title), run_time=0.5)

        rng = np.random.default_rng(42)
        rand_xs = np.linspace(-1.8, 1.8, 6)
        rand_ys = rng.uniform(-1.4, 1.4, 6)
        rand_coeffs = np.polyfit(rand_xs, rand_ys, deg=5)
        rand_poly = np.poly1d(rand_coeffs)

        specs = [
            ("linear", lambda x: 0.6 * x, C_INPUT, False),
            ("quadratic", lambda x: x**2 - 1.0, C_GREEN, False),
            ("exponential", lambda x: np.exp(0.8 * x) - 1.5, C_ORANGE, False),
            ("random", None, C_RED, True),
        ]

        all_axes, all_true, all_nn = [], [], []

        for i, (name, fn, color, is_rand) in enumerate(specs):
            col_i, row_i = i % 2, i // 2
            ax = Axes(
                x_range=[-2, 2, 1],
                y_range=[-2.5, 2.5, 1],
                x_length=3.0,
                y_length=2.5,
                axis_config={"stroke_width": 1.0, "stroke_color": C_GREY},
                tips=False,
            ).shift(RIGHT * (col_i * 3.6 - 1.8) + DOWN * (row_i * 3.2 - 0.6))
            lbl = Text(name, font_size=18, color=color).next_to(ax, UP, buff=0.1)

            if not is_rand:
                true_mob = ax.plot(
                    fn, x_range=[-1.9, 1.9], color=color, stroke_width=2.5
                )
                nn_mob = DashedVMobject(
                    ax.plot(
                        lambda x, f=fn: f(x) + 0.07 * np.sin(4 * x),
                        x_range=[-1.9, 1.9],
                        color=WHITE,
                        stroke_width=1.5,
                    ),
                    num_dashes=30,
                    dashed_ratio=0.5,
                )
            else:
                true_mob = VGroup(
                    *[
                        Dot(ax.c2p(x, y), radius=0.07, color=C_RED, fill_opacity=0.85)
                        for x, y in zip(rand_xs, rand_ys)
                    ]
                )
                nn_mob = DashedVMobject(
                    ax.plot(
                        rand_poly, x_range=[-1.75, 1.75], color=WHITE, stroke_width=1.5
                    ),
                    num_dashes=30,
                    dashed_ratio=0.5,
                )

            all_axes.append((ax, lbl))
            all_true.append(true_mob)
            all_nn.append(nn_mob)

        for ax, lbl in all_axes:
            self.play(Create(ax), FadeIn(lbl), run_time=0.35)

        for mob in all_true:
            anim = FadeIn(mob) if isinstance(mob, VGroup) else Create(mob)
            self.play(anim, run_time=0.45)

        self.next_slide()

        for mob in all_nn:
            self.play(Create(mob), run_time=0.4)

        punchline = Text(
            "NNs can approximate any function", font_size=28, color=C_YELLOW
        )
        punchline.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(punchline, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
