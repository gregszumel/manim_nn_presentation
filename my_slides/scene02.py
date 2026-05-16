from manim import *
from manim_slides import Slide

from my_slides.shared import (
    section_title,
    build_network,
    Neuron,
    C_INPUT,
    C_HIDDEN,
    C_OUTPUT,
    C_ORANGE,
    C_YELLOW,
    C_GREY,
)


# ══════════════════════════════════════════════════════════════════
# Slide 2 — Basic Neural Network
# ══════════════════════════════════════════════════════════════════
class Slide02BasicNetwork(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("a neural network")
        self.play(FadeIn(title), run_time=0.5)

        neurons, edges, net_group = build_network(
            [3, 4, 2], h_spacing=2.5, v_spacing=0.9
        )
        net_group.center().shift(DOWN * 0.3)

        for layer in neurons:
            self.play(
                LaggedStart(*[FadeIn(n) for n in layer], lag_ratio=0.2), run_time=0.6
            )
        self.next_slide()

        layer_edges = [[] for _ in range(len(neurons) - 1)]
        for (l, i, j), e in edges.items():
            layer_edges[l].append(e)
        for l_edges in layer_edges:
            self.play(
                LaggedStart(*[Create(e) for e in l_edges], lag_ratio=0.04), run_time=0.7
            )
        self.next_slide()

        layer_labels_info = [
            (neurons[0], "input", C_INPUT),
            (neurons[1], "hidden", C_HIDDEN),
            (neurons[2], "output", C_OUTPUT),
        ]
        layer_label_mobs = []
        for layer, name, color in layer_labels_info:
            group = VGroup(*layer)
            rect = SurroundingRectangle(group, buff=0.2, color=color, corner_radius=0.1)
            lbl = Text(name, font_size=20, color=color).next_to(group, DOWN, buff=0.4)
            self.play(ShowPassingFlash(rect, time_width=0.8, run_time=0.7))
            self.play(FadeIn(lbl), run_time=0.3)
            layer_label_mobs.append(lbl)
        self.next_slide()

        act_label = VGroup(
            Text("activations", font_size=22, color=C_YELLOW),
            Text("the value each neuron outputs", font_size=16, color=C_GREY),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        act_label.to_edge(LEFT, buff=0.5).shift(UP * 0.3)
        self.play(FadeIn(act_label), run_time=0.3)
        self.play(
            LaggedStart(
                *[
                    ShowPassingFlash(
                        n.copy().set_stroke(color=C_YELLOW, width=4), time_width=0.6
                    )
                    for n in [n for layer in neurons for n in layer]
                ],
                lag_ratio=0.12,
            ),
            run_time=1.5,
        )
        self.next_slide()

        weight_label = VGroup(
            Text("weights", font_size=22, color=C_ORANGE),
            Text("how strongly each connection matters", font_size=16, color=C_GREY),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        weight_label.next_to(act_label, DOWN, aligned_edge=LEFT)
        self.play(FadeIn(weight_label), run_time=0.3)
        self.play(
            LaggedStart(
                *[
                    ShowPassingFlash(
                        e.copy().set_stroke(color=C_ORANGE, width=2.5, opacity=1.0),
                        time_width=0.5,
                    )
                    for e in edges.values()
                ],
                lag_ratio=0.05,
            ),
            run_time=2.0,
        )
        self.next_slide()

        # ══════════════════════════════════════════════════════════════════
        # — Depth: insert h₂, h₃ between hidden and output —
        # ══════════════════════════════════════════════════════════════════

        self.play(
            FadeOut(VGroup(title, act_label, weight_label, *layer_label_mobs)),
            run_time=0.4,
        )
        self.next_slide()

        # The existing [3,4,2] network: input(3) → h₁(hidden,4) → output(2)
        # We'll insert h₂, h₃, ⋯ between h₁ and the output.
        h1 = neurons[1]  # the 4 hidden neurons (h₁ layer)
        out = neurons[2]  # the 2 output neurons

        o0_pos = out[0].get_center()
        o1_pos = out[1].get_center()
        o_y0 = o0_pos[1]  # ~0.15
        o_y1 = o1_pos[1]  # ~-0.75

        # Fade out old h₁→output edges
        old_h1_out_edges = VGroup(*[e for k, e in edges.items() if k[0] == 1])
        self.play(FadeOut(old_h1_out_edges), run_time=0.3)

        h_sp_d = 1.6
        h1_x = h1[0].get_center()[0]  # ~0
        o_x = o0_pos[0]  # ~2.5

        # New layers to the right of h₁
        # Match the y positions of the 4 h₁ neurons for h₂ and h₃
        h1_y_positions = [n.get_center()[1] for n in h1]

        h2_x = o_x
        h3_x = h2_x + h_sp_d
        dots_x = h3_x + 0.7
        out_new_x = h3_x + 2.0
        cy_dots = (h1_y_positions[0] + h1_y_positions[-1]) / 2

        # Create h₂ neurons (4, matching h₁'s vertical span)
        h2_neurons = VGroup(
            *[Neuron(label=f"h_{{2,{i}}}", color=C_HIDDEN) for i in range(4)]
        )
        for i, n in enumerate(h2_neurons):
            n.move_to(np.array([h2_x, h1_y_positions[i], 0]))
            n.set_z_index(1)

        # Create h₃ neurons (4, matching h₁'s vertical span)
        h3_neurons = VGroup(
            *[Neuron(label=f"h_{{3,{i}}}", color=C_HIDDEN) for i in range(4)]
        )
        for i, n in enumerate(h3_neurons):
            n.move_to(np.array([h3_x, h1_y_positions[i], 0]))
            n.set_z_index(1)

        # Ellipsis
        dots = MathTex(r"\cdots", font_size=36, color=C_GREY)
        dots.move_to(np.array([dots_x, cy_dots, 0]))

        # Edges: h₁ → h₂ (4×4 = 16)
        edges_h1_h2 = [
            Line(
                s.get_center(),
                t.get_center(),
                stroke_color=C_ORANGE,
                stroke_width=0.8,
                stroke_opacity=0.5,
            )
            for s in h1
            for t in h2_neurons
        ]
        # Edges: h₂ → h₃ (4×4 = 16)
        edges_h2_h3 = [
            Line(
                s.get_center(),
                t.get_center(),
                stroke_color=C_ORANGE,
                stroke_width=0.8,
                stroke_opacity=0.5,
            )
            for s in h2_neurons
            for t in h3_neurons
        ]
        # Edges: h₃ → output (4×2 = 8)
        edges_h3_out = [
            Line(
                s.get_center(),
                np.array([out_new_x, o_y0, 0]),
                stroke_color=C_ORANGE,
                stroke_width=0.8,
                stroke_opacity=0.5,
            )
            for s in h3_neurons
        ] + [
            Line(
                s.get_center(),
                np.array([out_new_x, o_y1, 0]),
                stroke_color=C_ORANGE,
                stroke_width=0.8,
                stroke_opacity=0.5,
            )
            for s in h3_neurons
        ]

        # Animate: move output right, fade in new layers + edges
        all_new_edges = edges_h1_h2 + edges_h2_h3 + edges_h3_out
        self.play(
            out[0].animate.move_to(np.array([out_new_x, o_y0, 0])),
            out[1].animate.move_to(np.array([out_new_x, o_y1, 0])),
            LaggedStart(*[FadeIn(n) for n in h2_neurons], lag_ratio=0.3),
            LaggedStart(*[FadeIn(n) for n in h3_neurons], lag_ratio=0.3),
            FadeIn(dots, scale=0.5),
            *[Create(e) for e in all_new_edges],
            run_time=1.0,
        )

        # Bracket + label spanning h₁ through ⋯
        depth_brace = Brace(
            VGroup(*h1, *h2_neurons, *h3_neurons, dots),
            DOWN,
            color=C_YELLOW,
            buff=0.15,
        )
        depth_label = Text("many hidden layers", font_size=22, color=C_YELLOW)
        depth_label.next_to(depth_brace, DOWN, buff=0.1)
        self.play(GrowFromCenter(depth_brace), FadeIn(depth_label), run_time=0.5)
        self.next_slide()

        # ══════════════════════════════════════════════════════════════════
        # — Scale back: remove depth layers, restore output —
        # ══════════════════════════════════════════════════════════════════

        depth_extra = VGroup(
            *h2_neurons,
            *h3_neurons,
            dots,
            depth_brace,
            depth_label,
            *all_new_edges,
        )
        self.play(FadeOut(depth_extra), run_time=0.5)

        # Restore output to original position
        self.play(
            out[0].animate.move_to(o0_pos),
            out[1].animate.move_to(o1_pos),
            run_time=0.4,
        )
        # Recreate the old h₁→output edges
        restored_h1_out = [
            Line(
                s.get_center(),
                t.get_center(),
                stroke_color=C_ORANGE,
                stroke_width=0.8,
                stroke_opacity=0.5,
            )
            for s in h1
            for t in out
        ]
        # Store them back in edges dict so later code can refer to them
        for i, s in enumerate(h1):
            for j, t in enumerate(out):
                edges[(1, i, j)] = restored_h1_out[i * len(out) + j]
        self.play(
            *[Create(e) for e in restored_h1_out],
            run_time=0.5,
        )
        self.next_slide()

        # ══════════════════════════════════════════════════════════════════
        # — Scale up feature dimensions (width) —
        # ══════════════════════════════════════════════════════════════════

        # On the full [3,4,2] network, grow each layer:
        # inputs:  3  → 5   (add i₃, i₄ below)
        # hidden:  4  → 6   (add h₄, h₅ below)
        # outputs: 2  → 4   (add o₂, o₃ below)

        v_sp_w = 0.75
        h_sp_w = 2.5  # same as original

        inp = neurons[0]
        hid = neurons[1]
        out = neurons[2]

        i_x = inp[0].get_center()[0]
        h_x = hid[0].get_center()[0]
        o_x = out[0].get_center()[0]

        # Lowest existing y in each layer
        i_last_y = inp[-1].get_center()[1]
        h_last_y = hid[-1].get_center()[1]
        o_last_y = out[-1].get_center()[1]

        # Extra input neurons below i₂
        i_extra = [
            Neuron(label=f"i_{{{3 + i}}}", color=C_INPUT).move_to(
                np.array([i_x, i_last_y - (i + 1) * v_sp_w, 0])
            )
            for i in range(2)  # i₃, i₄
        ]
        for n in i_extra:
            n.set_z_index(1)

        # Extra hidden neurons below h₃
        h_extra = [
            Neuron(label=f"h_{{{4 + i}}}", color=C_HIDDEN).move_to(
                np.array([h_x, h_last_y - (i + 1) * v_sp_w, 0])
            )
            for i in range(2)  # h₄, h₅
        ]
        for n in h_extra:
            n.set_z_index(1)

        # Extra output neurons below o₁
        o_extra = [
            Neuron(label=f"o_{{{2 + i}}}", color=C_OUTPUT).move_to(
                np.array([o_x, o_last_y - (i + 1) * v_sp_w, 0])
            )
            for i in range(2)  # o₂, o₃
        ]
        for n in o_extra:
            n.set_z_index(1)

        all_inp = list(inp) + i_extra
        all_hid = list(hid) + h_extra
        all_out = list(out) + o_extra

        # Build all new edges
        new_in_hid_edges = []
        for s in all_inp:
            for t in h_extra:
                new_in_hid_edges.append(
                    Line(
                        s.get_center(),
                        t.get_center(),
                        stroke_color=C_ORANGE,
                        stroke_width=0.8,
                        stroke_opacity=0.5,
                    )
                )
        # Also edges from i_extra to existing hidden
        for s in i_extra:
            for t in hid:
                new_in_hid_edges.append(
                    Line(
                        s.get_center(),
                        t.get_center(),
                        stroke_color=C_ORANGE,
                        stroke_width=0.8,
                        stroke_opacity=0.5,
                    )
                )

        new_hid_out_edges = []
        for s in all_hid:
            for t in o_extra:
                new_hid_out_edges.append(
                    Line(
                        s.get_center(),
                        t.get_center(),
                        stroke_color=C_ORANGE,
                        stroke_width=0.8,
                        stroke_opacity=0.5,
                    )
                )
        # Also edges from h_extra to existing output
        for s in h_extra:
            for t in out:
                new_hid_out_edges.append(
                    Line(
                        s.get_center(),
                        t.get_center(),
                        stroke_color=C_ORANGE,
                        stroke_width=0.8,
                        stroke_opacity=0.5,
                    )
                )

        all_new_w = new_in_hid_edges + new_hid_out_edges

        # Animate: fade in extra neurons + edges
        self.play(
            LaggedStart(*[FadeIn(n) for n in i_extra], lag_ratio=0.2),
            run_time=0.5,
        )
        self.play(
            LaggedStart(*[FadeIn(n) for n in h_extra], lag_ratio=0.2),
            run_time=0.5,
        )
        self.play(
            LaggedStart(*[FadeIn(n) for n in o_extra], lag_ratio=0.2),
            run_time=0.5,
        )
        self.play(
            LaggedStart(*[Create(e) for e in all_new_w], lag_ratio=0.02),
            run_time=1.2,
        )
        self.next_slide()

        # ══════════════════════════════════════════════════════════════════
        # — Scale back: remove extra width neurons —
        # ══════════════════════════════════════════════════════════════════

        w_extra = VGroup(*i_extra, *h_extra, *o_extra, *all_new_w)
        self.play(FadeOut(w_extra), run_time=0.5)
        self.next_slide()

        # ══════════════════════════════════════════════════════════════════
        # — Final strip-down to [2,1] —
        # ══════════════════════════════════════════════════════════════════

        # Keep only: i₀, i₁, h₁_₀ (first hidden neuron)
        keep_edge_keys = {(0, 0, 0), (0, 1, 0)}
        keep_neurons = {neurons[0][0], neurons[0][1], neurons[1][0]}
        remove_neurons = [
            n for layer in neurons for n in layer if n not in keep_neurons
        ]
        # Include the restored h₁→output edges we created
        remove_edges = [e for k, e in edges.items() if k not in keep_edge_keys]

        self.play(
            FadeOut(VGroup(*remove_neurons)),
            FadeOut(VGroup(*remove_edges)),
            run_time=0.6,
        )

        # Target positions match build_network([2,1], h_spacing=3.0, v_spacing=1.2)
        # .center().shift(LEFT*2.0 + DOWN*0.3)
        target_n00 = np.array([-3.5, 0.3, 0])
        target_n01 = np.array([-3.5, -0.9, 0])
        target_n10 = np.array([-0.5, -0.3, 0])

        self.play(
            neurons[0][0].animate.move_to(target_n00),
            neurons[0][1].animate.move_to(target_n01),
            neurons[1][0].animate.move_to(target_n10).set_stroke(color=C_HIDDEN),
            edges[(0, 0, 0)].animate.put_start_and_end_on(target_n00, target_n10),
            edges[(0, 1, 0)].animate.put_start_and_end_on(target_n01, target_n10),
            run_time=0.7,
        )
        self.next_slide()
