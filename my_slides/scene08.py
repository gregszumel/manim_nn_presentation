from manim import *
from manim_slides import Slide
from my_slides.shared import *
import numpy as np


def _sig(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20.0, 20.0)))


def _clip_line_to_box(cx, cy, dx, dy, xmin=-0.3, xmax=1.6, ymin=-0.3, ymax=1.6):
    """Return two endpoints of the line through (cx,cy) with direction (dx,dy) clipped to the box."""
    eps = 1e-9
    t_vals = []
    if abs(dx) > eps:
        for x in [xmin, xmax]:
            t = (x - cx) / dx
            y = cy + t * dy
            if ymin - eps <= y <= ymax + eps:
                t_vals.append(t)
    if abs(dy) > eps:
        for y in [ymin, ymax]:
            t = (y - cy) / dy
            x = cx + t * dx
            if xmin - eps <= x <= xmax + eps:
                t_vals.append(t)
    if len(t_vals) < 2:
        return None
    t_min, t_max = min(t_vals), max(t_vals)
    return (cx + t_min * dx, cy + t_min * dy), (cx + t_max * dx, cy + t_max * dy)


# ══════════════════════════════════════════════════════════════════
# Slide 8 — Activation = a soft if-statement
# ══════════════════════════════════════════════════════════════════
class Slide08Activations(Slide):
    def construct(self):
        self.next_slide()

        # ── Part 0: No activation → layers collapse into one linear model ──
        title = section_title("without activations: just a linear model")
        self.play(FadeIn(title), run_time=0.5)

        # 1 → 1 → 1 network (no σ)
        IN  = np.array([-5.0, -0.2, 0.0])
        HID = np.array([-1.5, -0.2, 0.0])
        OUT = np.array([ 1.5, -0.2, 0.0])

        def _circle(pos, col):
            c = Circle(radius=0.32, fill_color=DARK_BG, fill_opacity=1,
                       stroke_color=col, stroke_width=2.5)
            c.move_to(pos).set_z_index(2)
            return c

        in_c  = _circle(IN,  C_INPUT)
        hid_c = _circle(HID, C_HIDDEN)
        out_c = _circle(OUT, C_OUTPUT)
        x_lbl = Text("x", font_size=14, color=C_INPUT ).move_to(IN ).set_z_index(3)
        y_lbl = Text("y", font_size=14, color=C_OUTPUT).move_to(OUT).set_z_index(3)

        e0 = Line(IN,  HID, stroke_color=C_EDGE, stroke_width=2, stroke_opacity=0.6)
        e1 = Line(HID, OUT, stroke_color=C_EDGE, stroke_width=2, stroke_opacity=0.6)

        no_sig_lbl = Text("no σ", font_size=12, color=C_RED).next_to(hid_c, UP, buff=0.1)
        w0_lbl = MathTex("w_0", font_size=18, color=C_YELLOW).move_to((IN + HID) / 2 + UP * 0.28)
        w1_lbl = MathTex("w_1", font_size=18, color=C_YELLOW).move_to((HID + OUT) / 2 + UP * 0.28)

        self.play(
            FadeIn(in_c, hid_c, out_c, x_lbl, y_lbl, no_sig_lbl),
            Create(e0), Create(e1),
            FadeIn(w0_lbl, w1_lbl),
            run_time=0.7,
        )
        self.next_slide()

        # Equations — build up step by step
        eq_x = 4.0
        eq1 = MathTex(r"h = w_0 \cdot x",         font_size=26, color=WHITE   ).shift(RIGHT * eq_x + UP * 1.1)
        eq2 = MathTex(r"y = w_1 \cdot h",         font_size=26, color=WHITE   ).shift(RIGHT * eq_x + UP * 0.3)
        eq3 = MathTex(r"y = w_1 w_0 \cdot x",     font_size=26, color=C_YELLOW).shift(RIGHT * eq_x + DOWN * 0.5)
        eq4 = MathTex(r"y = w_{\!c} \cdot x",     font_size=26, color=C_GREEN ).shift(RIGHT * eq_x + DOWN * 1.4)

        self.play(Write(eq1), run_time=0.5)
        self.next_slide()
        self.play(Write(eq2), run_time=0.5)
        self.next_slide()
        self.play(Write(eq3), run_time=0.5)
        self.next_slide()

        # Collapse the hidden layer
        cap0 = Text("the two weights multiply into one — the hidden layer adds nothing",
                    font_size=16, color=C_GREY).to_edge(DOWN, buff=0.5)
        direct_edge = Line(IN, OUT, stroke_color=C_GREEN, stroke_width=2.5)
        wc_lbl = MathTex(r"w_{\!c}", font_size=18, color=C_GREEN).move_to(
            (IN + OUT) / 2 + DOWN * 0.3)

        self.play(
            FadeOut(hid_c, no_sig_lbl, e0, e1, w0_lbl, w1_lbl),
            Create(direct_edge), FadeIn(wc_lbl, cap0),
            Write(eq4),
            run_time=0.8,
        )
        self.next_slide()

        cap0b = Text("no matter how many layers: without σ, the whole network is just one linear function",
                     font_size=16, color=C_GREY).to_edge(DOWN, buff=0.5)
        self.play(Transform(cap0, cap0b), run_time=0.4)
        self.next_slide()

        # Clean up; transition title
        title2 = section_title("activation = a soft if-statement")
        self.play(
            FadeOut(VGroup(in_c, out_c, x_lbl, y_lbl, direct_edge, wc_lbl,
                           eq1, eq2, eq3, eq4, cap0)),
            Transform(title, title2),
            run_time=0.5,
        )
        self.next_slide()

        # ── Part 1: 1D sigmoid — weight controls slope ───────────────
        axes_1d = Axes(
            x_range=[-4, 4, 1],
            y_range=[-0.05, 1.1, 0.5],
            x_length=6.5,
            y_length=3.2,
            axis_config={"color": C_GREY, "include_tip": True, "tip_length": 0.15},
        ).shift(RIGHT * 0.8 + DOWN * 0.4)

        x_lbl = axes_1d.get_x_axis_label("x", direction=RIGHT, buff=0.1)
        y_lbl = axes_1d.get_y_axis_label(r"\sigma(wx+b)", direction=UP, buff=0.1)

        w_t = ValueTracker(1.0)
        b_t = ValueTracker(0.0)

        curve_1d = always_redraw(lambda: axes_1d.plot(
            lambda x: _sig(w_t.get_value() * x + b_t.get_value()),
            color=C_GREEN, stroke_width=3,
        ))

        thresh = DashedLine(
            axes_1d.c2p(-4, 0.5), axes_1d.c2p(4, 0.5),
            color=C_GREY, stroke_opacity=0.4, dash_length=0.12,
        )

        w_disp = always_redraw(lambda: MathTex(
            rf"w = {w_t.get_value():.1f}", font_size=22, color=C_YELLOW,
        ).shift(LEFT * 4.2 + UP * 1.2))

        b_disp = always_redraw(lambda: MathTex(
            rf"b = {b_t.get_value():.1f}", font_size=22, color=C_ORANGE,
        ).shift(LEFT * 4.2 + UP * 0.5))

        self.play(Create(axes_1d), Write(x_lbl), Write(y_lbl), run_time=0.6)
        self.add(curve_1d, w_disp, b_disp)
        self.play(FadeIn(thresh), run_time=0.4)
        self.next_slide()

        # Steepen slope
        cap = Text("larger weight  →  steeper slope  →  sharper threshold",
                   font_size=17, color=C_GREY).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(cap), run_time=0.3)
        self.play(w_t.animate.set_value(10.0), run_time=2.0)
        self.next_slide()

        # Shift threshold with bias
        cap2 = Text("bias shifts where it fires — it's the 'when' of the if-statement",
                    font_size=17, color=C_ORANGE).to_edge(DOWN, buff=0.5)
        self.play(w_t.animate.set_value(6.0), Transform(cap, cap2), run_time=0.6)
        self.play(b_t.animate.set_value(-3.0), run_time=1.0)
        self.next_slide()
        self.play(b_t.animate.set_value(3.0), run_time=1.5)
        self.next_slide()

        # ── Part 2: 2D — one neuron = one line boundary ──────────────
        self.play(
            FadeOut(VGroup(axes_1d, x_lbl, y_lbl, thresh, cap)),
            run_time=0.4,
        )
        self.remove(curve_1d, w_disp, b_disp)

        axes_2d = Axes(
            x_range=[-0.3, 1.6, 1],
            y_range=[-0.3, 1.6, 1],
            x_length=4.0,
            y_length=4.0,
            axis_config={"color": C_GREY, "include_tip": True},
            x_axis_config={"numbers_to_include": [0, 1]},
            y_axis_config={"numbers_to_include": [0, 1]},
        ).shift(RIGHT * 1.5 + DOWN * 0.2)

        ax0_lbl = axes_2d.get_x_axis_label("x_0", direction=RIGHT, buff=0.1)
        ax1_lbl = axes_2d.get_y_axis_label("x_1", direction=UP, buff=0.1)

        # OR: (0,0)=off, rest=on
        or_labels  = {(0, 0): False, (1, 0): True,  (0, 1): True,  (1, 1): True }
        # XOR: (0,0)=off, (1,1)=off, rest=on
        xor_labels = {(0, 0): False, (1, 0): True,  (0, 1): True,  (1, 1): False}

        pts = [(0, 0), (1, 0), (0, 1), (1, 1)]

        def make_dots(labels):
            return VGroup(*[
                Dot(axes_2d.c2p(x0, x1), radius=0.14,
                    color=C_GREEN if labels[(x0, x1)] else C_RED).set_z_index(5)
                for x0, x1 in pts
            ])

        or_dots  = make_dots(or_labels)
        xor_dots = make_dots(xor_labels)

        pt_lbls = VGroup(*[
            Text(f"({x0},{x1})", font_size=11, color=C_GREY)
            .next_to(axes_2d.c2p(x0, x1), UR, buff=0.08)
            for x0, x1 in pts
        ])

        legend = VGroup(
            VGroup(Dot(color=C_GREEN, radius=0.08),
                   Text("= 1", font_size=13, color=C_GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Dot(color=C_RED,   radius=0.08),
                   Text("= 0", font_size=13, color=C_RED  )).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, buff=0.15).shift(LEFT * 4.8 + UP * 0.5)

        self.play(Create(axes_2d), Write(ax0_lbl), Write(ax1_lbl), run_time=0.6)
        self.play(FadeIn(or_dots, pt_lbls, legend), run_time=0.5)

        cap_or = Text("OR gate:  can one neuron separate green from red?",
                      font_size=17, color=C_GREY).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(cap_or), run_time=0.3)
        self.next_slide()

        # OR decision boundary: w0=1, w1=1, b=-0.5  →  x1 = -x0 + 0.5
        or_line = axes_2d.plot(
            lambda x: -x + 0.5, x_range=[-0.3, 0.8],
            color=C_YELLOW, stroke_width=3,
        )
        one_neuron_lbl = Text("1 neuron\n= 1 line", font_size=13, color=C_YELLOW,
                              line_spacing=1.2).shift(LEFT * 4.8 + DOWN * 0.5)

        cap_or2 = Text("yes! — a single neuron draws one line, and OR is solvable",
                       font_size=17, color=C_YELLOW).to_edge(DOWN, buff=0.5)
        self.play(Create(or_line), FadeIn(one_neuron_lbl), run_time=0.6)
        self.play(Transform(cap_or, cap_or2), run_time=0.3)
        self.next_slide()

        # Switch to XOR — (1,1) flips to red
        cap_xor = Text("XOR: flip (1,1) to 0 — now try to draw that line",
                       font_size=17, color=C_GREY).to_edge(DOWN, buff=0.5)
        self.play(
            Transform(or_dots, xor_dots),
            FadeOut(or_line, one_neuron_lbl),
            Transform(cap_or, cap_xor),
            run_time=0.6,
        )
        self.next_slide()

        # Rotating line — any angle misclassifies at least one XOR point
        theta_t = ValueTracker(0.3)

        def make_fail_line():
            th = theta_t.get_value()
            dx, dy = np.cos(th + PI / 2), np.sin(th + PI / 2)
            # Rotate around a point slightly off-center toward the XOR region
            cx, cy = 0.6, 0.6
            result = _clip_line_to_box(cx, cy, dx, dy)
            if result is None:
                return Line(axes_2d.c2p(0, 0), axes_2d.c2p(1, 1),
                            color=C_RED, stroke_width=2.5)
            p1, p2 = result
            return Line(axes_2d.c2p(*p1), axes_2d.c2p(*p2),
                        color=C_RED, stroke_width=2.5)

        fail_line = always_redraw(make_fail_line)
        cap_fail = Text("no single line works — XOR is not linearly separable",
                        font_size=17, color=C_RED).to_edge(DOWN, buff=0.5)
        self.add(fail_line)
        self.play(Transform(cap_or, cap_fail), run_time=0.3)
        self.play(theta_t.animate.set_value(0.3 + 2 * PI), run_time=4.0, rate_func=linear)
        self.next_slide()

        self.remove(fail_line)

        # ── Part 3: Two neurons = two lines → XOR ────────────────────
        cap_solve = Text("two neurons = two lines — together they carve out XOR",
                         font_size=17, color=C_GREEN).to_edge(DOWN, buff=0.5)
        self.play(Transform(cap_or, cap_solve), run_time=0.4)

        # Neuron 1: x0+x1=0.5  →  x1 = -x0 + 0.5  (lower boundary)
        # Neuron 2: x0+x1=1.5  →  x1 = -x0 + 1.5  (upper boundary)
        # XOR region: 0.5 < x0+x1 < 1.5
        line1 = axes_2d.plot(lambda x: -x + 0.5, x_range=[-0.3, 0.8],
                             color=C_GREEN, stroke_width=2.5)
        line2 = axes_2d.plot(lambda x: -x + 1.5, x_range=[-0.1, 1.6],
                             color=C_YELLOW, stroke_width=2.5)

        # Shaded XOR strip: the diagonal band between the two lines, clipped to axes
        region = Polygon(
            axes_2d.c2p(-0.3, 0.8),   # line1 @ left edge
            axes_2d.c2p(0.8,  -0.3),  # line1 @ bottom edge
            axes_2d.c2p(1.6,  -0.3),  # bottom-right corner of strip
            axes_2d.c2p(1.6,  -0.1),  # line2 @ right edge
            axes_2d.c2p(-0.1,  1.6),  # line2 @ top edge
            axes_2d.c2p(-0.3,  1.6),  # top-left corner of strip
            fill_color=C_GREEN, fill_opacity=0.18, stroke_width=0,
        )

        lbl1 = Text("neuron 1", font_size=13, color=C_GREEN).next_to(
            axes_2d.c2p(-0.3, 0.8), LEFT, buff=0.12)
        lbl2 = Text("neuron 2", font_size=13, color=C_YELLOW).next_to(
            axes_2d.c2p(-0.1, 1.6), UP, buff=0.12)

        self.play(FadeIn(region), Create(line1), Create(line2), run_time=0.8)
        self.play(FadeIn(lbl1, lbl2), run_time=0.3)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
