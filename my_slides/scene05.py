from manim import *
from manim_slides import Slide
from my_slides.shared import *


class Slide05MatrixMult(Slide):
    def construct(self):

        # ── Network (same as slide 4 ending) ──────────────────────────────
        neurons, edges, net_group = build_network(
            [3, 4], h_spacing=2.8, v_spacing=0.95, colors=[C_INPUT, C_HIDDEN]
        )
        # Layer 1 is the last layer so build_network labels it "o_j"; fix to "h_j"
        for i, n in enumerate(neurons[1]):
            n.set_label(f"h_{{{i}}}", color=C_HIDDEN)
        net_group.shift(LEFT * 2.8)
        self.add(
            *[n for layer in neurons for n in layer],
            *[e for e in edges.values()],
        )

        # ── Equations: i_0·w_{x0} + … = h_j (flipped form) ───────────────
        n_inputs, n_hidden = 3, 4
        eq_rows = []

        for j in range(n_hidden):
            i_list, w_list, other_list, parts = [], [], [], []

            for x in range(n_inputs):
                if x > 0:
                    plus_m = MathTex(r"+", font_size=22)
                    other_list.append(plus_m)
                    parts.append(plus_m)
                i_m = MathTex(f"i_{{{x}}}", font_size=22, color=C_INPUT)
                dot_m = MathTex(r"\cdot", font_size=22)
                w_m = MathTex(f"w_{{{x}{j}}}", font_size=22, color=C_ORANGE)
                i_list.append(i_m)
                w_list.append(w_m)
                other_list.append(dot_m)
                parts.extend([i_m, dot_m, w_m])

            eq_m = MathTex("=", font_size=22)
            h_m = MathTex(f"h_{{{j}}}", font_size=22, color=C_HIDDEN)
            other_list.append(eq_m)
            parts.extend([eq_m, h_m])

            row = VGroup(*parts).arrange(RIGHT, buff=0.12)
            eq_rows.append(
                {"i": i_list, "w": w_list, "h": h_m, "other": other_list, "row": row}
            )

        all_eq = VGroup(*[r["row"] for r in eq_rows]).arrange(
            DOWN, buff=0.35, aligned_edge=LEFT
        )
        all_eq.next_to(net_group, RIGHT, buff=1.5)

        self.add(all_eq)
        title = section_title("this is just matrix multiplication")
        self.play(FadeIn(title), run_time=0.5)

        self.next_slide()

        # ── Push up: fade network, center equations at top ─────────────────
        self.play(
            FadeOut(VGroup(*[n for layer in neurons for n in layer], *edges.values())),
            FadeOut(title),
            all_eq.animate.to_edge(UP, buff=0.5).set_x(0),
            run_time=0.7,
        )
        self.next_slide()

        # ── Pre-build matrix structure (invisible until animated in) ───────
        # W: n_hidden rows × n_inputs cols, W[j][x] = w_{xj}
        W_grid = [
            [
                MathTex(f"w_{{{x}{j}}}", font_size=20, color=C_ORANGE)
                for x in range(n_inputs)
            ]
            for j in range(n_hidden)
        ]
        W_mat = MobjectMatrix(W_grid, h_buff=1.1, v_buff=0.7)

        i_grid = [
            [MathTex(f"i_{{{x}}}", font_size=20, color=C_INPUT)]
            for x in range(n_inputs)
        ]
        i_vec = MobjectMatrix(i_grid, h_buff=0.9, v_buff=0.7)

        h_grid = [
            [MathTex(f"h_{{{j}}}", font_size=20, color=C_HIDDEN)]
            for j in range(n_hidden)
        ]
        h_vec = MobjectMatrix(h_grid, h_buff=0.9, v_buff=0.7)

        dot_op = MathTex(r"\cdot", font_size=32)
        eq_op = MathTex(r"=", font_size=32)

        mat_eq = VGroup(W_mat, dot_op, i_vec, eq_op, h_vec).arrange(RIGHT, buff=0.45)
        mat_eq.center().shift(DOWN * 0.5)

        # Record target positions BEFORE hiding anything
        W_pos = {
            (j, x): W_grid[j][x].get_center().copy()
            for j in range(n_hidden)
            for x in range(n_inputs)
        }
        i_pos = {x: i_grid[x][0].get_center().copy() for x in range(n_inputs)}
        h_pos = {j: h_grid[j][0].get_center().copy() for j in range(n_hidden)}

        # Hide all entries and operators (matrix shells stay invisible)
        for row in W_grid:
            for e in row:
                e.set_opacity(0)
        for row in i_grid:
            row[0].set_opacity(0)
        for row in h_grid:
            row[0].set_opacity(0)
        W_mat.get_brackets().set_opacity(0)
        i_vec.get_brackets().set_opacity(0)
        h_vec.get_brackets().set_opacity(0)
        dot_op.set_opacity(0)
        eq_op.set_opacity(0)

        self.add(mat_eq)

        # ── Weights → W matrix ─────────────────────────────────────────────
        # We'll store visible copies in w_vis[j][x] so we can reference them later
        all_eq_w = [w for r in eq_rows for w in r["w"]]
        self.play(*[w.animate.set_color(C_YELLOW) for w in all_eq_w], run_time=0.4)
        self.next_slide()

        w_vis = [[None for _ in range(n_inputs)] for _ in range(n_hidden)]
        w_fly = []
        for j, row in enumerate(eq_rows):
            for x, w_m in enumerate(row["w"]):
                c = w_m.copy().set_color(C_YELLOW)
                w_vis[j][x] = c
                self.add(c)
                w_fly.append(c.animate.move_to(W_pos[(j, x)]).set_color(C_ORANGE))

        self.play(*w_fly, run_time=1.2)
        # Reset equation w's back to original color, show matrix brackets
        self.play(
            *[w.animate.set_color(C_ORANGE) for w in all_eq_w],
            W_mat.get_brackets().animate.set_opacity(1),
            run_time=0.5,
        )
        self.next_slide()

        # ── i's → i vector ────────────────────────────────────────────────
        all_eq_i = [i_m for r in eq_rows for i_m in r["i"]]
        self.play(*[i_m.animate.set_color(C_YELLOW) for i_m in all_eq_i], run_time=0.4)
        self.next_slide()

        i_vis = [None for _ in range(n_inputs)]
        all_is = set()
        i_fly = []
        for row in eq_rows:
            for x, i_m in enumerate(row["i"]):
                c = i_m.copy().set_color(C_YELLOW)
                all_is.add(c)
                i_vis[x] = c  # last one wins (all identical, same target)
                self.add(c)
                i_fly.append(c.animate.move_to(i_pos[x]).set_color(C_INPUT))

        self.play(*i_fly, run_time=1.0)
        # Reset equation i's back to original color, show i vector brackets
        self.play(
            *[i_m.animate.set_color(C_INPUT) for i_m in all_eq_i],
            i_vec.get_brackets().animate.set_opacity(1),
            run_time=0.5,
        )
        self.next_slide()

        # ── h's → h vector ─────────────────────────────────────────────────
        all_eq_h = [r["h"] for r in eq_rows]
        self.play(*[h_m.animate.set_color(C_YELLOW) for h_m in all_eq_h], run_time=0.4)

        h_vis = [None for _ in range(n_hidden)]
        h_fly = []
        for j, h_m in enumerate(all_eq_h):
            c = h_m.copy().set_color(C_YELLOW)
            h_vis[j] = c
            self.add(c)
            h_fly.append(c.animate.move_to(h_pos[j]).set_color(C_HIDDEN))

        self.play(*h_fly, run_time=0.8)

        # Reset equation h's back to original color, show operators & brackets
        self.play(
            *[h_m.animate.set_color(C_HIDDEN) for h_m in all_eq_h],
            h_vec.get_brackets().animate.set_opacity(1),
            dot_op.animate.set_opacity(1),
            eq_op.animate.set_opacity(1),
            run_time=0.5,
        )
        self.next_slide()

        # ═══════════════════════════════════════════════════════════════════
        # ── Pseudo matrix multiplication: all 4 rows ─────────────────────
        # ═══════════════════════════════════════════════════════════════════
        hl = C_YELLOW

        for j in range(n_hidden):
            # Highlight row j of W and all i entries
            self.play(
                *[w_vis[j][x].animate.set_color(hl) for x in range(n_inputs)],
                *[i_vis[x].animate.set_color(hl) for x in range(n_inputs)],
                run_time=0.4,
            )

            w_box = SurroundingRectangle(
                VGroup(*w_vis[j]), color=hl, buff=0.1, stroke_width=2
            )
            i_box = SurroundingRectangle(
                VGroup(*i_vis), color=hl, buff=0.1, stroke_width=2
            )

            # Dot-product equation for this row
            dot_terms = []
            for x in range(n_inputs):
                if x > 0:
                    dot_terms.append(MathTex(r"+", font_size=26, color=WHITE))
                dot_terms.append(MathTex(f"w_{{{x}{j}}}", font_size=26, color=C_ORANGE))
                dot_terms.append(MathTex(r"\cdot", font_size=26, color=WHITE))
                dot_terms.append(MathTex(f"i_{{{x}}}", font_size=26, color=C_INPUT))
            dot_terms.append(MathTex(r"=", font_size=26, color=WHITE))
            dot_terms.append(MathTex(f"h_{{{j}}}", font_size=26, color=C_HIDDEN))
            dot_eq = VGroup(*dot_terms).arrange(RIGHT, buff=0.10)
            dot_eq.next_to(mat_eq, DOWN, buff=0.7)

            hj_box = SurroundingRectangle(h_vis[j], color=hl, buff=0.1, stroke_width=2)

            self.play(
                Create(w_box),
                Create(i_box),
                FadeIn(dot_eq, shift=UP * 0.1),
                run_time=0.5,
            )
            self.play(
                Create(hj_box),
                h_vis[j].animate.set_color(hl),
                run_time=0.3,
            )
            self.next_slide()

            # Reset highlights
            self.play(
                FadeOut(w_box),
                FadeOut(i_box),
                FadeOut(hj_box),
                FadeOut(dot_eq),
                *[w_vis[j][x].animate.set_color(C_ORANGE) for x in range(n_inputs)],
                *[i_vis[x].animate.set_color(C_INPUT) for x in range(n_inputs)],
                h_vis[j].animate.set_color(C_HIDDEN),
                run_time=0.4,
            )

        self.next_slide()

        # ═══════════════════════════════════════════════════════════════════
        # ── Grow bold symbols from matrix centers, then form equation ────
        # ═══════════════════════════════════════════════════════════════════
        # Find centers of each matrix/vector (all entries stay visible)
        w_center = VGroup(
            *[w_vis[j][x] for j in range(n_hidden) for x in range(n_inputs)]
        ).get_center()
        i_center = VGroup(*i_vis).get_center()
        h_center = VGroup(*h_vis).get_center()

        # Bold collective symbols (same font size as final equation)
        W_sym = MathTex(r"\mathbf{W}", font_size=48, color=C_ORANGE).move_to(w_center)
        i_sym = MathTex(r"\mathbf{i}", font_size=48, color=C_INPUT).move_to(i_center)
        h_sym = MathTex(r"\mathbf{h}", font_size=48, color=C_HIDDEN).move_to(h_center)

        # Grow them from the center of each matrix/vector
        self.play(
            GrowFromCenter(W_sym),
            GrowFromCenter(i_sym),
            GrowFromCenter(h_sym),
            run_time=0.7,
        )
        self.next_slide()

        # Build the equation target below the matrices
        eq_final = VGroup(
            MathTex(r"\mathbf{h}", font_size=48, color=C_HIDDEN),
            MathTex("=", font_size=48, color=WHITE),
            MathTex(r"\mathbf{W}", font_size=48, color=C_ORANGE),
            MathTex(r"\mathbf{i}", font_size=48, color=C_INPUT),
        )
        eq_final.arrange(RIGHT, buff=0.12)
        eq_final.next_to(mat_eq, DOWN, buff=0.55)

        # Move the grown symbols to their equation positions + reveal =
        self.play(
            h_sym.animate.move_to(eq_final[0].get_center()),
            W_sym.animate.move_to(eq_final[2].get_center()),
            i_sym.animate.move_to(eq_final[3].get_center()),
            FadeIn(eq_final[1]),
            run_time=0.8,
        )
        self.add(eq_final)
        self.remove(h_sym, W_sym, i_sym)

        self.next_slide()
        # ═══════════════════════════════════════════════════════════════════
        # ── Show equivalence: network = matrix multiplication ────────────
        # ═══════════════════════════════════════════════════════════════════
        # Fade out the top equations and old matrix elements
        old_matrix_stuff = VGroup(mat_eq, *all_is, *w_vis, *i_vis, *h_vis)
        self.play(
            FadeOut(all_eq),
            FadeOut(old_matrix_stuff),
            run_time=0.4,
        )

        final_group = VGroup(
            [net_group.copy().set_opacity(0), eq_final.copy().set_opacity(0)]
        )
        final_group.arrange(RIGHT, buff=3)
        final_group.move_to(ORIGIN)

        self.play(
            # FadeIn(mat_eq_right, scale=0.8),
            # FadeIn(bold_eq, shift=UP * 0.1),
            FadeIn(VGroup(*[n for layer in neurons for n in layer], *edges.values())),
            # *[n.animate.set_opacity(1) for layer in neurons for n in layer],
            # *[e.animate.set_stroke(opacity=0.2) for e in edges.values()],
            net_group.animate.move_to(final_group[0].get_center()),
            eq_final.animate.move_to(final_group[1].get_center()),
            run_time=0.8,
        )

        self.next_slide()

        final_summary = Tex("These two representations are equivalent!", color=WHITE)
        final_summary.next_to(DOWN, final_group.get_bottom(), buff=0.5)
        self.play(Create(final_summary))

        self.play(
            LaggedStart(
                Circumscribe(final_group[0]),
                Circumscribe(final_group[1]),
                lag_ratio=0.75,
            )
        )
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
