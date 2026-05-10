from manim import *
from manim_slides import Slide
from my_slides.shared import *


# ══════════════════════════════════════════════════════════════════
# Slide 16 — Train / Val / Test
# ══════════════════════════════════════════════════════════════════
class Slide16TrainValTest(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("train  /  val  /  test")
        self.play(FadeIn(title), run_time=0.5)

        rng = np.random.default_rng(0)
        pool = VGroup(
            *[
                Dot(radius=0.09, color=C_GREY, fill_opacity=0.7).shift(
                    RIGHT * rng.uniform(-0.8, 0.8) + UP * rng.uniform(-0.3, 0.3)
                )
                for _ in range(18)
            ]
        ).shift(LEFT * 4.5 + UP * 1.8)
        pool_lbl = Text("data", font_size=20, color=C_GREY).next_to(pool, UP, buff=0.15)
        self.play(FadeIn(pool), FadeIn(pool_lbl), run_time=0.6)
        self.next_slide()

        buckets_info = [("train", C_INPUT), ("val", C_GREEN), ("test", C_ORANGE)]
        buckets = VGroup()
        for i, (lbl, col) in enumerate(buckets_info):
            rect = RoundedRectangle(
                corner_radius=0.1,
                width=2.0,
                height=0.85,
                stroke_color=col,
                fill_color=DARK_BG,
                fill_opacity=0.85,
            )
            rect.shift(LEFT * (2.2 - i * 2.5) + UP * 1.8)
            text = Text(lbl, font_size=22, color=col).move_to(rect)
            buckets.add(VGroup(rect, text))
        self.play(FadeIn(buckets), run_time=0.6)
        self.next_slide()

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 2.2, 0.5],
            x_length=7.5,
            y_length=3.0,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(DOWN * 1.7)

        x_lbl = Text("training steps", font_size=20, color=C_GREY).next_to(
            axes.get_x_axis(), DOWN, buff=0.2
        )
        y_lbl = Text("loss", font_size=20, color=C_GREY).next_to(
            axes.get_y_axis(), LEFT, buff=0.2
        )

        train_curve = axes.plot(
            lambda t: 1.8 * np.exp(-0.35 * t) + 0.1,
            x_range=[0, 10],
            color=C_INPUT,
            stroke_width=2.5,
        )
        val_curve = axes.plot(
            lambda t: 1.8 * np.exp(-0.28 * t) + 0.3 + 0.04 * max(0, t - 4) ** 2,
            x_range=[0, 10],
            color=C_ORANGE,
            stroke_width=2.5,
        )

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.7)
        self.play(Create(train_curve), run_time=0.7)
        train_lbl = Text("train", font_size=20, color=C_INPUT).next_to(
            axes.c2p(9.8, 0.2), RIGHT, buff=0.05
        )
        self.play(FadeIn(train_lbl), run_time=0.3)
        self.next_slide()

        self.play(Create(val_curve), run_time=0.8)
        val_lbl = Text("val", font_size=20, color=C_ORANGE).next_to(
            axes.c2p(9.8, 0.9), RIGHT, buff=0.05
        )
        self.play(FadeIn(val_lbl), run_time=0.3)
        self.next_slide()

        vline = axes.get_vertical_line(axes.c2p(4, 0), color=C_RED, stroke_width=2)
        stop_lbl = Text("stop here", font_size=20, color=C_RED).next_to(
            axes.c2p(4, 1.4), RIGHT, buff=0.1
        )
        self.play(Create(vline), FadeIn(stop_lbl), run_time=0.5)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
