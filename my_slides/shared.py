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
                    stroke_opacity=0.2,
                ).set_z(0)
    all_mobs = VGroup(*[m for layer in neurons for m in layer], *edges.values())
    all_mobs.center()
    return neurons, edges, all_mobs


def section_title(text, font_size=36):
    t = Text(text, font_size=font_size, slant=ITALIC)
    t.to_edge(UP, buff=0.5)
    return t
