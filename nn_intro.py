"""
Neural Network Introduction Animation
Standalone Manim scene — no external project dependencies.

Render:
    manim -pql nn_intro.py NeuralNetworkIntroScene
    manim -pqh nn_intro.py NeuralNetworkIntroScene
"""

from manim import *
import numpy as np

# ── Color palette ──────────────────────────────────────────────────
C_INPUT = "#5B9BD5"  # blue   – input neurons
C_HIDDEN = "#70AD47"  # green  – hidden neurons
C_OUTPUT = "#ED7D31"  # orange – output neurons
C_EDGE = "#888888"  # grey   – resting edges
DARK_BG = "#1a1a2e"  # dark   – neuron resting fill


# ── Network builder ────────────────────────────────────────────────


def build_network(
    layer_sizes: list[int],
    h_spacing: float = 2.5,
    v_spacing: float = 1.0,
    colors: list[str] | None = None,
) -> tuple[list[list[Circle]], dict[tuple, Line], VGroup]:
    """
    Returns:
        neurons  – neurons[layer][index]
        edges    – edges[(layer, src_i, dst_j)]
        vgroup   – all Mobjects together
    """
    if colors is None:
        colors = [C_INPUT] + [C_HIDDEN] * (len(layer_sizes) - 2) + [C_OUTPUT]

    neurons: list[list[Circle]] = []
    for l, (n, col) in enumerate(zip(layer_sizes, colors)):
        layer: list[Circle] = []
        total_h = (n - 1) * v_spacing
        for i in range(n):
            circle = Vertex(
                radius=0.32,
                stroke_color=col,
                stroke_width=2.0,
                fill_color=DARK_BG,
                fill_opacity=0.9,
            )
            circle.move_to(np.array([l * h_spacing, total_h / 2 - i * v_spacing, 0]))
            layer.append(circle)
        neurons.append(layer)

    edges: dict[tuple, Line] = {}
    for l in range(len(layer_sizes) - 1):
        for i, src in enumerate(neurons[l]):
            for j, dst in enumerate(neurons[l + 1]):
                edges[(l, i, j)] = Line(
                    src.get_center(),
                    dst.get_center(),
                    stroke_color=C_EDGE,
                    stroke_width=0.8,
                    stroke_opacity=0.35,
                )

    vgroup = VGroup(*edges.values(), *[n for layer in neurons for n in layer])
    return neurons, edges, vgroup


def _flow_flashes(
    src_layer: list[Circle],
    dst_layer: list[Circle],
    color: str,
    time_width: float = 0.4,
) -> list[ShowPassingFlash]:
    """ShowPassingFlash animations for one layer-to-layer flow (left → right)."""
    anims = []
    for src in src_layer:
        for dst in dst_layer:
            line = Line(
                src.get_center(),
                dst.get_center(),
                stroke_color=color,
                stroke_width=2.5,
                stroke_opacity=1.0,
            )
            anims.append(ShowPassingFlash(line, time_width=time_width))
    return anims


# ── Main scene ─────────────────────────────────────────────────────


