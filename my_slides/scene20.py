from manim import *
from manim_slides import Slide
from my_slides.shared import *


# ══════════════════════════════════════════════════════════════════
# Slide 20 — Evaluate Your Prompts
# ══════════════════════════════════════════════════════════════════
class Slide20EvaluatePrompts(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("evaluate your prompts")
        self.play(FadeIn(title), run_time=0.5)

        buckets_info = [
            ("prompt dev set", C_INPUT),
            ("held-out eval set", C_GREEN),
            ("test set", C_ORANGE),
        ]
        buckets = VGroup()
        for i, (lbl, col) in enumerate(buckets_info):
            rect = RoundedRectangle(
                corner_radius=0.1,
                width=2.7,
                height=0.9,
                stroke_color=col,
                fill_color=DARK_BG,
                fill_opacity=0.85,
            )
            rect.shift(LEFT * (2.7 - i * 2.7) + UP * 1.0)
            text = Text(lbl, font_size=19, color=col).move_to(rect)
            buckets.add(VGroup(rect, text))
        self.play(FadeIn(buckets), run_time=0.7)
        self.next_slide()

        warning = Text(
            "tune on your dev set.\nnever peek at eval until you're done.",
            font_size=28,
            color=C_RED,
            line_spacing=1.4,
        ).shift(DOWN * 0.5)
        self.play(FadeIn(warning, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        final = Text(
            "if you're tuning a prompt, you need a holdout —\nor you're just overfitting to your examples",
            font_size=24,
            color=C_YELLOW,
            line_spacing=1.4,
        ).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(final, shift=UP * 0.1), run_time=0.7)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
