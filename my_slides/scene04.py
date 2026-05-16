from manim import *
from manim_slides import Slide
from my_slides.shared import *


class Slide04Equations(Slide):
    def construct(self):
        neurons, edges, net_group = build_network(
            [3, 4], h_spacing=2.8, v_spacing=0.95, colors=[C_INPUT, C_HIDDEN]
        )
        [n.set_label(f"h_{i}") for (i, n) in enumerate(neurons[-1])]
        net_group.shift(LEFT * 2.5)
        self.add(
            *[n for layer in neurons for n in layer],
            *[e for e in edges.values()],
        )
        self.next_slide()

        title = section_title("writing it out")
        self.play(FadeIn(title), run_time=0.5)

        self.next_slide()

        n_inputs = 3

        # ── Pre-build all equation rows so positions are fixed ────────────
        rows = []
        for j in range(4):
            lhs = MathTex(f"h_{{{j}}}", "=", font_size=24)
            lhs[0].set_color(C_HIDDEN)

            terms = []
            for x in range(n_inputs):
                if x == 0:
                    t = MathTex(f"i_{{{x}}}", r"\cdot", f"w_{{{x}{j}}}", font_size=24)
                    t[0].set_color(C_INPUT)
                    t[2].set_color(C_ORANGE)
                else:
                    t = MathTex(
                        "+", f"i_{{{x}}}", r"\cdot", f"w_{{{x}{j}}}", font_size=24
                    )
                    t[1].set_color(C_INPUT)
                    t[3].set_color(C_ORANGE)
                terms.append(t)

            row = VGroup(lhs, *terms).arrange(RIGHT, buff=0.15)
            rows.append((lhs, terms, row))

        # Stack all rows, aligned left
        all_eq = VGroup(*[r[2] for r in rows]).arrange(
            DOWN, buff=0.45, aligned_edge=LEFT
        )
        all_eq.next_to(net_group, RIGHT, buff=2.5)

        # ── Animate row by row ────────────────────────────────────────────
        for j, (lhs, terms, _) in enumerate(rows):
            self.play(
                neurons[1][j].animate.set_stroke(color=C_YELLOW, width=3),
                FadeIn(lhs),
                run_time=0.5,
            )

            w_lbls = []
            for x in range(n_inputs):
                edge = edges[(0, x, j)]
                w_lbl = MathTex(f"w_{{{x}{j}}}", font_size=18, color=C_ORANGE)
                w_lbl.next_to(edge.get_center(), UP, buff=0.1)
                w_lbls.append(w_lbl)
                self.play(
                    neurons[0][x].animate.set_stroke(color=C_YELLOW, width=3),
                    edge.animate.set_stroke(color=C_ORANGE, width=2.0, opacity=1.0),
                    FadeIn(terms[x]),
                    FadeIn(w_lbl),
                    run_time=0.5,
                )
                self.next_slide()

            # Reset highlights + weight labels, leave equation visible
            self.play(
                neurons[1][j].animate.set_stroke(color=C_HIDDEN, width=2),
                *[
                    neurons[0][x].animate.set_stroke(color=C_INPUT, width=2)
                    for x in range(n_inputs)
                ],
                *[
                    edges[(0, x, j)].animate.set_stroke(
                        color=C_EDGE, width=0.8, opacity=0.4
                    )
                    for x in range(n_inputs)
                ],
                *[FadeOut(w) for w in w_lbls],
                run_time=0.4,
            )

        self.next_slide()

        # ── Flip h to RHS ─────────────────────────────────────────────────
        flipped = []
        for j in range(4):
            lhs, terms, _ = rows[j]

            ft0 = MathTex(f"i_{{{0}}}", r"\cdot", f"w_{{0{j}}}", font_size=24)
            ft0[0].set_color(C_INPUT)
            ft0[2].set_color(C_ORANGE)
            ft1 = MathTex("+", f"i_{{{1}}}", r"\cdot", f"w_{{1{j}}}", font_size=24)
            ft1[1].set_color(C_INPUT)
            ft1[3].set_color(C_ORANGE)
            ft2 = MathTex("+", f"i_{{{2}}}", r"\cdot", f"w_{{2{j}}}", font_size=24)
            ft2[1].set_color(C_INPUT)
            ft2[3].set_color(C_ORANGE)
            rhs = MathTex("=", f"h_{{{j}}}", font_size=24)
            rhs[1].set_color(C_HIDDEN)

            row_f = VGroup(ft0, ft1, ft2, rhs).arrange(RIGHT, buff=0.15)
            flipped.append((row_f, lhs, terms))

        all_flipped = VGroup(*[f[0] for f in flipped]).arrange(
            DOWN, buff=0.45, aligned_edge=LEFT
        )
        all_flipped.move_to(all_eq.get_center())

        self.play(
            *[
                TransformMatchingTex(VGroup(lhs, *terms), row_f)
                for row_f, lhs, terms in flipped
            ],
            run_time=0.8,
        )
        self.next_slide()
        self.play(FadeOut(title))
