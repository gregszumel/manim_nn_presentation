from manim import *
import numpy as np
from manim_slides import Slide


# ══════════════════════════════════════════════════════════════════
# Slide 1 — Goals
# ══════════════════════════════════════════════════════════════════
class Slide01Goals(Slide):
    def construct(self):
        self.next_slide()

        title = Text("neural networks: what even are they?", font_size=40, slant=ITALIC)
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=UP * 0.1), run_time=0.8)

        underline = Line(
            np.array([title.get_left()[0], title.get_bottom()[1] - 0.08, 0]),
            np.array([title.get_right()[0], title.get_bottom()[1] - 0.08, 0]),
            stroke_color=WHITE,
            stroke_width=1,
            stroke_opacity=0.4,
        )
        self.play(Create(underline), run_time=0.4)
        self.next_slide()

        goals = [
            "- Provide intuitions about how neural networks work",
            "- evaluations are essential when developing ML models",
            "- prompting is pseudo-finetuning, so the above point applies",
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
