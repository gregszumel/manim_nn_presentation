from manim import *
from manim_slides import Slide

from my_slides.shared import (
    section_title,
    build_network,
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

        # Transition: strip down to a [2,1] network matching Slide03's layout
        self.play(
            FadeOut(VGroup(title, act_label, weight_label, *layer_label_mobs)),
            run_time=0.4,
        )

        keep_edge_keys = {(0, 0, 0), (0, 1, 0)}
        keep_neurons = {neurons[0][0], neurons[0][1], neurons[1][0]}
        remove_neurons = [
            n for layer in neurons for n in layer if n not in keep_neurons
        ]
        remove_edges = [e for k, e in edges.items() if k not in keep_edge_keys]

        self.play(FadeOut(VGroup(*remove_neurons, *remove_edges)), run_time=0.6)

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
