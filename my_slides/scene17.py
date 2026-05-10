from manim import *
from manim_slides import Slide
from my_slides.shared import *


# ══════════════════════════════════════════════════════════════════
# Slide 17 — Simplified LLM Diagram
# ══════════════════════════════════════════════════════════════════
class Slide17LLMDiagram(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("LLMs are neural networks too")
        self.play(FadeIn(title), run_time=0.5)

        tokens_in = ["The", "cat", "sat", "<PAD>", "<PAD>"]
        tokens_out = ["cat", "sat", "on", "<PAD>", "<PAD>"]
        t_colors = [C_INPUT, C_INPUT, C_INPUT, C_GREY, C_GREY]

        input_nodes = VGroup()
        output_nodes = VGroup()

        for i, (tok, col) in enumerate(zip(tokens_in, t_colors)):
            box = RoundedRectangle(
                corner_radius=0.1,
                width=1.4,
                height=0.55,
                stroke_color=col,
                fill_color=DARK_BG,
                fill_opacity=0.9,
            )
            box.shift(LEFT * 3.5 + UP * (1.0 - i * 0.8))
            lbl = Text(tok, font_size=17, color=col).move_to(box)
            input_nodes.add(VGroup(box, lbl))

        for i, (tok, col) in enumerate(zip(tokens_out, t_colors)):
            box = RoundedRectangle(
                corner_radius=0.1,
                width=1.4,
                height=0.55,
                stroke_color=col,
                fill_color=DARK_BG,
                fill_opacity=0.9,
            )
            box.shift(RIGHT * 3.5 + UP * (1.0 - i * 0.8))
            lbl = Text(tok, font_size=17, color=col).move_to(box)
            output_nodes.add(VGroup(box, lbl))

        self.play(FadeIn(input_nodes), FadeIn(output_nodes), run_time=0.7)
        self.next_slide()

        # Causal connections: output j can attend to inputs 0..j
        causal_lines = VGroup(
            *[
                Line(
                    input_nodes[i].get_right(),
                    output_nodes[j].get_left(),
                    stroke_color=C_EDGE,
                    stroke_width=0.6,
                    stroke_opacity=0.55 if (i < 3 and j < 3) else 0.12,
                )
                for i in range(5)
                for j in range(5)
                if j >= i
            ]
        )
        self.play(Create(causal_lines), run_time=0.9)
        self.next_slide()

        mask_lbl = Text(
            "causal mask: each output sees only past inputs",
            font_size=22,
            color=C_YELLOW,
        )
        mask_lbl.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(mask_lbl, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
