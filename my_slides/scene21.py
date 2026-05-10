from manim import *
from manim_slides import Slide
from my_slides.shared import *


# ══════════════════════════════════════════════════════════════════
# Slide 21 — Wrap-up
# ══════════════════════════════════════════════════════════════════
class Slide21Wrapup(Slide):
    def construct(self):
        self.next_slide()

        title = Text("that's a wrap", font_size=44, slant=ITALIC)
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=UP * 0.1), run_time=0.8)

        underline = Line(
            title.get_left() + DOWN * 0.15,
            title.get_right() + DOWN * 0.15,
            stroke_color=WHITE,
            stroke_width=1,
            stroke_opacity=0.4,
        )
        self.play(Create(underline), run_time=0.4)
        self.next_slide()

        goals = [
            "neural networks are just math — we can reason about them  ✓",
            "evaluations are critical — and hard to get right  ✓",
            "prompting is pseudo-finetuning — eval your prompts  ✓",
        ]
        goal_mobs = VGroup(*[Text(g, font_size=26, color=C_GREEN) for g in goals])
        goal_mobs.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        goal_mobs.next_to(underline, DOWN, buff=0.55).to_edge(LEFT, buff=1.0)
        for m in goal_mobs:
            m.set_opacity(0)
        self.add(goal_mobs)

        for m in goal_mobs:
            self.play(m.animate.set_opacity(1.0), run_time=0.45)
            self.next_slide()

        summer = Text(
            "ML summer series — zero to your own LLM in 12 weeks",
            font_size=26,
            color=C_YELLOW,
        ).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(summer, shift=UP * 0.1), run_time=0.7)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
