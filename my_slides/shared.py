"""
All 21 slide scenes for the neural networks talk.

Render a single scene:
    manim-slides render slides/scenes.py Slide01Goals
Present:
    manim-slides present Slide01Goals Slide02BasicNetwork ...
"""

import sys, os

from manim import *
from manim_slides import Slide
import numpy as np

# ── Palette ────────────────────────────────────────────────────────
C_INPUT = "#5B9BD5"
C_HIDDEN = "#70AD47"
C_OUTPUT = "#ED7D31"
C_EDGE = "#888888"
DARK_BG = "#1a1a2e"
C_YELLOW = "#FFD966"
C_ORANGE = "#FF8C42"
C_GREEN = "#69db7c"
C_RED = "#FF6B6B"
C_GREY = "#AAAAAA"
C_CLAIM = "#A8C4E0"


# ── Neuron ─────────────────────────────────────────────────────────


class Neuron(LabeledDot):
    """Circle neuron with an optional MathTex label centred inside."""

    def __init__(self, label: str = "", color: str = C_HIDDEN, **kwargs):
        rendered_label = MathTex(label, font_size=16, color=color)
        super().__init__(
            label=rendered_label,
            radius=0.32,
            fill_color=DARK_BG,
            fill_opacity=1,
            stroke_color=color,
            stroke_width=2.0,
            **kwargs,
        )

    @property
    def label(self):
        return self.submobjects[0]

    def set_label(self, new_text: str, color: str | None = None) -> None:
        """Instantly replace label text with an optional new color."""
        color = color or self.submobjects[0].get_color()
        new_mob = MathTex(new_text, font_size=16, color=color)
        new_mob.move_to(self.get_center()).set_z_index(2)

        self.remove(self.submobjects[0])
        self.add(new_mob)


# ── Shared helpers ─────────────────────────────────────────────────


def _layer_prefix(l: int, n_layers: int) -> str:
    if l == 0:
        return "i"
    if l == n_layers - 1:
        return "o"
    return "h"


def build_network(layer_sizes, h_spacing=2.2, v_spacing=1.0, colors=None, labels=True):
    if colors is None:
        colors = [C_INPUT] + [C_HIDDEN] * (len(layer_sizes) - 2) + [C_OUTPUT]
    n_layers = len(layer_sizes)
    neurons: list[list[Neuron]] = []
    for l, (n, col) in enumerate(zip(layer_sizes, colors)):
        prefix = _layer_prefix(l, n_layers)
        layer = []
        total_h = (n - 1) * v_spacing
        for i in range(n):
            lbl = f"{prefix}_{{{i}}}" if labels else ""
            neuron = Neuron(label=lbl, color=col)
            neuron.move_to(np.array([l * h_spacing, total_h / 2 - i * v_spacing, 0]))
            neuron.set_z_index(1)
            layer.append(neuron)
        neurons.append(layer)
    edges = {}
    for l in range(len(layer_sizes) - 1):
        for i, src in enumerate(neurons[l]):
            for j, dst in enumerate(neurons[l + 1]):
                edges[(l, i, j)] = Line(
                    src.get_center(),
                    dst.get_center(),
                    stroke_color=C_ORANGE,
                    stroke_width=0.8,
                    stroke_opacity=0.5,
                ).set_z(0)
    all_mobs = VGroup(*[m for layer in neurons for m in layer], *edges.values())
    all_mobs.center()
    return neurons, edges, all_mobs


def add_layer(
    neurons,
    edges,
    net_group,
    n=1,
    color=C_OUTPUT,
    h_spacing=2.2,
    v_spacing=1.0,
    labels=True,
):
    """
    Append a layer of *n* neurons at the end of an existing network.

    The new neurons and their incoming edges are appended to the
    *neurons* list and *edges* dict in place.  The caller should
    add the returned mobjects to *net_group* **after** animating
    them in (to control when they appear on screen).

    Parameters
    ----------
    neurons : list[list[Neuron]]
    edges : dict[(int, int, int), Line]
    net_group : VGroup  (not mutated by this function)
    n : int  number of neurons in the new layer
    color : str
    h_spacing : float  horizontal distance from the previous layer
    v_spacing : float  vertical spacing between neurons in this layer
    labels : bool

    Returns
    -------
    (new_neurons, new_edge_mobs)
        new_neurons : list[Neuron]
        new_edge_mobs : list[Line]
    """
    last_layer = neurons[-1]
    l = len(neurons)  # index this new layer will have

    # Position the new layer *h_spacing* to the right of the last layer,
    # respecting any previous shifts / centering applied to the network.
    last_x = np.mean([n.get_center()[0] for n in last_layer])
    new_x = last_x + h_spacing

    total_h = (n - 1) * v_spacing
    new_neurons = []
    for i in range(n):
        prefix = _layer_prefix(l, l + 1)  # new total = l + 1
        lbl = f"{prefix}_{{{i}}}" if labels else ""
        neuron = Neuron(label=lbl, color=color)
        neuron.move_to(np.array([new_x, total_h / 2 - i * v_spacing, 0]))
        neuron.set_z_index(1)
        new_neurons.append(neuron)
        net_group.add(neuron)

    # Edges from the previous last layer → new layer
    src_idx = l - 1
    new_edge_mobs = []
    for i, src in enumerate(last_layer):
        for j, dst in enumerate(new_neurons):
            e = Line(
                src.get_center(),
                dst.get_center(),
                stroke_color=C_ORANGE,
                stroke_width=0.8,
                stroke_opacity=0.5,
            ).set_z(0)
            edges[(src_idx, i, j)] = e
            new_edge_mobs.append(e)
            net_group.add(e)

    neurons.append(new_neurons)
    return new_neurons, new_edge_mobs


def section_title(text, font_size=36):
    t = Text(text, font_size=font_size, slant=ITALIC)
    t.to_edge(UP, buff=0.5)
    return t
