from manim import *
from manim_slides import Slide

from my_slides.shared import *


class Slide03SingleNeuron(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("how one neuron computes")
        neurons, edges, net_group = build_network([2, 1], h_spacing=3.0, v_spacing=1.2)
        neurons[-1][-1].set_stroke_color(C_HIDDEN)
        neurons[-1][-1].set_label("h_{0}", color=C_HIDDEN)
        net_group.shift(LEFT * 2.0 + DOWN * 0.3)
        self.add(*[n for layer in neurons for n in layer], *edges.values())
        self.play(FadeIn(title), run_time=0.5)
        self.next_slide()

        v0, v1, w0, w1, b = 0.5, 0.8, 0.6, -0.3, 0.1

        neurons[0][0].set_label(f"{v0}")
        neurons[0][1].set_label(f"{v1}")
        self.next_slide()

        w_lbl0 = MathTex(f"w_{{00}}={w0}", font_size=24, color=C_ORANGE)
        w_lbl1 = MathTex(f"w_{{10}}={w1}", font_size=24, color=C_ORANGE)
        w_lbl0.next_to(edges[(0, 0, 0)].get_center(), UP, buff=0.15)
        w_lbl1.next_to(edges[(0, 1, 0)].get_center(), DOWN, buff=0.15)
        self.play(
            edges[(0, 0, 0)].animate.set_stroke(color=C_ORANGE, width=2.5),
            edges[(0, 1, 0)].animate.set_stroke(color=C_ORANGE, width=2.5),
            FadeIn(w_lbl0),
            FadeIn(w_lbl1),
            run_time=0.6,
        )
        self.next_slide()

        # ── Build ALL final positions before any float manipulation ──────
        # (moving submobjects changes parent bounding boxes, so record
        #  destinations and lay out dependent mobs first)

        term1 = MathTex(r"0.5", r"\times", r"0.6", r"=", r"0.30", font_size=30)
        term1[0].set_color(C_INPUT)
        term1[2].set_color(C_ORANGE)
        term1[4].set_color(C_HIDDEN)
        term1.move_to(RIGHT * 3.2 + UP * 1.5)

        term2 = MathTex(r"0.8", r"\times", r"(-0.3)", r"=", r"-0.24", font_size=30)
        term2[0].set_color(C_INPUT)
        term2[2].set_color(C_ORANGE)
        term2[4].set_color(C_HIDDEN)
        term2.next_to(term1, DOWN, buff=0.4).align_to(term1, RIGHT)

        plus = MathTex(r"+", font_size=30).next_to(term2, LEFT, buff=0.25)

        lx = min(plus.get_left()[0], term1.get_left()[0]) - 0.1
        rx = max(term1.get_right()[0], term2.get_right()[0]) + 0.1
        ly = term2.get_bottom()[1] - 0.15
        divider = Line(
            np.array([lx, ly, 0]),
            np.array([rx, ly, 0]),
            stroke_color=C_GREY,
            stroke_width=1.2,
        )

        sum_eq = MathTex(r"h", r"=", r"0.06", font_size=30)
        sum_eq[2].set_color(C_HIDDEN)
        sum_eq.next_to(divider, DOWN, buff=0.2).align_to(term2, RIGHT)

        bias_eq = MathTex(r"h = 0.06 +", r"\ 0.1", font_size=26)
        bias_eq[1].set_color(C_GREEN)
        bias_desc = Text(
            "bias: a fixed offset per neuron —\nshifts the threshold for firing",
            font_size=14,
            color=C_GREY,
            line_spacing=1.2,
        )
        bias_group = VGroup(bias_eq, bias_desc).arrange(
            DOWN, buff=0.12, aligned_edge=LEFT
        )
        bias_group.next_to(sum_eq, DOWN, buff=0.5).align_to(plus, LEFT)

        act_eq = MathTex(r"\text{output} = \sigma(h)", font_size=26, color=C_GREEN)
        act_desc = Text(
            "activation: squashes result to a bounded range\n— without this, layers collapse to one matrix",
            font_size=14,
            color=C_GREY,
            line_spacing=1.2,
        )
        act_group = VGroup(act_eq, act_desc).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        act_group.next_to(bias_group, DOWN, buff=0.4).align_to(bias_group, LEFT)

        # Record float destinations (must happen before submob moves)
        dst_v0 = term1[0].get_center().copy()
        dst_w0 = term1[2].get_center().copy()
        dst_v1 = term2[0].get_center().copy()
        dst_w1 = term2[2].get_center().copy()

        src_v0 = neurons[0][0].get_center().copy()
        src_w0 = w_lbl0.get_center().copy()
        src_v1 = neurons[0][1].get_center().copy()
        src_w1 = w_lbl1.get_center().copy()

        # ── Float term 1 ─────────────────────────────────────────────────
        term1[0].move_to(src_v0)
        term1[2].move_to(src_w0)
        for p in [term1[1], term1[3], term1[4]]:
            p.set_opacity(0)
        self.add(term1)
        self.play(
            term1[0].animate.move_to(dst_v0),
            term1[2].animate.move_to(dst_w0),
            run_time=0.65,
        )
        self.play(
            term1[1].animate.set_opacity(1),
            term1[3].animate.set_opacity(1),
            term1[4].animate.set_opacity(1),
            run_time=0.35,
        )
        self.next_slide()

        # ── Float term 2 ─────────────────────────────────────────────────
        term2[0].move_to(src_v1)
        term2[2].move_to(src_w1)
        for p in [term2[1], term2[3], term2[4]]:
            p.set_opacity(0)
        self.add(term2)
        self.play(
            term2[0].animate.move_to(dst_v1),
            term2[2].animate.move_to(dst_w1),
            FadeIn(plus),
            run_time=0.65,
        )
        self.play(
            term2[1].animate.set_opacity(1),
            term2[3].animate.set_opacity(1),
            term2[4].animate.set_opacity(1),
            run_time=0.35,
        )
        self.next_slide()

        # ── Sum ──────────────────────────────────────────────────────────
        self.play(Create(divider), run_time=0.3)
        self.play(Write(sum_eq), run_time=0.5)

        # Float h=0.06 from the equation into the output neuron, then swap label
        h_in_neuron = MathTex("0.06", font_size=16, color=C_YELLOW)
        h_in_neuron.move_to(sum_eq[2].get_center())
        self.add(h_in_neuron)
        self.play(h_in_neuron.animate.move_to(neurons[1][0].get_center()), run_time=0.6)
        self.play(FadeOut(h_in_neuron), run_time=0.25)
        neurons[1][0].set_label("0.06", color=C_YELLOW)
        self.next_slide()

        # ── Bias ─────────────────────────────────────────────────────────
        self.play(FadeIn(bias_group), run_time=0.6)
        self.next_slide()

        # ── Activation ───────────────────────────────────────────────────
        self.play(FadeIn(act_group), run_time=0.6)
        self.next_slide()

        # ── Transition: fade out computation, expand to [3,4] ────────────
        # Ends matching scene04's starting layout exactly.
        self.play(
            FadeOut(
                VGroup(
                    title,
                    w_lbl0,
                    w_lbl1,
                    term1,
                    term2,
                    plus,
                    divider,
                    sum_eq,
                    bias_group,
                    act_group,
                )
            ),
            run_time=0.4,
        )

        # Build target [3,4] geometry — same params as scene04
        full_neurons, full_edges, full_net = build_network(
            [3, 4], h_spacing=2.8, v_spacing=0.95, colors=[C_INPUT, C_HIDDEN]
        )
        # Layer 1 gets prefix "o" by default (last layer); relabel to "h"
        for i, n in enumerate(full_neurons[1]):
            n.set_label(f"h_{{{i}}}", color=C_HIDDEN)
        full_net.center().shift(LEFT * 2.5)

        t_n00 = full_neurons[0][0].get_center()
        t_n01 = full_neurons[0][1].get_center()
        t_n10 = full_neurons[1][0].get_center()

        self.play(
            edges[(0, 0, 0)].animate.set_stroke(color=C_ORANGE, width=0.8),
            edges[(0, 1, 0)].animate.set_stroke(color=C_ORANGE, width=0.8),
        )
        neurons[0][0].set_label("i_0")
        neurons[0][1].set_label("i_1")
        neurons[1][0].set_label("h_0", color=C_HIDDEN)
        # Move the 3 kept neurons to their new positions
        self.play(
            neurons[0][0].animate.move_to(t_n00),
            neurons[0][1].animate.move_to(t_n01),
            neurons[1][0].animate.move_to(t_n10),
            edges[(0, 0, 0)].animate.put_start_and_end_on(t_n00, t_n10),
            edges[(0, 1, 0)].animate.put_start_and_end_on(t_n01, t_n10),
            run_time=0.7,
        )

        # Fade in the remaining neurons: third input + hidden neurons 1-3
        self.play(
            LaggedStart(
                FadeIn(full_neurons[0][2]),
                *[FadeIn(n) for n in full_neurons[1][1:]],
                lag_ratio=0.15,
            ),
            run_time=0.5,
        )

        # Create the remaining edges (the two kept ones are already positioned)
        extra_edges = [
            e for k, e in full_edges.items() if k not in {(0, 0, 0), (0, 1, 0)}
        ]
        self.play(
            LaggedStart(*[Create(e) for e in extra_edges], lag_ratio=0.03),
            run_time=0.8,
        )
        self.next_slide()
