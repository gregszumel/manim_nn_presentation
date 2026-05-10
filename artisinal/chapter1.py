from itertools import accumulate, product
from manim import (
    BLACK,
    RED,
    WHITE,
    Circle,
    Create,
    FadeOut,
    Graph,
    LaggedStart,
    MathTex,
    Scene,
    ShowPassingFlash,
    Text,
    Transform,
    Uncreate,
)


class AnimatedNeuralNet:
    def __init__(self, layers: list[int]):
        accumulated_layers = list(accumulate([0] + layers))
        neurons = [*range(sum(layers))]
        neuron_moobjects = {
            n: Circle(
                0.2,
                color=BLACK,
                fill_opacity=1,
                # fill_opacity=0.2,
                stroke_color=WHITE,
                stroke_width=0.5,
                z_index=10,
            )
            for n in neurons
        }
        print(neuron_moobjects)
        neurons_by_layer = []
        for i in range(len(accumulated_layers) - 1):
            neurons_by_layer.append(
                [*range(accumulated_layers[i], accumulated_layers[i + 1])]
            )

        edges = []
        for i in range(len(neurons_by_layer) - 1):
            layer_neurons = neurons_by_layer[i]
            next_layer_neurons = neurons_by_layer[i + 1]
            edges.extend(product(layer_neurons, next_layer_neurons))

        print(neurons)
        print(neurons_by_layer)
        print(edges)
        self.graph = Graph(
            neurons,
            edges,
            layout="partite",
            partitions=neurons_by_layer,
            vertex_mobjects=neuron_moobjects,
            layout_scale=(5, 2),
            edge_config={"stroke_width": 0.2},
        )

    def get_graph(self, layers: list[int]):
        return self.graph

    def get_edges(self, vertex: int):
        return [self.graph.edges[e] for e in self.graph.edges if vertex in e]


class Introduction(Scene):
    def construct(self) -> None:
        text = Text("What even is a neural network?")
        text2 = Text("Let's find out, and learn some manim along the way")
        self.play(Create(text))
        self.wait(2)
        self.play(Transform(text, text2))
        self.wait(2)
        self.play(Uncreate(text))
        net = AnimatedNeuralNet([3, 5, 2])
        graph = net.graph

        self.play(Create(net.graph))
        self.wait(2)
        from manim import Line

        anims = [
            ShowPassingFlash(
                Line(
                    graph.vertices[u].get_center(),
                    graph.vertices[v].get_center(),
                    stroke_color=RED,
                    stroke_width=2.5,
                ),
                time_width=0.4,
            )
            for (u, v) in graph.edges
        ]

        self.play(
            LaggedStart(
                *anims,
                lag_ratio=0.02,
                run_time=1.0,
            )
        )
        anims = [FadeOut(e) for e in net.get_edges(0)] + [FadeOut(graph.vertices[0])]
        self.play(LaggedStart(*anims, lag_ratio=0.2))
        graph.remove_vertices(0)
        self.play(
            graph.animate.change_layout(
                "partite",
                partitions=[[1, 2], [3, 4, 5, 6, 7], [8, 9]],
                layout_scale=(5, 2),
            )
        )
        self.wait(2)
