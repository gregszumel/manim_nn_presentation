from manim import *
from manim_slides import Slide
from my_slides.shared import *


class Slide06TwoLayers(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("what happens if we add another layer?")
        self.play(FadeIn(title), run_time=0.5)

        # ── Network: [3, 4] (same as slide 5) ─────────────────────────────
        neurons, edges, net_group = build_network(
            [3, 4], h_spacing=2.8, v_spacing=0.95, colors=[C_INPUT, C_HIDDEN]
        )
        # Layer 1 is the last layer so build_network labels it "o_j"; fix to "h_j"
        for i, n in enumerate(neurons[1]):
            n.set_label(f"h_{{{i}}}", color=C_HIDDEN)
        net_group.shift(LEFT * 3.8)

        self.play(
            *[FadeIn(n) for layer in neurons for n in layer],
            *[Create(e) for e in edges.values()],
            run_time=0.8,
        )
        self.next_slide()

        # ═══════════════════════════════════════════════════════════════════
        # ── Add output layer (using shared helper) ────────────────────────
        # ═══════════════════════════════════════════════════════════════════
        new_neurons, new_edge_mobs = add_layer(
            neurons,
            edges,
            net_group,
            n=1,
            color=C_OUTPUT,
            h_spacing=2.8,
            v_spacing=0.95,
            labels=True,
        )
        out_neuron = new_neurons[0]
        out_edges = VGroup(*new_edge_mobs)

        new_title = section_title("still just linear...")
        self.play(Transform(title, new_title), run_time=0.4)

        # ── Equation: h = W₁ i ────────────────────────────────────────────
        eq_h = MathTex(r"\mathbf{h}", "=", r"\mathbf{W}_1", r"\mathbf{i}", font_size=34)
        eq_h[0].set_color(C_HIDDEN)
        eq_h[2].set_color(C_ORANGE)  # W1 in hidden (green)
        eq_h[3].set_color(C_INPUT)
        eq_h.next_to(net_group, RIGHT, buff=1.8).shift(UP * 1.0)

        self.play(FadeIn(eq_h, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        self.play(FadeIn(out_neuron), Create(out_edges), run_time=0.8)
        # Incorporate into net_group so it stays in sync
        net_group.add(out_neuron, out_edges)
        self.next_slide()

        # ── Question: o = ? ──────────────────────────────────────────────
        eq_o_q = MathTex(r"\mathbf{o}", "=", "?", font_size=34)
        eq_o_q[0].set_color(C_OUTPUT)
        eq_o_q.next_to(eq_h, DOWN, buff=0.6, aligned_edge=LEFT)

        self.play(FadeIn(eq_o_q, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        # ── Isolate hidden→output: fade input+hidden + h-equation ────────
        # Only the first two layers (input, hidden) and their connecting edges
        in_hid_neurons = VGroup(*[n for layer in neurons[:1] for n in layer])
        in_hid_edges = VGroup(*[e for k, e in edges.items() if k[0] < len(neurons) - 2])

        self.play(
            *[n.animate.set_opacity(0) for n in in_hid_neurons],
            *[e.animate.set_stroke(opacity=0) for e in in_hid_edges],
            FadeOut(eq_h),
            run_time=0.5,
        )
        self.next_slide()

        # ── Fill in: o = W_2 h ───────────────────────────────────────────
        eq_o = MathTex(r"\mathbf{o}", "=", r"\mathbf{W}_2", r"\mathbf{h}", font_size=34)
        eq_o[0].set_color(C_OUTPUT)
        eq_o[2].set_color(C_ORANGE)
        eq_o[3].set_color(C_HIDDEN)
        eq_o.move_to(eq_o_q.get_center())

        self.play(TransformMatchingShapes(eq_o_q, eq_o), run_time=0.6)
        self.next_slide()

        # ── Bring back everything with indexes ───────────────────────────
        eq_h1 = MathTex(
            r"\mathbf{h}", "=", r"\mathbf{W}_1", r"\mathbf{i}", font_size=34
        )
        eq_h1[0].set_color(C_HIDDEN)
        eq_h1[2].set_color(C_ORANGE)
        eq_h1[3].set_color(C_INPUT)
        eq_h1.next_to(eq_o, UP, buff=0.5, aligned_edge=LEFT)

        self.play(
            *[n.animate.set_opacity(1) for n in in_hid_neurons],
            *[e.animate.set_stroke(opacity=0.5) for e in in_hid_edges],
            FadeIn(eq_h1),
            run_time=0.6,
        )
        # Now also add the output-layer edges back to net_group (they were
        # already added above, so they are visible throughout the fade).
        self.next_slide()

        # ═══════════════════════════════════════════════════════════════════
        # ── Substitute h into output equation ────────────────────────────
        # ═══════════════════════════════════════════════════════════════════
        # 1. Copy o = W_2 h and slide it down below the original
        sub_copy = eq_o.copy()
        sub_copy.generate_target()
        sub_copy.target.next_to(eq_o, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(MoveToTarget(sub_copy), run_time=0.6)
        self.next_slide()

        # 2. Replace the h in the copied equation with (W_1 i)
        replacement = MathTex(
            r"(",
            r"\mathbf{W}_1",
            r"\mathbf{i}",
            r")",
            font_size=34,
        )
        replacement = MathTex(
            r"\mathbf{o}",
            "=",
            r"\mathbf{W}_2",
            r"(",
            r"\mathbf{W}_1",
            r"\mathbf{i}",
            r")",
            font_size=34,
        )
        replacement[0].set_color(C_OUTPUT)
        replacement[2].set_color(C_ORANGE)
        replacement[4].set_color(C_ORANGE)
        replacement[5].set_color(C_INPUT)
        replacement.move_to(sub_copy.get_left(), aligned_edge=LEFT)

        self.play(TransformMatchingTex(sub_copy, replacement), run_time=0.7)
        # sub_copy is now visually:  o = W_2 (W_1 i)
        self.next_slide()

        # ═══════════════════════════════════════════════════════════════════
        # ── Collapse to (W_2 W_1) i = W* i ──────────────────────────────
        # ═══════════════════════════════════════════════════════════════════
        # Move the parentheses: W_2 (W_1 i) → (W_2 W_1) i
        eq_collapse = MathTex(
            r"\mathbf{o}",
            "=",
            r"(",
            r"\mathbf{W}_2",
            r"\mathbf{W}_1",
            r")",
            r"\mathbf{i}",
            font_size=34,
        )
        eq_collapse[0].set_color(C_OUTPUT)
        eq_collapse[3].set_color(C_ORANGE)
        eq_collapse[4].set_color(C_ORANGE)
        eq_collapse[6].set_color(C_INPUT)
        eq_collapse.move_to(replacement.get_center())

        self.play(
            TransformMatchingShapes(replacement, eq_collapse),
            run_time=0.8,
        )
        self.next_slide()

        # Annotate W* below the product
        paren_group = VGroup(eq_collapse[3], eq_collapse[4])
        brace = Brace(paren_group, DOWN, color=C_YELLOW, buff=0.05)
        w_star = MathTex(r"\mathbf{W}^*", font_size=32, color=C_YELLOW)
        w_star.next_to(brace, DOWN, buff=0.1)

        self.play(
            GrowFromCenter(brace),
            Write(w_star),
            run_time=0.6,
        )
        self.next_slide()

        # ── Punchline ─────────────────────────────────────────────────────
        punchline = Text(
            "still just one matrix — no matter how many layers",
            font_size=26,
            color=C_RED,
        )
        punchline.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(punchline, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        # ═══════════════════════════════════════════════════════════════════
        # ── Visual illustration: collapse edges into the simple net ─────
        # ═══════════════════════════════════════════════════════════════════
        self.next_slide()

        # Slide the current network up to make room (keep all text)
        shift_up = 1.5
        net_group.generate_target()
        net_group.target.shift(UP * shift_up)

        self.play(MoveToTarget(net_group), run_time=0.6)
        self.next_slide()

        # Build the collapsed [3, 1] network below
        simp_neurons, simp_edges, simp_group = build_network(
            [3, 1],
            h_spacing=2.8,
            v_spacing=0.95,
            colors=[C_INPUT, C_OUTPUT],
            labels=True,
        )
        simp_group.shift(LEFT * 3.8 + DOWN * 2.0)

        # Label it
        simp_label = Text("collapsed view", font_size=22, color=C_GREY)
        simp_label.next_to(simp_group, DOWN)

        self.play(
            *[FadeIn(n) for layer in simp_neurons for n in layer],
            FadeIn(simp_label, shift=UP * 0.1),
            FadeOut(punchline),
            run_time=0.8,
        )
        self.next_slide()

        # ── Collapse step 1: i₀→h edges flow into i₀→o edge below ────────
        # Highlight i₀→h edges in yellow
        collapse_edge_visual(self, edges, neurons, simp_edges, i_idx=0)
        collapse_edge_visual(self, edges, neurons, simp_edges, i_idx=1)
        collapse_edge_visual(self, edges, neurons, simp_edges, i_idx=2)

        # ═══════════════════════════════════════════════════════════════════
        # ── Matrix multiplication: W₂ · W₁ = W* (bottom-left) ────────────
        # ═══════════════════════════════════════════════════════════════════
        # Keep all graphs on screen; place matrices in the empty bottom-left

        n_inputs, n_hidden = 3, 4

        # ── Build W₂ (1 × 4), W₁ (4 × 3), W* (1 × 3) ────────────────────
        w2_grid = [
            [
                MathTex(f"w_{{{j}}}", font_size=20, color=C_ORANGE)
                for j in range(n_hidden)
            ]
        ]
        W2 = MobjectMatrix(w2_grid, h_buff=0.3, v_buff=0.2)

        w1_grid = [
            [
                MathTex(f"w_{{{x}{j}}}", font_size=20, color=C_ORANGE)
                for x in range(n_inputs)
            ]
            for j in range(n_hidden)
        ]
        W1 = MobjectMatrix(w1_grid, h_buff=0.5, v_buff=0.2)

        w_star_grid = [
            [
                MathTex(f"w^*_{{{x}}}", font_size=20, color=C_YELLOW)
                for x in range(n_inputs)
            ]
        ]
        W_star = MobjectMatrix(w_star_grid, h_buff=0.4, v_buff=0.2)

        dot_op = MathTex(r"\cdot", font_size=28)
        eq_op = MathTex(r"=", font_size=28)

        mat_eq = VGroup(W2, dot_op, W1, eq_op, W_star).arrange(RIGHT, buff=0.35)
        mat_eq.to_corner(DR, buff=0.7)

        self.play(
            FadeIn(mat_eq, shift=UP * 0.1),
            run_time=0.8,
        )
        self.next_slide()

        # ── Highlight the multiplication column by column ─────────────────
        hl = C_YELLOW

        # For W₂ (1×4) · W₁ (4×3), each output entry w*_x = Σ_j w_{j}·w_{xj}
        # Highlight W₂'s single row + each column of W₁ in turn
        w2_row_hl = SurroundingRectangle(
            VGroup(*w2_grid[0]), color=hl, buff=0.1, stroke_width=2
        )

        for x in range(n_inputs):
            w1_col = VGroup(*[w1_grid[j][x] for j in range(n_hidden)])
            w1_col_hl = SurroundingRectangle(w1_col, color=hl, buff=0.1, stroke_width=2)
            wstar_col_hl = SurroundingRectangle(
                w_star_grid[0][x], color=hl, buff=0.1, stroke_width=2
            )

            self.play(
                Create(wstar_col_hl),
                Create(w2_row_hl),
                Create(w1_col_hl),
                run_time=0.4,
            )
            self.wait(0.1)

            # Pulse the result entry (index via the grid, not MobjectMatrix)
            self.play(
                w_star_grid[0][x].animate.set_color(hl),
                run_time=0.3,
            )
            self.wait(0.1)

            self.play(
                FadeOut(wstar_col_hl),
                FadeOut(w2_row_hl),
                FadeOut(w1_col_hl),
                w_star_grid[0][x].animate.set_color(C_YELLOW),
                *[w2_grid[0][jj].animate.set_color(C_ORANGE) for jj in range(n_hidden)],
                *[w1_grid[j][x].animate.set_color(C_ORANGE) for j in range(n_hidden)],
                run_time=0.3,
            )

        self.next_slide()

        # ── Final connection: matrices → W₂ W₁ = W* ──────────────────────
        eq_final = MathTex(
            r"\mathbf{W}_2",
            r"\mathbf{W}_1",
            "=",
            r"\mathbf{W}^*",
            font_size=34,
        )
        eq_final[0].set_color(C_ORANGE)
        eq_final[1].set_color(C_ORANGE)
        eq_final[3].set_color(C_YELLOW)
        eq_final.to_corner(DR, buff=1.5)

        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


def collapse_edge_visual(self, edges, neurons, simp_edges, i_idx):
    # ── Collapse step 1: i₀→h edges flow into i₀→o edge below ────────
    # Highlight i₀→h edges in yellow
    i0_edges = VGroup(
        # all edges out of i_0
        *[edges[(0, i_idx, j)] for j in range(len(neurons[1]))],
        # all edges out of every h
        *[[e for (key, e) in edges.items() if key[0] == 1]],
    )
    i0_orig_colors = [e.get_stroke_color() for e in i0_edges]

    self.play(
        *[
            e.animate.set_stroke(color=C_YELLOW, width=2.5, opacity=1.0)
            for e in i0_edges
        ],
        run_time=0.6,
    )
    self.next_slide()

    # The bottom edge i₀→o₀ in [3, 1] is at simp_edges[(0, 0, 0)]
    bottom_edge = simp_edges[(0, i_idx, 0)]
    # Make copies of each top edge, then animate them shrinking/sliding
    # onto the position of the bottom edge, one at a time

    edge_copies = [
        e.copy().set_stroke(color=C_YELLOW, width=2.5, opacity=1.0) for e in i0_edges
    ]

    self.add(*edge_copies)
    self.play(
        *[
            e.animate.become(
                bottom_edge.copy().set_stroke(
                    color=C_YELLOW,
                    width=2.5,
                    opacity=0.5,
                )
            )
            for e in edge_copies
        ],
        run_time=0.5,
    )
    self.remove(*edge_copies)

    # Now pulse the bottom edge yellow to show it's "received" the paths
    self.play(
        bottom_edge.animate.set_stroke(color=C_YELLOW, width=3.0, opacity=1.0),
        run_time=0.4,
    )
    self.next_slide()

    # Fade top edges back to normal
    self.play(
        *[
            e.animate.set_stroke(color=c, width=0.8, opacity=0.5)
            for e, c in zip(i0_edges, i0_orig_colors)
        ],
        run_time=0.5,
    )
    self.next_slide()
