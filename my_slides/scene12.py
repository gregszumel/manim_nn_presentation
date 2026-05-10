from manim import *
from manim_slides import Slide

from my_slides.shared import *


# ══════════════════════════════════════════════════════════════════
# Slide 12 — Gradient Descent Loop
# ══════════════════════════════════════════════════════════════════
class Slide12GradientLoop(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("the training loop")
        self.play(FadeIn(title), run_time=0.5)

        steps = [
            "show example",
            "compute error",
            "nudge weights toward correct output",
            "repeat",
        ]
        boxes = VGroup()
        for step in steps:
            box = RoundedRectangle(
                corner_radius=0.15,
                width=5.5,
                height=0.75,
                stroke_color=C_INPUT,
                stroke_width=1.5,
                fill_color=DARK_BG,
                fill_opacity=0.9,
            )
            lbl = Text(step, font_size=26).move_to(box)
            boxes.add(VGroup(box, lbl))
        boxes.arrange(DOWN, buff=0.45).center().shift(DOWN * 0.2)

        arrows = VGroup(
            *[
                Arrow(
                    boxes[i].get_bottom(),
                    boxes[i + 1].get_top(),
                    buff=0.05,
                    stroke_width=2,
                    color=C_GREY,
                )
                for i in range(len(boxes) - 1)
            ]
        )
        loop_arrow = CurvedArrow(
            boxes[-1].get_right() + UP * 0.1,
            boxes[0].get_right() + DOWN * 0.1,
            angle=-PI / 2,
            color=C_ORANGE,
            stroke_width=2,
        )

        for box in boxes:
            self.play(FadeIn(box), run_time=0.4)
            self.next_slide()

        self.play(
            LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2), run_time=0.6
        )
        self.play(Create(loop_arrow), run_time=0.6)
        self.next_slide()

        warning = Text(
            "push weights toward what we saw → eventually memorizes",
            font_size=22,
            color=C_RED,
        )
        warning.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(warning, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
