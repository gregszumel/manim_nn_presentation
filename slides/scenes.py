"""
All 21 slide scenes for the neural networks talk.

Render a single scene:
    manim-slides render slides/scenes.py Slide01Goals
Present:
    manim-slides present Slide01Goals Slide02BasicNetwork ...
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
from manim_slides import Slide
import numpy as np

# ── Palette ────────────────────────────────────────────────────────
C_INPUT  = "#5B9BD5"
C_HIDDEN = "#70AD47"
C_OUTPUT = "#ED7D31"
C_EDGE   = "#888888"
DARK_BG  = "#1a1a2e"
C_YELLOW = "#FFD966"
C_ORANGE = "#FF8C42"
C_GREEN  = "#69db7c"
C_RED    = "#FF6B6B"
C_GREY   = "#AAAAAA"
C_CLAIM  = "#A8C4E0"


# ── Shared helpers ─────────────────────────────────────────────────

def build_network(layer_sizes, h_spacing=2.2, v_spacing=1.0, colors=None):
    if colors is None:
        colors = [C_INPUT] + [C_HIDDEN] * (len(layer_sizes) - 2) + [C_OUTPUT]
    neurons = []
    for l, (n, col) in enumerate(zip(layer_sizes, colors)):
        layer = []
        total_h = (n - 1) * v_spacing
        for i in range(n):
            c = Circle(radius=0.32, stroke_color=col, stroke_width=2.0,
                       fill_color=DARK_BG, fill_opacity=0.9)
            c.move_to(np.array([l * h_spacing, total_h / 2 - i * v_spacing, 0]))
            layer.append(c)
        neurons.append(layer)
    edges = {}
    for l in range(len(layer_sizes) - 1):
        for i, src in enumerate(neurons[l]):
            for j, dst in enumerate(neurons[l + 1]):
                edges[(l, i, j)] = Line(
                    src.get_center(), dst.get_center(),
                    stroke_color=C_EDGE, stroke_width=0.8, stroke_opacity=0.4,
                )
    all_mobs = VGroup(*[m for layer in neurons for m in layer], *edges.values())
    all_mobs.center()
    return neurons, edges, all_mobs


def section_title(text, font_size=36):
    t = Text(text, font_size=font_size, slant=ITALIC)
    t.to_edge(UP, buff=0.5)
    return t


# ══════════════════════════════════════════════════════════════════
# Slide 1 — Goals
# ══════════════════════════════════════════════════════════════════
class Slide01Goals(Slide):
    def construct(self):
        self.next_slide()

        title = Text("neural networks: the math that matters", font_size=40, slant=ITALIC)
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=UP * 0.1), run_time=0.8)

        underline = Line(
            title.get_left() + DOWN * 0.15, title.get_right() + DOWN * 0.15,
            stroke_color=WHITE, stroke_width=1, stroke_opacity=0.4,
        )
        self.play(Create(underline), run_time=0.4)
        self.next_slide()

        goals = [
            "neural networks are just math — we can reason about them",
            "evaluations are critical for understanding model behavior",
            "prompting / agent orchestration is pseudo-finetuning",
            "ML summer series: zero to your own LLM in 12 weeks",
        ]
        goal_mobs = VGroup(*[Text(g, font_size=27) for g in goals])
        goal_mobs.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        goal_mobs.next_to(underline, DOWN, buff=0.55).to_edge(LEFT, buff=1.0)
        for m in goal_mobs:
            m.set_opacity(0)
        self.add(goal_mobs)

        for m in goal_mobs:
            self.play(m.animate.set_opacity(1.0), run_time=0.45)
            self.next_slide()

        # self.play(FadeOut(VGroup(title, underline, goal_mobs)))


# ══════════════════════════════════════════════════════════════════
# Slide 2 — Basic Neural Network
# ══════════════════════════════════════════════════════════════════
class Slide02BasicNetwork(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("a neural network")
        self.play(FadeIn(title), run_time=0.5)

        neurons, edges, net_group = build_network([3, 4, 2], h_spacing=2.5, v_spacing=0.9)
        net_group.center().shift(DOWN * 0.3)

        for layer in neurons:
            self.play(LaggedStart(*[FadeIn(n) for n in layer], lag_ratio=0.2), run_time=0.6)
        self.next_slide()

        layer_edges = [[] for _ in range(len(neurons) - 1)]
        for (l, i, j), e in edges.items():
            layer_edges[l].append(e)
        for l_edges in layer_edges:
            self.play(LaggedStart(*[Create(e) for e in l_edges], lag_ratio=0.04), run_time=0.7)
        self.next_slide()

        layer_labels_info = [
            (neurons[0], "input",  C_INPUT),
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

        act_label = Text("activations", font_size=22, color=C_YELLOW)
        act_label.next_to(neurons[1][0], UP, buff=0.55)
        act_arrow = Arrow(act_label.get_bottom(), neurons[1][0].get_top(),
                          buff=0.1, stroke_width=1.5, color=C_YELLOW)
        self.play(FadeIn(act_label), Create(act_arrow), run_time=0.5)
        self.next_slide()

        e_sample = edges[(0, 0, 1)]
        weight_label = Text("weights", font_size=22, color=C_ORANGE)
        weight_label.next_to(e_sample.get_center(), UP, buff=0.2)
        self.play(
            e_sample.animate.set_stroke(color=C_ORANGE, width=2.5),
            FadeIn(weight_label),
            run_time=0.5,
        )
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 3 — How One Neuron Computes
# ══════════════════════════════════════════════════════════════════
class Slide03SingleNeuron(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("how one neuron computes")
        self.play(FadeIn(title), run_time=0.5)

        neurons, edges, net_group = build_network([2, 1], h_spacing=3.0, v_spacing=1.2)
        net_group.shift(LEFT * 2.0 + DOWN * 0.3)
        self.play(
            *[FadeIn(n) for layer in neurons for n in layer],
            *[Create(e) for e in edges.values()],
            run_time=0.8,
        )
        self.next_slide()

        v0, v1, w0, w1, b = 0.5, 0.8, 0.6, -0.3, 0.1

        val0 = DecimalNumber(v0, num_decimal_places=1, font_size=26, color=C_INPUT)
        val1 = DecimalNumber(v1, num_decimal_places=1, font_size=26, color=C_INPUT)
        val0.move_to(neurons[0][0])
        val1.move_to(neurons[0][1])
        self.play(FadeIn(val0), FadeIn(val1), run_time=0.5)
        self.next_slide()

        w_lbl0 = MathTex(f"w_{{00}}={w0}", font_size=24, color=C_ORANGE)
        w_lbl1 = MathTex(f"w_{{10}}={w1}", font_size=24, color=C_ORANGE)
        w_lbl0.next_to(edges[(0, 0, 0)].get_center(), UP, buff=0.15)
        w_lbl1.next_to(edges[(0, 1, 0)].get_center(), DOWN, buff=0.15)
        self.play(
            edges[(0, 0, 0)].animate.set_stroke(color=C_ORANGE, width=2.5),
            edges[(0, 1, 0)].animate.set_stroke(color=C_ORANGE, width=2.5),
            FadeIn(w_lbl0), FadeIn(w_lbl1),
            run_time=0.6,
        )
        self.next_slide()

        eq = MathTex(
            r"h = ", r"0.5 \times 0.6", r" + ", r"0.8 \times (-0.3)",
            font_size=32,
        ).shift(RIGHT * 2.0 + UP * 0.5)
        eq[1].set_color(C_INPUT)
        eq[3].set_color(C_INPUT)
        self.play(Write(eq), run_time=0.9)
        self.next_slide()

        result = MathTex(r"h = 0.06", font_size=32, color=C_YELLOW)
        result.next_to(eq, DOWN, buff=0.35)
        self.play(Write(result), run_time=0.5)
        self.next_slide()

        bias_eq = MathTex(r"h = 0.06 + 0.1 \quad \text{(+ bias)}", font_size=30, color=C_GREEN)
        bias_eq.next_to(result, DOWN, buff=0.35)
        self.play(Write(bias_eq), run_time=0.6)
        self.next_slide()

        act_eq = MathTex(r"\text{output} = \sigma(h)", font_size=30, color=C_GREEN)
        act_eq.next_to(bias_eq, DOWN, buff=0.3)
        act_note = Text("activation function", font_size=18, color=C_GREY)
        act_note.next_to(act_eq, RIGHT, buff=0.3)
        self.play(Write(act_eq), FadeIn(act_note), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 4 — Equations
# ══════════════════════════════════════════════════════════════════
class Slide04Equations(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("writing it out")
        self.play(FadeIn(title), run_time=0.5)

        neurons, edges, net_group = build_network([2, 2, 1], h_spacing=2.2, v_spacing=1.1)
        net_group.shift(LEFT * 3.2 + DOWN * 0.2)
        self.play(
            *[FadeIn(n) for layer in neurons for n in layer],
            *[Create(e) for e in edges.values()],
            run_time=0.8,
        )
        self.next_slide()

        eq1 = MathTex(r"h_0 = i_0 \cdot w_{00} + i_1 \cdot w_{10}", font_size=30)
        eq2 = MathTex(r"h_1 = i_0 \cdot w_{01} + i_1 \cdot w_{11}", font_size=30)
        VGroup(eq1, eq2).arrange(DOWN, buff=0.5).shift(RIGHT * 2.0 + UP * 0.3)

        self.play(
            neurons[1][0].animate.set_stroke(color=C_YELLOW, width=3),
            Write(eq1),
            run_time=0.8,
        )
        self.next_slide()

        self.play(
            neurons[1][0].animate.set_stroke(color=C_HIDDEN, width=2),
            neurons[1][1].animate.set_stroke(color=C_YELLOW, width=3),
            Write(eq2),
            run_time=0.8,
        )
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 5 — This Is Just Matrix Multiplication
# ══════════════════════════════════════════════════════════════════
class Slide05MatrixMult(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("this is just matrix multiplication")
        self.play(FadeIn(title), run_time=0.5)

        eq_scalar = VGroup(
            MathTex(r"h_0 = i_0 w_{00} + i_1 w_{10}", font_size=30),
            MathTex(r"h_1 = i_0 w_{01} + i_1 w_{11}", font_size=30),
        ).arrange(DOWN, buff=0.4).shift(UP * 1.2)
        self.play(FadeIn(eq_scalar), run_time=0.6)
        self.next_slide()

        eq_compact = MathTex(r"\mathbf{h} = \mathbf{W}\,\mathbf{i}", font_size=52)
        eq_compact.shift(LEFT * 1.5)
        expanded = MathTex(
            r"\begin{pmatrix} h_0 \\ h_1 \end{pmatrix} ="
            r"\begin{pmatrix} w_{00} & w_{10} \\ w_{01} & w_{11} \end{pmatrix}"
            r"\begin{pmatrix} i_0 \\ i_1 \end{pmatrix}",
            font_size=28,
        ).shift(RIGHT * 2.8)
        self.play(TransformFromCopy(eq_scalar, eq_compact), run_time=1.0)
        self.next_slide()
        self.play(Write(expanded), run_time=0.9)
        self.next_slide()

        punchline = Text("one layer  =  one matrix multiply", font_size=30, color=C_YELLOW)
        punchline.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(punchline, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 6 — Two Layers, No Activation
# ══════════════════════════════════════════════════════════════════
class Slide06TwoLayers(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("two layers — no activation")
        self.play(FadeIn(title), run_time=0.5)

        neurons, edges, net_group = build_network([2, 2, 1], h_spacing=2.2, v_spacing=1.1)
        net_group.shift(LEFT * 3.8 + DOWN * 0.2)
        self.play(
            *[FadeIn(n) for layer in neurons for n in layer],
            *[Create(e) for e in edges.values()],
            run_time=0.8,
        )
        self.next_slide()

        eq1 = MathTex(r"\mathbf{h} = \mathbf{W_0}\,\mathbf{i}", font_size=34)
        eq2 = MathTex(r"\mathbf{o} = \mathbf{W_1}\,\mathbf{h}", font_size=34)
        eqs = VGroup(eq1, eq2).arrange(DOWN, buff=0.4).shift(RIGHT * 1.2 + UP * 1.2)
        self.play(Write(eq1), run_time=0.6)
        self.next_slide()
        self.play(Write(eq2), run_time=0.6)
        self.next_slide()

        sub = MathTex(r"\mathbf{o} = \mathbf{W_1}(\mathbf{W_0}\,\mathbf{i})", font_size=34)
        sub.next_to(eqs, DOWN, buff=0.45)
        self.play(Write(sub), run_time=0.7)
        self.next_slide()

        collapse = MathTex(
            r"\mathbf{o} = \underbrace{(\mathbf{W_1 W_0})}_{\mathbf{W^*}}\,\mathbf{i}",
            font_size=34, color=C_RED,
        )
        collapse.next_to(sub, DOWN, buff=0.4)
        self.play(Write(collapse), run_time=0.8)
        self.next_slide()

        punchline = Text("still just one matrix — no matter how many layers", font_size=26, color=C_RED)
        punchline.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(punchline, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 7 — Activation Functions
# ══════════════════════════════════════════════════════════════════
class Slide07Activations(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("activation functions")
        self.play(FadeIn(title), run_time=0.5)

        eq1 = MathTex(r"\mathbf{h} = \sigma(\mathbf{W_0}\,\mathbf{i})", font_size=38)
        eq2 = MathTex(r"\mathbf{o} = \mathbf{W_1}\,\sigma(\mathbf{W_0}\,\mathbf{i})", font_size=38)
        VGroup(eq1, eq2).arrange(DOWN, buff=0.5).shift(LEFT * 1.5 + UP * 0.6)

        self.play(Write(eq1), run_time=0.7)
        self.next_slide()
        self.play(Write(eq2), run_time=0.7)
        self.next_slide()

        no_collapse = Text("σ blocks the collapse — layers stay distinct", font_size=26, color=C_GREEN)
        no_collapse.shift(LEFT * 1.5 + DOWN * 0.8)
        self.play(FadeIn(no_collapse, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        axes = Axes(
            x_range=[-2, 2, 1], y_range=[-0.3, 2, 0.5],
            x_length=3.5, y_length=2.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(RIGHT * 3.2 + DOWN * 0.4)
        relu = axes.plot(lambda x: max(0.0, x), x_range=[-2, 2], color=C_ORANGE, stroke_width=2.5)
        relu_label = Text("ReLU  —  fires past threshold", font_size=20, color=C_ORANGE)
        relu_label.next_to(axes, DOWN, buff=0.2)

        self.play(Create(axes), run_time=0.5)
        self.play(Create(relu), FadeIn(relu_label), run_time=0.7)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 8 — XOR Problem
# ══════════════════════════════════════════════════════════════════
class Slide08XOR(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("the XOR problem")
        self.play(FadeIn(title), run_time=0.5)

        axes = Axes(
            x_range=[-0.4, 1.6, 1], y_range=[-0.4, 1.6, 1],
            x_length=4.5, y_length=4.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(LEFT * 2.2 + DOWN * 0.3)

        x_lbl = MathTex("x_0", font_size=26).next_to(axes.get_x_axis(), DOWN, buff=0.2)
        y_lbl = MathTex("x_1", font_size=26).next_to(axes.get_y_axis(), LEFT, buff=0.2)
        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.7)
        self.next_slide()

        xor_data = [((0, 0), 0), ((1, 1), 0), ((0, 1), 1), ((1, 0), 1)]
        dots = []
        for (x, y), cls in xor_data:
            color = C_RED if cls == 0 else C_INPUT
            d = Dot(axes.c2p(x, y), radius=0.16, color=color, fill_opacity=0.9)
            dots.append(d)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.3), run_time=0.8)
        self.next_slide()

        fail_lines = [
            axes.plot(lambda x: 0.5 + 0 * x, color=C_GREY, stroke_width=1.5, stroke_opacity=0.6),
            axes.plot(lambda x: x, color=C_GREY, stroke_width=1.5, stroke_opacity=0.6),
            axes.plot(lambda x: -x + 1, color=C_GREY, stroke_width=1.5, stroke_opacity=0.6),
        ]
        fail_label = Text("no line separates these", font_size=24, color=C_RED)
        fail_label.shift(RIGHT * 3.0 + UP * 0.5)

        for fl in fail_lines:
            self.play(Create(fl), run_time=0.5)
            self.next_slide()
            self.play(fl.animate.set_stroke(opacity=0.2), run_time=0.3)

        self.play(FadeIn(fail_label, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        solution = Text("add hidden layer + activation", font_size=24, color=C_GREEN)
        solution.next_to(fail_label, DOWN, buff=0.4)
        result = Text("→  now separable", font_size=24, color=C_GREEN)
        result.next_to(solution, DOWN, buff=0.2)

        self.play(FadeIn(solution), run_time=0.5)
        self.play(FadeIn(result), run_time=0.5)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 9 — Universal Function Approximators
# ══════════════════════════════════════════════════════════════════
class Slide09UniversalApprox(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("universal function approximators")
        self.play(FadeIn(title), run_time=0.5)

        rng = np.random.default_rng(42)
        rand_xs = np.linspace(-1.8, 1.8, 6)
        rand_ys = rng.uniform(-1.4, 1.4, 6)
        rand_coeffs = np.polyfit(rand_xs, rand_ys, deg=5)
        rand_poly = np.poly1d(rand_coeffs)

        specs = [
            ("linear",      lambda x: 0.6 * x,                  C_INPUT,  False),
            ("quadratic",   lambda x: x ** 2 - 1.0,             C_GREEN,  False),
            ("exponential", lambda x: np.exp(0.8 * x) - 1.5,   C_ORANGE, False),
            ("random",      None,                                C_RED,    True),
        ]

        all_axes, all_true, all_nn = [], [], []

        for i, (name, fn, color, is_rand) in enumerate(specs):
            col_i, row_i = i % 2, i // 2
            ax = Axes(
                x_range=[-2, 2, 1], y_range=[-2.5, 2.5, 1],
                x_length=3.0, y_length=2.5,
                axis_config={"stroke_width": 1.0, "stroke_color": C_GREY},
                tips=False,
            ).shift(RIGHT * (col_i * 3.6 - 1.8) + DOWN * (row_i * 3.2 - 0.6))
            lbl = Text(name, font_size=18, color=color).next_to(ax, UP, buff=0.1)

            if not is_rand:
                true_mob = ax.plot(fn, x_range=[-1.9, 1.9], color=color, stroke_width=2.5)
                nn_mob = DashedVMobject(
                    ax.plot(
                        lambda x, f=fn: f(x) + 0.07 * np.sin(4 * x),
                        x_range=[-1.9, 1.9], color=WHITE, stroke_width=1.5,
                    ),
                    num_dashes=30, dashed_ratio=0.5,
                )
            else:
                true_mob = VGroup(*[
                    Dot(ax.c2p(x, y), radius=0.07, color=C_RED, fill_opacity=0.85)
                    for x, y in zip(rand_xs, rand_ys)
                ])
                nn_mob = DashedVMobject(
                    ax.plot(rand_poly, x_range=[-1.75, 1.75], color=WHITE, stroke_width=1.5),
                    num_dashes=30, dashed_ratio=0.5,
                )

            all_axes.append((ax, lbl))
            all_true.append(true_mob)
            all_nn.append(nn_mob)

        for ax, lbl in all_axes:
            self.play(Create(ax), FadeIn(lbl), run_time=0.35)

        for mob in all_true:
            anim = FadeIn(mob) if isinstance(mob, VGroup) else Create(mob)
            self.play(anim, run_time=0.45)

        self.next_slide()

        for mob in all_nn:
            self.play(Create(mob), run_time=0.4)

        punchline = Text("NNs can approximate any function", font_size=28, color=C_YELLOW)
        punchline.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(punchline, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 10 — Real World: Images & Audio
# ══════════════════════════════════════════════════════════════════
class Slide10RealWorld(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("but these are just numbers")
        self.play(FadeIn(title), run_time=0.5)

        # 4×4 pixel grid (stylised cat)
        pixel_colors = [
            ["#FF8C42", "#FF8C42", "#AAAAAA", "#AAAAAA"],
            ["#FF8C42", "#FFDD88", "#FFDD88", "#AAAAAA"],
            ["#AAAAAA", "#FFDD88", "#FFDD88", "#FF8C42"],
            ["#AAAAAA", "#AAAAAA", "#FF8C42", "#FF8C42"],
        ]
        ps = 0.38
        pixels = VGroup(*[
            Square(side_length=ps, fill_color=pixel_colors[r][c], fill_opacity=1,
                   stroke_color=DARK_BG, stroke_width=1)
            .move_to(np.array([c * ps, -r * ps, 0]))
            for r in range(4) for c in range(4)
        ]).center().shift(LEFT * 5.2 + UP * 0.5)
        cat_label = Text("image", font_size=20, color=C_GREY).next_to(pixels, DOWN, buff=0.2)

        self.play(FadeIn(pixels), FadeIn(cat_label), run_time=0.6)
        self.next_slide()

        flat_vals = [0.8, 0.8, 0.5, 0.5, 0.8, 0.9, 0.9, 0.5, 0.5, 0.9, 0.9, 0.8, 0.5, 0.5, 0.8, 0.8]
        num_mobs = VGroup(*[
            DecimalNumber(v, num_decimal_places=1, font_size=13, color=C_GREY)
            for v in flat_vals
        ]).arrange(RIGHT, buff=0.07).shift(LEFT * 2.5 + UP * 0.5)

        arr_flat = Arrow(pixels.get_right(), num_mobs.get_left(), buff=0.1,
                         stroke_width=1.5, color=C_GREY)
        self.play(Create(arr_flat), FadeIn(num_mobs), run_time=0.6)
        self.next_slide()

        _, _, net_img = build_network([4, 3, 2], h_spacing=1.4, v_spacing=0.65)
        net_img.shift(RIGHT * 0.8 + UP * 0.5)
        arr_net = Arrow(num_mobs.get_right(), net_img.get_left(), buff=0.1,
                        stroke_width=1.5, color=C_GREY)
        out_cat = Text('"cat"', font_size=26, color=C_GREEN).next_to(net_img, RIGHT, buff=0.4)

        self.play(Create(arr_net), FadeIn(net_img), run_time=0.6)
        self.play(FadeIn(out_cat), run_time=0.4)
        self.next_slide()

        # Audio waveform
        ax_audio = Axes(
            x_range=[0, 4 * PI, PI], y_range=[-1.5, 1.5, 1],
            x_length=3.0, y_length=1.6,
            axis_config={"stroke_width": 1.0, "stroke_color": C_GREY},
            tips=False,
        ).shift(LEFT * 4.5 + DOWN * 2.0)
        waveform = ax_audio.plot(
            lambda x: np.sin(x) * np.exp(-0.1 * x) * 1.2,
            x_range=[0, 4 * PI], color=C_INPUT, stroke_width=2,
        )
        audio_label = Text("audio", font_size=20, color=C_GREY).next_to(ax_audio, DOWN, buff=0.2)

        self.play(Create(ax_audio), Create(waveform), FadeIn(audio_label), run_time=0.7)
        self.next_slide()

        out_audio = Text('"Ten-four"', font_size=26, color=C_GREEN).shift(RIGHT * 1.0 + DOWN * 2.0)
        arr_audio = Arrow(ax_audio.get_right(), out_audio.get_left(), buff=0.2,
                          stroke_width=1.5, color=C_GREY)
        self.play(Create(arr_audio), FadeIn(out_audio), run_time=0.6)
        self.next_slide()

        tagline = Text("all just numbers — NNs approximate the function that maps them",
                       font_size=22, color=C_YELLOW)
        tagline.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(tagline, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 11 — Loss Landscape
# ══════════════════════════════════════════════════════════════════
class Slide11LossLandscape(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("how do we train?")
        self.play(FadeIn(title), run_time=0.5)

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[0, 5, 1],
            x_length=6.5, y_length=4.0,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(DOWN * 0.4)

        x_lbl = Text("weights", font_size=22, color=C_GREY).next_to(axes.get_x_axis(), DOWN, buff=0.3)
        y_lbl = Text("loss", font_size=22, color=C_GREY).next_to(axes.get_y_axis(), LEFT, buff=0.3)
        loss_curve = axes.plot(lambda x: x ** 2 + 0.3, x_range=[-2.8, 2.8],
                               color=C_INPUT, stroke_width=2.5)

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.7)
        self.play(Create(loss_curve), run_time=0.6)
        self.next_slide()

        sx = 2.5
        dot = Dot(axes.c2p(sx, sx ** 2 + 0.3), radius=0.14, color=C_YELLOW)
        self.play(FadeIn(dot), run_time=0.4)
        self.next_slide()

        grad_end_x = sx - 0.8
        grad_arrow = Arrow(
            axes.c2p(sx, sx ** 2 + 0.3),
            axes.c2p(grad_end_x, grad_end_x ** 2 + 0.3),
            buff=0.05, stroke_width=2, color=C_ORANGE,
        )
        grad_lbl = MathTex(r"-\frac{d\mathcal{L}}{dw}", font_size=28, color=C_ORANGE)
        grad_lbl.next_to(grad_arrow, UP, buff=0.15)
        self.play(Create(grad_arrow), FadeIn(grad_lbl), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(grad_arrow), FadeOut(grad_lbl), run_time=0.3)
        for nx in [1.8, 1.1, 0.5, 0.1]:
            self.play(dot.animate.move_to(axes.c2p(nx, nx ** 2 + 0.3)), run_time=0.35)

        bottom = Text("gradient descent — take small steps downhill", font_size=24, color=C_YELLOW)
        bottom.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(bottom, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 12 — Gradient Descent Loop
# ══════════════════════════════════════════════════════════════════
class Slide12GradientLoop(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("the training loop")
        self.play(FadeIn(title), run_time=0.5)

        steps = [
            "show example",
            "compute error",
            "nudge weights toward correct output",
            "repeat",
        ]
        boxes = VGroup()
        for step in steps:
            box = RoundedRectangle(corner_radius=0.15, width=5.5, height=0.75,
                                   stroke_color=C_INPUT, stroke_width=1.5,
                                   fill_color=DARK_BG, fill_opacity=0.9)
            lbl = Text(step, font_size=26).move_to(box)
            boxes.add(VGroup(box, lbl))
        boxes.arrange(DOWN, buff=0.45).center().shift(DOWN * 0.2)

        arrows = VGroup(*[
            Arrow(boxes[i].get_bottom(), boxes[i + 1].get_top(),
                  buff=0.05, stroke_width=2, color=C_GREY)
            for i in range(len(boxes) - 1)
        ])
        loop_arrow = CurvedArrow(
            boxes[-1].get_right() + UP * 0.1,
            boxes[0].get_right() + DOWN * 0.1,
            angle=-PI / 2,
            color=C_ORANGE, stroke_width=2,
        )

        for box in boxes:
            self.play(FadeIn(box), run_time=0.4)
            self.next_slide()

        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2), run_time=0.6)
        self.play(Create(loop_arrow), run_time=0.6)
        self.next_slide()

        warning = Text("push weights toward what we saw → eventually memorizes",
                       font_size=22, color=C_RED)
        warning.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(warning, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 13 — Back to the Random Function
# ══════════════════════════════════════════════════════════════════
class Slide13RandomFunction(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("back to the random function…")
        self.play(FadeIn(title), run_time=0.5)

        rng = np.random.default_rng(42)
        rand_xs = np.linspace(-1.8, 1.8, 6)
        rand_ys = rng.uniform(-1.4, 1.4, 6)
        coeffs = np.polyfit(rand_xs, rand_ys, deg=5)
        poly = np.poly1d(coeffs)

        axes = Axes(
            x_range=[-2.2, 2.2, 1], y_range=[-2, 2, 1],
            x_length=6.5, y_length=4.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(DOWN * 0.3)

        dots = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.11, color=C_RED, fill_opacity=0.9)
            for x, y in zip(rand_xs, rand_ys)
        ])
        self.play(Create(axes), run_time=0.6)
        self.play(FadeIn(dots), run_time=0.5)
        self.next_slide()

        fit = axes.plot(poly, x_range=[-1.75, 1.75], color=C_YELLOW, stroke_width=2.5)
        fit_lbl = Text("NN fits perfectly", font_size=24, color=C_YELLOW)
        fit_lbl.to_corner(UR).shift(DOWN * 1.5 + LEFT * 0.3)
        self.play(Create(fit), run_time=0.9)
        self.play(FadeIn(fit_lbl), run_time=0.4)
        self.next_slide()

        question = Text("wait — is it approximating randomness?", font_size=28, color=C_ORANGE)
        question.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(question, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 14 — Memorization
# ══════════════════════════════════════════════════════════════════
class Slide14Memorization(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("memorization")
        self.play(FadeIn(title), run_time=0.5)

        rng = np.random.default_rng(42)
        rand_xs = np.linspace(-1.8, 1.8, 6)
        rand_ys = rng.uniform(-1.4, 1.4, 6)
        coeffs = np.polyfit(rand_xs, rand_ys, deg=5)
        poly = np.poly1d(coeffs)

        ax_l = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-2, 2, 1],
            x_length=4.5, y_length=3.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.2},
            tips=False,
        ).shift(LEFT * 2.9 + DOWN * 0.4)
        lbl_l = Text("memorized", font_size=22, color=C_RED).next_to(ax_l, UP, buff=0.15)

        ax_r = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-2, 2, 1],
            x_length=4.5, y_length=3.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.2},
            tips=False,
        ).shift(RIGHT * 2.9 + DOWN * 0.4)
        lbl_r = Text("learned the function", font_size=22, color=C_GREEN).next_to(ax_r, UP, buff=0.15)

        self.play(
            Create(ax_l), FadeIn(lbl_l),
            Create(ax_r), FadeIn(lbl_r),
            run_time=0.7,
        )

        train_dots = VGroup(*[Dot(ax_l.c2p(x, y), radius=0.1, color=C_RED) for x, y in zip(rand_xs, rand_ys)])
        fit_l = ax_l.plot(poly, x_range=[-1.75, 1.75], color=C_YELLOW, stroke_width=2)

        lin_pts_y = 0.7 * rand_xs + 0.1 + rng.normal(0, 0.15, len(rand_xs))
        lin_dots = VGroup(*[Dot(ax_r.c2p(x, y), radius=0.1, color=C_GREEN) for x, y in zip(rand_xs, lin_pts_y)])
        fit_r = ax_r.plot(lambda x: 0.7 * x + 0.1, x_range=[-2.3, 2.3], color=C_YELLOW, stroke_width=2)

        self.play(FadeIn(train_dots), Create(fit_l), FadeIn(lin_dots), Create(fit_r), run_time=0.8)
        self.next_slide()

        # New point — memorized model fails
        new_x = 2.1
        clipped_y = float(np.clip(poly(new_x), -1.8, 1.8))
        new_dot_l = Dot(ax_l.c2p(new_x, clipped_y), radius=0.13, color=C_ORANGE)
        fail_lbl = Text("???", font_size=20, color=C_ORANGE).next_to(new_dot_l, UP, buff=0.1)
        self.play(FadeIn(new_dot_l), FadeIn(fail_lbl), run_time=0.5)
        self.next_slide()

        # New point — linear model extrapolates
        new_dot_r = Dot(ax_r.c2p(new_x, 0.7 * new_x + 0.1), radius=0.13, color=C_GREEN)
        extrap_lbl = Text("extrapolates!", font_size=20, color=C_GREEN).next_to(new_dot_r, UP, buff=0.1)
        self.play(FadeIn(new_dot_r), FadeIn(extrap_lbl), run_time=0.5)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 15 — Overfitting
# ══════════════════════════════════════════════════════════════════
class Slide15Overfitting(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("overfitting")
        self.play(FadeIn(title), run_time=0.5)

        rng = np.random.default_rng(7)
        xs = np.linspace(-2, 2, 12)
        ys = 0.5 * xs + rng.normal(0, 0.35, 12)

        axes = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-2, 2, 1],
            x_length=7.5, y_length=4.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(DOWN * 0.2)

        dots = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.09, color=WHITE, fill_opacity=0.85)
            for x, y in zip(xs, ys)
        ])
        self.play(Create(axes), run_time=0.6)
        self.play(FadeIn(dots), run_time=0.6)
        self.next_slide()

        good_fit = axes.plot(lambda x: 0.5 * x, x_range=[-2.3, 2.3],
                             color=C_GREEN, stroke_width=2.5)
        good_lbl = Text("good generalization", font_size=22, color=C_GREEN)
        good_lbl.to_corner(UL).shift(DOWN * 1.5 + RIGHT * 0.3)
        self.play(Create(good_fit), FadeIn(good_lbl), run_time=0.7)
        self.next_slide()

        overfit_coeffs = np.polyfit(xs, ys, deg=11)
        overfit_poly = np.poly1d(overfit_coeffs)
        bad_fit = axes.plot(overfit_poly, x_range=[-1.95, 1.95],
                            color=C_RED, stroke_width=2.5)
        bad_lbl = Text("overfitting — zero training error,\nbad generalization",
                       font_size=22, color=C_RED)
        bad_lbl.to_corner(UR).shift(DOWN * 1.5 + LEFT * 0.3)
        self.play(Create(bad_fit), FadeIn(bad_lbl), run_time=0.8)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 16 — Train / Val / Test
# ══════════════════════════════════════════════════════════════════
class Slide16TrainValTest(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("train  /  val  /  test")
        self.play(FadeIn(title), run_time=0.5)

        rng = np.random.default_rng(0)
        pool = VGroup(*[
            Dot(radius=0.09, color=C_GREY, fill_opacity=0.7).shift(
                RIGHT * rng.uniform(-0.8, 0.8) + UP * rng.uniform(-0.3, 0.3)
            ) for _ in range(18)
        ]).shift(LEFT * 4.5 + UP * 1.8)
        pool_lbl = Text("data", font_size=20, color=C_GREY).next_to(pool, UP, buff=0.15)
        self.play(FadeIn(pool), FadeIn(pool_lbl), run_time=0.6)
        self.next_slide()

        buckets_info = [("train", C_INPUT), ("val", C_GREEN), ("test", C_ORANGE)]
        buckets = VGroup()
        for i, (lbl, col) in enumerate(buckets_info):
            rect = RoundedRectangle(corner_radius=0.1, width=2.0, height=0.85,
                                    stroke_color=col, fill_color=DARK_BG, fill_opacity=0.85)
            rect.shift(LEFT * (2.2 - i * 2.5) + UP * 1.8)
            text = Text(lbl, font_size=22, color=col).move_to(rect)
            buckets.add(VGroup(rect, text))
        self.play(FadeIn(buckets), run_time=0.6)
        self.next_slide()

        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 2.2, 0.5],
            x_length=7.5, y_length=3.0,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(DOWN * 1.7)

        x_lbl = Text("training steps", font_size=20, color=C_GREY).next_to(axes.get_x_axis(), DOWN, buff=0.2)
        y_lbl = Text("loss", font_size=20, color=C_GREY).next_to(axes.get_y_axis(), LEFT, buff=0.2)

        train_curve = axes.plot(
            lambda t: 1.8 * np.exp(-0.35 * t) + 0.1,
            x_range=[0, 10], color=C_INPUT, stroke_width=2.5,
        )
        val_curve = axes.plot(
            lambda t: 1.8 * np.exp(-0.28 * t) + 0.3 + 0.04 * max(0, t - 4) ** 2,
            x_range=[0, 10], color=C_ORANGE, stroke_width=2.5,
        )

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.7)
        self.play(Create(train_curve), run_time=0.7)
        train_lbl = Text("train", font_size=20, color=C_INPUT).next_to(axes.c2p(9.8, 0.2), RIGHT, buff=0.05)
        self.play(FadeIn(train_lbl), run_time=0.3)
        self.next_slide()

        self.play(Create(val_curve), run_time=0.8)
        val_lbl = Text("val", font_size=20, color=C_ORANGE).next_to(axes.c2p(9.8, 0.9), RIGHT, buff=0.05)
        self.play(FadeIn(val_lbl), run_time=0.3)
        self.next_slide()

        vline = axes.get_vertical_line(axes.c2p(4, 0), color=C_RED, stroke_width=2)
        stop_lbl = Text("stop here", font_size=20, color=C_RED).next_to(axes.c2p(4, 1.4), RIGHT, buff=0.1)
        self.play(Create(vline), FadeIn(stop_lbl), run_time=0.5)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 17 — Simplified LLM Diagram
# ══════════════════════════════════════════════════════════════════
class Slide17LLMDiagram(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("LLMs are neural networks too")
        self.play(FadeIn(title), run_time=0.5)

        tokens_in  = ["The", "cat", "sat", "<PAD>", "<PAD>"]
        tokens_out = ["cat", "sat", "on",  "<PAD>", "<PAD>"]
        t_colors   = [C_INPUT, C_INPUT, C_INPUT, C_GREY, C_GREY]

        input_nodes = VGroup()
        output_nodes = VGroup()

        for i, (tok, col) in enumerate(zip(tokens_in, t_colors)):
            box = RoundedRectangle(corner_radius=0.1, width=1.4, height=0.55,
                                   stroke_color=col, fill_color=DARK_BG, fill_opacity=0.9)
            box.shift(LEFT * 3.5 + UP * (1.0 - i * 0.8))
            lbl = Text(tok, font_size=17, color=col).move_to(box)
            input_nodes.add(VGroup(box, lbl))

        for i, (tok, col) in enumerate(zip(tokens_out, t_colors)):
            box = RoundedRectangle(corner_radius=0.1, width=1.4, height=0.55,
                                   stroke_color=col, fill_color=DARK_BG, fill_opacity=0.9)
            box.shift(RIGHT * 3.5 + UP * (1.0 - i * 0.8))
            lbl = Text(tok, font_size=17, color=col).move_to(box)
            output_nodes.add(VGroup(box, lbl))

        self.play(FadeIn(input_nodes), FadeIn(output_nodes), run_time=0.7)
        self.next_slide()

        # Causal connections: output j can attend to inputs 0..j
        causal_lines = VGroup(*[
            Line(input_nodes[i].get_right(), output_nodes[j].get_left(),
                 stroke_color=C_EDGE, stroke_width=0.6,
                 stroke_opacity=0.55 if (i < 3 and j < 3) else 0.12)
            for i in range(5) for j in range(5) if j >= i
        ])
        self.play(Create(causal_lines), run_time=0.9)
        self.next_slide()

        mask_lbl = Text("causal mask: each output sees only past inputs",
                        font_size=22, color=C_YELLOW)
        mask_lbl.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(mask_lbl, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 18 — Prompt as Bias Term
# ══════════════════════════════════════════════════════════════════
class Slide18PromptBias(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("prompting as a bias term")
        self.play(FadeIn(title), run_time=0.5)

        eq_base = MathTex(
            r"o = \sigma\!\Bigl(\sum_i w_i\,a_i + b\Bigr)",
            font_size=46,
        ).shift(UP * 0.9)
        self.play(Write(eq_base), run_time=0.8)
        self.next_slide()

        bias_box = SurroundingRectangle(eq_base, buff=0.08, color=C_ORANGE)
        bias_lbl = Text("bias term", font_size=22, color=C_ORANGE).next_to(bias_box, DOWN, buff=0.2)
        self.play(Create(bias_box), FadeIn(bias_lbl), run_time=0.5)
        self.next_slide()

        arrow = Arrow(ORIGIN + DOWN * 0.5, ORIGIN + DOWN * 1.3,
                      buff=0.05, stroke_width=2, color=C_ORANGE)
        eq_prompt = MathTex(
            r"o = \sigma\!\Bigl(\sum_i w_i\,a_i + b + b_{\text{prompt}}\Bigr)",
            font_size=38,
        ).shift(DOWN * 1.0)
        prompt_lbl = Text("prompt tokens add an effective bias shift",
                          font_size=24, color=C_ORANGE).next_to(eq_prompt, DOWN, buff=0.35)

        self.play(FadeOut(bias_box), FadeOut(bias_lbl), Create(arrow), run_time=0.4)
        self.play(Write(eq_prompt), run_time=0.8)
        self.play(FadeIn(prompt_lbl), run_time=0.5)
        self.next_slide()

        change_lbl = Text("change the prompt → change the bias → change the output",
                          font_size=22, color=C_YELLOW)
        change_lbl.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(change_lbl, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 19 — Two Loops Side by Side
# ══════════════════════════════════════════════════════════════════
class Slide19TwoLoops(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("training loop  =  prompting loop")
        self.play(FadeIn(title), run_time=0.5)

        train_steps  = ["run input", "check vs expected", "update weights", "repeat"]
        prompt_steps = ["run input", "check vs expected", "update prompt",  "repeat"]

        divider = Line(UP * 2.2, DOWN * 2.8, stroke_color=C_GREY, stroke_width=1, stroke_opacity=0.35)
        self.play(Create(divider), run_time=0.3)

        train_lbl  = Text("training loop",  font_size=26, color=C_INPUT).shift(LEFT  * 3.2 + UP * 1.8)
        prompt_lbl = Text("prompting loop", font_size=26, color=C_GREEN).shift(RIGHT * 3.2 + UP * 1.8)
        self.play(FadeIn(train_lbl), FadeIn(prompt_lbl), run_time=0.5)

        for i, (ts, ps) in enumerate(zip(train_steps, prompt_steps)):
            y = 0.9 - i * 0.95
            diff = ts != ps
            tc = C_ORANGE if diff else WHITE
            pc = C_ORANGE if diff else WHITE

            tb = RoundedRectangle(corner_radius=0.1, width=3.0, height=0.62,
                                  stroke_color=C_INPUT, fill_color=DARK_BG, fill_opacity=0.85)
            tb.shift(LEFT * 3.2 + UP * y)
            tl = Text(ts, font_size=20, color=tc).move_to(tb)

            pb = RoundedRectangle(corner_radius=0.1, width=3.0, height=0.62,
                                  stroke_color=C_GREEN, fill_color=DARK_BG, fill_opacity=0.85)
            pb.shift(RIGHT * 3.2 + UP * y)
            pl = Text(ps, font_size=20, color=pc).move_to(pb)

            self.play(FadeIn(VGroup(tb, tl)), FadeIn(VGroup(pb, pl)), run_time=0.35)

            conn = DashedLine(tb.get_right(), pb.get_left(),
                              stroke_color=C_GREY, stroke_width=0.8, stroke_opacity=0.45)
            self.play(Create(conn), run_time=0.2)
            self.next_slide()

        punchline = Text("prompting is finetuning — just with natural language instead of gradients",
                         font_size=21, color=C_YELLOW)
        punchline.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(punchline, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 20 — Evaluate Your Prompts
# ══════════════════════════════════════════════════════════════════
class Slide20EvaluatePrompts(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("evaluate your prompts")
        self.play(FadeIn(title), run_time=0.5)

        buckets_info = [
            ("prompt dev set", C_INPUT),
            ("held-out eval set", C_GREEN),
            ("test set", C_ORANGE),
        ]
        buckets = VGroup()
        for i, (lbl, col) in enumerate(buckets_info):
            rect = RoundedRectangle(corner_radius=0.1, width=2.7, height=0.9,
                                    stroke_color=col, fill_color=DARK_BG, fill_opacity=0.85)
            rect.shift(LEFT * (2.7 - i * 2.7) + UP * 1.0)
            text = Text(lbl, font_size=19, color=col).move_to(rect)
            buckets.add(VGroup(rect, text))
        self.play(FadeIn(buckets), run_time=0.7)
        self.next_slide()

        warning = Text(
            "tune on your dev set.\nnever peek at eval until you're done.",
            font_size=28, color=C_RED, line_spacing=1.4,
        ).shift(DOWN * 0.5)
        self.play(FadeIn(warning, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        final = Text(
            "if you're tuning a prompt, you need a holdout —\nor you're just overfitting to your examples",
            font_size=24, color=C_YELLOW, line_spacing=1.4,
        ).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(final, shift=UP * 0.1), run_time=0.7)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════
# Slide 21 — Wrap-up
# ══════════════════════════════════════════════════════════════════
class Slide21Wrapup(Slide):
    def construct(self):
        self.next_slide()

        title = Text("that's a wrap", font_size=44, slant=ITALIC)
        title.to_edge(UP, buff=0.6)
        self.play(FadeIn(title, shift=UP * 0.1), run_time=0.8)

        underline = Line(
            title.get_left() + DOWN * 0.15, title.get_right() + DOWN * 0.15,
            stroke_color=WHITE, stroke_width=1, stroke_opacity=0.4,
        )
        self.play(Create(underline), run_time=0.4)
        self.next_slide()

        goals = [
            "neural networks are just math — we can reason about them  ✓",
            "evaluations are critical — and hard to get right  ✓",
            "prompting is pseudo-finetuning — eval your prompts  ✓",
        ]
        goal_mobs = VGroup(*[Text(g, font_size=26, color=C_GREEN) for g in goals])
        goal_mobs.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        goal_mobs.next_to(underline, DOWN, buff=0.55).to_edge(LEFT, buff=1.0)
        for m in goal_mobs:
            m.set_opacity(0)
        self.add(goal_mobs)

        for m in goal_mobs:
            self.play(m.animate.set_opacity(1.0), run_time=0.45)
            self.next_slide()

        summer = Text(
            "ML summer series — zero to your own LLM in 12 weeks",
            font_size=26, color=C_YELLOW,
        ).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(summer, shift=UP * 0.1), run_time=0.7)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
