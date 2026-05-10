from manim import *
from manim_slides import Slide
from my_slides.shared import *


# ══════════════════════════════════════════════════════════════════
# Slide 18 — Prompt as Bias Term
# ══════════════════════════════════════════════════════════════════
class Slide18PromptBias(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("prompting as a bias term")
        self.play(FadeIn(title), run_time=0.5)

        eq_base = MathTex(
            r"o = \sigma\!\Bigl(\sum_i w_i\,a_i + b\Bigr)",
            font_size=46,
        ).shift(UP * 0.9)
        self.play(Write(eq_base), run_time=0.8)
        self.next_slide()

        bias_box = SurroundingRectangle(eq_base, buff=0.08, color=C_ORANGE)
        bias_lbl = Text("bias term", font_size=22, color=C_ORANGE).next_to(
            bias_box, DOWN, buff=0.2
        )
        self.play(Create(bias_box), FadeIn(bias_lbl), run_time=0.5)
        self.next_slide()

        arrow = Arrow(
            ORIGIN + DOWN * 0.5,
            ORIGIN + DOWN * 1.3,
            buff=0.05,
            stroke_width=2,
            color=C_ORANGE,
        )
        eq_prompt = MathTex(
            r"o = \sigma\!\Bigl(\sum_i w_i\,a_i + b + b_{\text{prompt}}\Bigr)",
            font_size=38,
        ).shift(DOWN * 1.0)
        prompt_lbl = Text(
            "prompt tokens add an effective bias shift", font_size=24, color=C_ORANGE
        ).next_to(eq_prompt, DOWN, buff=0.35)

        self.play(FadeOut(bias_box), FadeOut(bias_lbl), Create(arrow), run_time=0.4)
        self.play(Write(eq_prompt), run_time=0.8)
        self.play(FadeIn(prompt_lbl), run_time=0.5)
        self.next_slide()

        change_lbl = Text(
            "change the prompt → change the bias → change the output",
            font_size=22,
            color=C_YELLOW,
        )
        change_lbl.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(change_lbl, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
