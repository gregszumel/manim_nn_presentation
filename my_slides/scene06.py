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

        # ── Equation: h = W i ─────────────────────────────────────────────
        eq_h = MathTex(r"\mathbf{h}", "=", r"\mathbf{W}", r"\mathbf{i}", font_size=34)
        eq_h[0].set_color(C_HIDDEN)
        eq_h[2].set_color(C_ORANGE)
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
            *[e.animate.set_stroke(opacity=0.2) for e in in_hid_edges],
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
            TransformMatchingShapes(sub_copy, eq_collapse),
            run_time=0.8,
        )
        self.next_slide()

        # Annotate W* below the product
        paren_group = VGroup(eq_collapse[3], eq_collapse[4])
        brace = Brace(paren_group, DOWN, color=C_RED, buff=0.05)
        w_star = MathTex(r"\mathbf{W}^*", font_size=32, color=C_RED)
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

        self.play(FadeOut(Group(*self.mobjects)))
