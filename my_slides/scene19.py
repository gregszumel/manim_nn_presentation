from manim import *
from manim_slides import Slide
from my_slides.shared import *


# ══════════════════════════════════════════════════════════════════
# Slide 19 — Two Loops Side by Side
# ══════════════════════════════════════════════════════════════════
class Slide19TwoLoops(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("training loop  =  prompting loop")
        self.play(FadeIn(title), run_time=0.5)

        train_steps = ["run input", "check vs expected", "update weights", "repeat"]
        prompt_steps = ["run input", "check vs expected", "update prompt", "repeat"]

        divider = Line(
            UP * 2.2,
            DOWN * 2.8,
            stroke_color=C_GREY,
            stroke_width=1,
            stroke_opacity=0.35,
        )
        self.play(Create(divider), run_time=0.3)

        train_lbl = Text("training loop", font_size=26, color=C_INPUT).shift(
            LEFT * 3.2 + UP * 1.8
        )
        prompt_lbl = Text("prompting loop", font_size=26, color=C_GREEN).shift(
            RIGHT * 3.2 + UP * 1.8
        )
        self.play(FadeIn(train_lbl), FadeIn(prompt_lbl), run_time=0.5)

        for i, (ts, ps) in enumerate(zip(train_steps, prompt_steps)):
            y = 0.9 - i * 0.95
            diff = ts != ps
            tc = C_ORANGE if diff else WHITE
            pc = C_ORANGE if diff else WHITE

            tb = RoundedRectangle(
                corner_radius=0.1,
                width=3.0,
                height=0.62,
                stroke_color=C_INPUT,
                fill_color=DARK_BG,
                fill_opacity=0.85,
            )
            tb.shift(LEFT * 3.2 + UP * y)
            tl = Text(ts, font_size=20, color=tc).move_to(tb)

            pb = RoundedRectangle(
                corner_radius=0.1,
                width=3.0,
                height=0.62,
                stroke_color=C_GREEN,
                fill_color=DARK_BG,
                fill_opacity=0.85,
            )
            pb.shift(RIGHT * 3.2 + UP * y)
            pl = Text(ps, font_size=20, color=pc).move_to(pb)

            self.play(FadeIn(VGroup(tb, tl)), FadeIn(VGroup(pb, pl)), run_time=0.35)

            conn = DashedLine(
                tb.get_right(),
                pb.get_left(),
                stroke_color=C_GREY,
                stroke_width=0.8,
                stroke_opacity=0.45,
            )
            self.play(Create(conn), run_time=0.2)
            self.next_slide()

        punchline = Text(
            "prompting is finetuning — just with natural language instead of gradients",
            font_size=21,
            color=C_YELLOW,
        )
        punchline.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(punchline, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
