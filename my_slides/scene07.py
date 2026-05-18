from manim import *
from manim_slides import Slide
from my_slides.shared import *


# ══════════════════════════════════════════════════════════════════
# Slide 7 — Activation Functions
# ══════════════════════════════════════════════════════════════════
class Slide07Activations(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("activation functions — the missing piece")
        self.play(FadeIn(title), run_time=0.5)

        # ── 1. Biological intuition ──────────────────────────────────────
        bio = Text(
            "like biological neurons — they only fire\npast a certain threshold",
            font_size=26,
            color=C_GREY,
            line_spacing=1.3,
        )
        bio.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(bio, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        # ── 2. ReLU plot ────────────────────────────────────────────────
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-0.4, 2.2, 0.5],
            x_length=4.5,
            y_length=3.0,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).next_to(bio, DOWN, buff=0.5)

        x_lbl = MathTex("z", font_size=24, color=C_GREY).next_to(
            axes.get_x_axis(), DOWN, buff=0.2
        )
        y_lbl = MathTex(r"\sigma(z)", font_size=24, color=C_GREY).next_to(
            axes.get_y_axis(), LEFT, buff=0.2
        )

        relu = axes.plot(
            lambda x: max(0.0, x), x_range=[-2, 2], color=C_ORANGE, stroke_width=3
        )
        relu_label = Text(
            "negative → 0     positive → unchanged", font_size=20, color=C_ORANGE
        )
        relu_label.next_to(axes, DOWN, buff=0.25)

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.6)
        self.play(Create(relu), FadeIn(relu_label), run_time=0.7)
        self.next_slide()

        # ═══════════════════════════════════════════════════════════════════
        # ── 3. Fade out —  build [3, 4, 1] network ───────────────────────
        # ═══════════════════════════════════════════════════════════════════
        self.play(
            FadeOut(VGroup(bio, axes, x_lbl, y_lbl, relu, relu_label)),
            run_time=0.4,
        )

        # Changed: use [3, 4, 1] so the output neuron is visible
        # and shift network LEFT * 2.5 (was 3.8) for better centering
        neurons, edges, net_group = build_network(
            [3, 4, 1],
            h_spacing=2.8,
            v_spacing=0.95,
            colors=[C_INPUT, C_HIDDEN, C_OUTPUT],
        )
        net_group.shift(LEFT * 2.5)

        self.play(
            *[FadeIn(n) for layer in neurons for n in layer],
            *[Create(e) for e in edges.values()],
            run_time=0.8,
        )
        self.next_slide()

        # ═══════════════════════════════════════════════════════════════════
        # ── 4. ReLU demo on the hidden layer ─────────────────────────────
        # ═══════════════════════════════════════════════════════════════════
        # Pre-activation values (some negative, some positive)
        pre_act = [(-0.49, C_RED), (0.36, C_GREEN), (-0.95, C_RED), (0.72, C_GREEN)]
        # Post-activation values (negatives clamped to 0)
        post_act = [("0", C_GREY), ("0.36", C_GREEN), ("0", C_GREY), ("0.72", C_GREEN)]

        # Create floating labels above each hidden neuron
        inter_labels = VGroup()
        for j, (val, col) in enumerate(pre_act):
            lbl = MathTex(f"{val:+.2f}", font_size=20, color=col)
            lbl.next_to(neurons[1][j], UP, buff=0.12)
            inter_labels.add(lbl)

        inter_labels.set_z_index(5)
        self.play(FadeIn(inter_labels, shift=DOWN * 0.1), run_time=0.5)

        relu_hint = Text(
            "ReLU: negatives → 0, positives stay",
            font_size=22,
            color=C_ORANGE,
        )
        relu_hint.next_to(net_group, DOWN, buff=0.6)
        self.play(FadeIn(relu_hint, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        # Highlight the hidden layer
        hidden_highlight = SurroundingRectangle(
            VGroup(*neurons[1], *inter_labels),
            color=C_YELLOW,
            buff=0.2,
            corner_radius=0.1,
        ).set_z_index(2)
        self.play(Create(hidden_highlight), run_time=0.4)
        self.next_slide()

        # Transform each pre-activation label to its post-activation value
        for j in range(4):
            new_val, col = post_act[j]
            new_lbl = MathTex(new_val, font_size=20, color=col)
            new_lbl.move_to(inter_labels[j].get_center())

            if new_val == "0":
                # Negative → 0: overlay red X, then fade to 0
                strike = Text("✗", font_size=28, color=C_RED)
                strike.move_to(inter_labels[j].get_center())
                self.play(
                    inter_labels[j].animate.set_color(C_RED),
                    FadeIn(strike, scale=0.5),
                    run_time=0.25,
                )
                self.play(
                    FadeOut(strike),
                    Transform(inter_labels[j], new_lbl),
                    run_time=0.25,
                )
            else:
                # Positive → stays: just pulse
                self.play(
                    inter_labels[j].animate.set_color(C_YELLOW),
                    run_time=0.15,
                )
                self.play(
                    Transform(inter_labels[j], new_lbl),
                    run_time=0.25,
                )

        self.next_slide()

        # Remove highlight, keep labels + hint visible
        self.play(FadeOut(hidden_highlight), run_time=0.3)
        self.next_slide()

        # ═══════════════════════════════════════════════════════════════════
        # ── 5. Equations with σ ──────────────────────────────────────────
        # ═══════════════════════════════════════════════════════════════════
        # Removed the .shift(UP * 0.6) — equations now anchor properly
        eq_h = MathTex(
            r"\mathbf{h}",
            "=",
            r"\sigma(",
            r"\mathbf{W}_1",
            r"\mathbf{i}",
            ")",
            font_size=34,
        )
        eq_h[0].set_color(C_HIDDEN)
        eq_h[3].set_color(C_ORANGE)
        eq_h[4].set_color(C_INPUT)
        eq_h.next_to(net_group, RIGHT, buff=1.5, aligned_edge=UP)

        self.play(FadeIn(eq_h, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        eq_o = MathTex(
            r"\mathbf{o}",
            "=",
            r"\mathbf{W}_2",
            r"\,",
            r"\sigma(",
            r"\mathbf{W}_1",
            r"\mathbf{i}",
            ")",
            font_size=34,
        )
        eq_o[0].set_color(C_OUTPUT)
        eq_o[2].set_color(C_ORANGE)
        eq_o[5].set_color(C_ORANGE)
        eq_o[6].set_color(C_INPUT)
        eq_o.next_to(eq_h, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(FadeIn(eq_o, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        # ═══════════════════════════════════════════════════════════════════
        # ── 6. Why σ blocks collapse ─────────────────────────────────────
        # ═══════════════════════════════════════════════════════════════════
        # Two short lines instead of one wide one so the text fits the frame.
        explain = VGroup(
            Text("σ is nonlinear —", font_size=20, color=C_YELLOW),
            Text("it cannot be moved past the matrix", font_size=20, color=C_YELLOW),
        ).arrange(DOWN, buff=0.12)
        explain.next_to(eq_o, DOWN, buff=0.5).set_x(eq_o.get_center()[0])

        attempt = MathTex(
            r"\sigma(",  # 0
            r"\mathbf{W}_1",  # 1
            r"\mathbf{i})",  # 2
            r"\;\neq\;",  # 3
            r"\mathbf{W}_1 ",  # 4
            r"\sigma(",  # 5
            r"\mathbf{i}",  # 6
            ")",  # 7
            font_size=28,
        )
        attempt[1].set_color(C_ORANGE)
        attempt[2].set_color(C_INPUT)
        attempt[4].set_color(C_ORANGE)
        attempt[6].set_color(C_INPUT)
        attempt.next_to(explain, DOWN, buff=0.3).set_x(eq_o.get_center()[0])

        self.play(FadeIn(explain, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(attempt, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        distinct = Text(
            "layers stay fundamentally distinct", font_size=18, color=C_GREEN
        )
        distinct.next_to(attempt, DOWN, buff=0.3).set_x(eq_o.get_center()[0])
        self.play(FadeIn(distinct, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        # ═══════════════════════════════════════════════════════════════════
        # ── 7. Summary contrast (centered at bottom) ─────────────────────
        # ═══════════════════════════════════════════════════════════════════
        self.play(
            FadeOut(VGroup(explain, attempt, distinct, relu_hint, inter_labels)),
            run_time=0.4,
        )

        no_sigma_eq = MathTex(
            r"\mathbf{o} = (\mathbf{W}_2 \mathbf{W}_1) \mathbf{i}",
            font_size=28,
            color=C_RED,
        )
        yes_sigma_eq = MathTex(
            r"\mathbf{o} = \mathbf{W}_2 \,\sigma(\mathbf{W}_1 \mathbf{i})",
            font_size=28,
            color=C_GREEN,
        )

        no_sigma_lbl = Text("without σ:  collapse", font_size=20, color=C_RED)
        yes_sigma_lbl = Text("with σ:  no collapse", font_size=20, color=C_GREEN)

        no_group = VGroup(no_sigma_lbl, no_sigma_eq).arrange(
            DOWN, buff=0.15, aligned_edge=LEFT
        )
        yes_group = VGroup(yes_sigma_lbl, yes_sigma_eq).arrange(
            DOWN, buff=0.15, aligned_edge=LEFT
        )

        # Summary moves up into the space the explain/attempt/distinct
        # text vacated (right of the network), stacked vertically rather
        # than side-by-side so the punchline can take the bottom slot.
        summary = VGroup(no_group, yes_group).arrange(
            DOWN, buff=0.45, aligned_edge=LEFT
        )
        summary.next_to(net_group, RIGHT, buff=1.3).set_y(eq_o.get_center()[1] - 2.0)

        self.play(FadeIn(summary, shift=UP * 0.1), run_time=0.7)
        self.next_slide()

        # ── 8. Punchline ─────────────────────────────────────────────────
        # Punchline drops to the bottom edge, freed up by the summary's move.
        punchline = Text(
            "non-linearities = representational power",
            font_size=28,
            color=C_YELLOW,
        )
        punchline.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(punchline, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