class NeuralNetworkIntroScene(Scene):
    """
    Intro to neural networks:
      1. Build the network
      2. Highlight inputs → animate flow to hidden layer → highlight hidden
      3. Animate flow from hidden → output → highlight outputs
      4. Repeat the full forward sweep one more time
    """

    LAYER_SIZES = [3, 4, 2]

    def construct(self):
        neurons, edges, net = build_network(self.LAYER_SIZES)
        net.center()

        title = Text("Neural Network", font_size=44)
        title.to_edge(UP, buff=0.4)

        layer_names = ["Inputs", "Hidden Layer", "Outputs"]
        layer_colors = [C_INPUT, C_HIDDEN, C_OUTPUT]
        layer_labels = []
        for i, (name, col) in enumerate(zip(layer_names, layer_colors)):
            lbl = Text(name, font_size=22, color=col)
            lbl.move_to(
                np.array(
                    [
                        neurons[i][0].get_x(),
                        neurons[i][-1].get_y() - 0.85,
                        0,
                    ]
                )
            )
            layer_labels.append(lbl)

        # ── 1. Draw the network ────────────────────────────────────
        self.play(Write(title), run_time=0.8)
        self.play(
            LaggedStart(
                *[Create(e) for e in edges.values()], lag_ratio=0.02, run_time=1.5
            ),
        )
        self.play(
            LaggedStart(
                *[GrowFromCenter(n) for layer in neurons for n in layer],
                lag_ratio=0.08,
                run_time=1.2,
            ),
        )
        self.play(
            LaggedStart(
                *[FadeIn(lbl) for lbl in layer_labels], lag_ratio=0.3, run_time=0.8
            ),
        )
        self.wait(0.5)

        # ── 2. Highlight inputs ────────────────────────────────────
        desc = Text("Inputs: raw data enters here", font_size=24, color=C_INPUT)
        desc.to_edge(DOWN, buff=0.5)

        self.play(
            *[n.animate.set_fill(color=C_INPUT, opacity=0.75) for n in neurons[0]],
            Write(desc),
            run_time=0.8,
        )
        self.wait(0.7)

        # ── 3. Flow: inputs → hidden ───────────────────────────────
        self.play(FadeOut(desc), run_time=0.25)
        self.play(
            LaggedStart(
                *_flow_flashes(neurons[0], neurons[1], C_INPUT),
                lag_ratio=0.00,
                run_time=1.0,
            ),
        )

        # ── 4. Highlight hidden ────────────────────────────────────
        desc = Text(
            "Hidden Layer: learns internal features", font_size=24, color=C_HIDDEN
        )
        desc.to_edge(DOWN, buff=0.5)

        self.play(
            *[n.animate.set_fill(color=DARK_BG, opacity=0.9) for n in neurons[0]],
            *[n.animate.set_fill(color=C_HIDDEN, opacity=0.75) for n in neurons[1]],
            Write(desc),
            run_time=0.8,
        )
        self.wait(0.7)

        # ── 5. Flow: hidden → output ───────────────────────────────
        self.play(FadeOut(desc), run_time=0.25)
        self.play(
            LaggedStart(
                *_flow_flashes(neurons[1], neurons[2], C_HIDDEN),
                lag_ratio=0.00,
                run_time=1.0,
            ),
        )

        # ── 6. Highlight outputs ───────────────────────────────────
        desc = Text("Outputs: the network's predictions", font_size=24, color=C_OUTPUT)
        desc.to_edge(DOWN, buff=0.5)

        self.play(
            *[n.animate.set_fill(color=DARK_BG, opacity=0.9) for n in neurons[1]],
            *[n.animate.set_fill(color=C_OUTPUT, opacity=0.75) for n in neurons[2]],
            Write(desc),
            run_time=0.8,
        )
        self.wait(0.8)
        self.play(FadeOut(desc), run_time=0.25)

        # ── 7. Reset, then replay full forward sweep ───────────────
        self.play(
            *[
                n.animate.set_fill(color=DARK_BG, opacity=0.9)
                for layer in neurons
                for n in layer
            ],
            run_time=0.5,
        )
        self.wait(0.3)

        sweep_label = Text("Information flows forward →", font_size=26, color=WHITE)
        sweep_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(sweep_label), run_time=0.4)

        # inputs
        self.play(
            *[n.animate.set_fill(color=C_INPUT, opacity=0.75) for n in neurons[0]],
            run_time=0.5,
        )

        # input → hidden
        self.play(
            LaggedStart(
                *_flow_flashes(neurons[0], neurons[1], C_INPUT),
                lag_ratio=0.00,
                run_time=0.7,
            ),
        )
        self.play(
            *[n.animate.set_fill(color=DARK_BG, opacity=0.9) for n in neurons[0]],
            *[n.animate.set_fill(color=C_HIDDEN, opacity=0.75) for n in neurons[1]],
            run_time=0.5,
        )

        # hidden → output
        self.play(
            LaggedStart(
                *_flow_flashes(neurons[1], neurons[2], C_HIDDEN),
                lag_ratio=0.00,
                run_time=0.7,
            ),
        )
        self.play(
            *[n.animate.set_fill(color=DARK_BG, opacity=0.9) for n in neurons[1]],
            *[n.animate.set_fill(color=C_OUTPUT, opacity=0.75) for n in neurons[2]],
            run_time=0.5,
        )

        self.wait(1.0)

        self.play(FadeOut(VGroup(sweep_label, title, *layer_labels, net)))
