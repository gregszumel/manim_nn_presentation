from manim import *
from manim_slides import Slide


# ══════════════════════════════════════════════════════════════════
# Slide 1 — Goals
# ══════════════════════════════════════════════════════════════════
class Slide01Goals(Slide):
    def construct(self):
        self.next_slide()

        title = Text(
            "neural networks: the math that matters", font_size=40, slant=ITALIC
        )
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
            "neural networks are just math — we can reason about them",
            "evaluations are critical for understanding model behavior",
            "prompting / agent orchestration is pseudo-finetuning",
            "ML summer series: zero to your own LLM in 12 weeks",
        ]
        goal_mobs = VGroup(*[Text(g, font_size=27) for g in goals])
        goal_mobs.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        goal_mobs.next_to(underline, DOWN, buff=0.55).to_edge(LEFT, buff=1.0)
        for m in goal_mobs:
            m.set_opacity(0)
        self.add(goal_mobs)

        for m in goal_mobs:
            self.play(m.animate.set_opacity(1.0), run_time=0.45)
            self.next_slide()

        # self.play(FadeOut(VGroup(title, underline, goal_mobs)))
