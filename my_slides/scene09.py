from manim import *
from manim_slides import Slide
from my_slides.shared import *
import numpy as np


# ── Tiny 1→N_HIDDEN→1 network used for curve fitting ──────────────
N_HIDDEN = 4

# Fixed input→hidden weights: diverse slopes so the basis covers the domain
_W1 = np.array([2.0,  1.0, -1.0, -2.0])
_B1 = np.array([0.0, -0.4,  0.4,  0.0])

SWEEP_START = -1.5
SWEEP_END   =  1.5


def _relu(x):
    return np.maximum(0.0, x)


def _H(xs):
    return np.column_stack([_relu(_W1[j] * xs + _B1[j]) for j in range(N_HIDDEN)])


def _fit(xs, ys):
    H_aug = np.column_stack([_H(xs), np.ones(len(xs))])
    w, _, _, _ = np.linalg.lstsq(H_aug, ys, rcond=None)
    return w[:N_HIDDEN], float(w[N_HIDDEN])


def _predict(x_scalar, W2, b2):
    h = _relu(_W1 * x_scalar + _B1)
    return float(np.dot(h, W2) + b2)


def _make_node_labels(x_tracker, neurons, W2, b2):
    """
    Build always_redraw labels for each neuron showing live forward-pass values.
    Input node: current x. Hidden nodes: ReLU activation (green if active, grey if zero).
    Output node: NN prediction.
    """
    def _input_lbl():
        return (
            Text(f"{x_tracker.get_value():.2f}", font_size=11, color=C_INPUT)
            .move_to(neurons[0][0].get_center())
            .set_z_index(10)
        )

    def _make_h_lbl(j):
        def _h_lbl():
            v = float(_relu(_W1[j] * x_tracker.get_value() + _B1[j]))
            return (
                Text(f"{v:.2f}", font_size=10, color=C_HIDDEN if v > 1e-6 else C_GREY)
                .move_to(neurons[1][j].get_center())
                .set_z_index(10)
            )
        return always_redraw(_h_lbl)

    def _output_lbl():
        return (
            Text(f"{_predict(x_tracker.get_value(), W2, b2):.2f}", font_size=11, color=C_YELLOW)
            .move_to(neurons[2][0].get_center())
            .set_z_index(10)
        )

    return [
        always_redraw(_input_lbl),
        *[_make_h_lbl(j) for j in range(N_HIDDEN)],
        always_redraw(_output_lbl),
    ]


# ══════════════════════════════════════════════════════════════════
# Slide 9 — Universal Function Approximators
# ══════════════════════════════════════════════════════════════════
class Slide09UniversalApprox(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("universal function approximators")
        self.play(FadeIn(title), run_time=0.5)

        # Match scene13 exactly so the random subplot is visually consistent
        rng = np.random.default_rng(42)
        rand_xs = np.linspace(-1.8, 1.8, 6)
        rand_ys = rng.uniform(-1.4, 1.4, 6)
        rand_poly = np.poly1d(np.polyfit(rand_xs, rand_ys, deg=5))

        specs = [
            ("linear",      lambda x: 0.6 * x,               C_INPUT,  False),
            ("quadratic",   lambda x: x**2 - 1.0,             C_GREEN,  False),
            ("exponential", lambda x: np.exp(0.6 * x) - 1.2, C_ORANGE, False),
            ("random",      None,                              C_RED,    True),
        ]

        dense_xs = np.linspace(-1.85, 1.85, 300)

        # static_mobs: FadeOut-able between functions
        # node_lbls:   always_redraw mobs, removed with self.remove()
        static_mobs = VGroup()
        node_lbls = []

        for k, (name, fn, color, is_rand) in enumerate(specs):

            # ── Fit ──────────────────────────────────────────────────
            if not is_rand:
                W2, b2 = _fit(dense_xs, fn(dense_xs))
                nn_fn   = lambda x, W=W2, b=b2: _predict(x, W, b)
                true_fn = fn
                plot_range = [-1.85, 1.85]
            else:
                W2, b2  = _fit(rand_xs, rand_ys)
                # Use the polynomial so the curve matches scene13's "NN fits perfectly" reveal
                nn_fn   = lambda x: float(rand_poly(x))
                true_fn = lambda x: float(rand_poly(x))
                plot_range = [-1.75, 1.75]

            # ── Transition ───────────────────────────────────────────
            if k > 0:
                self.next_slide()
                # node_lbls from previous function were removed at end of its sweep;
                # only static geometry remains to fade out.
                self.play(FadeOut(static_mobs), run_time=0.35)

            static_mobs = VGroup()

            # ── Axes + true function (left side) ─────────────────────
            ax = Axes(
                x_range=[-2, 2, 1],
                y_range=[-2.5, 2.5, 1],
                x_length=5.0,
                y_length=4.5,
                axis_config={"stroke_width": 1.2, "stroke_color": C_GREY},
                tips=False,
            ).shift(LEFT * 3.0 + DOWN * 0.2)
            fn_lbl = Text(name, font_size=26, color=color).next_to(ax, UP, buff=0.1)

            if not is_rand:
                true_mob = ax.plot(fn, x_range=[-1.9, 1.9], color=color, stroke_width=2.5)
                self.play(Create(ax), FadeIn(fn_lbl), run_time=0.45)
                self.play(Create(true_mob), run_time=0.5)
            else:
                true_mob = VGroup(*[
                    Dot(ax.c2p(x, y), radius=0.1, color=C_RED, fill_opacity=0.9)
                    for x, y in zip(rand_xs, rand_ys)
                ])
                self.play(Create(ax), FadeIn(fn_lbl), run_time=0.45)
                self.play(
                    LaggedStart(*[FadeIn(d) for d in true_mob], lag_ratio=0.15),
                    run_time=0.5,
                )

            static_mobs.add(ax, fn_lbl, true_mob)

            # ── NN diagram + live forward-pass values (right side) ────
            self.next_slide()

            # Tracker starts at sweep start so node labels are "live" immediately
            x_tracker = ValueTracker(SWEEP_START)

            neurons, edges, net_mob = build_network(
                [1, N_HIDDEN, 1],
                h_spacing=1.7,
                v_spacing=0.78,
                labels=False,  # dynamic labels replace static ones
            )
            net_mob.shift(RIGHT * 3.8 + DOWN * 0.1)

            for e in edges.values():
                e.set_stroke(opacity=0.55, width=1.1)

            # always_redraw labels — show live computation at current x
            node_lbls = _make_node_labels(x_tracker, neurons, W2, b2)

            # Input→hidden edge labels (fixed _W1, grey)
            in_w_labels = []
            for j in range(N_HIDDEN):
                e = edges[(0, 0, j)]
                mid = (e.get_start() + e.get_end()) * 0.5
                lbl = Text(f"{_W1[j]:+.1f}", font_size=11, color=C_GREY)
                lbl.move_to(mid + UP * 0.20)
                in_w_labels.append(lbl)

            # Hidden→output edge labels (fitted W2, yellow)
            out_w_labels = []
            for j in range(N_HIDDEN):
                e = edges[(1, j, 0)]
                mid = (e.get_start() + e.get_end()) * 0.5
                lbl = Text(f"{W2[j]:+.2f}", font_size=12, color=C_YELLOW)
                lbl.move_to(mid + UP * 0.20)
                out_w_labels.append(lbl)

            flat_neurons = [n for layer in neurons for n in layer]

            # Neurons appear first, then labels overlay on top
            self.play(
                LaggedStart(*[FadeIn(n) for n in flat_neurons], lag_ratio=0.12),
                run_time=0.6,
            )
            self.add(*node_lbls)   # instant — appear on top of neuron fill
            self.play(
                LaggedStart(*[Create(e) for e in edges.values()], lag_ratio=0.05),
                run_time=0.6,
            )
            self.play(
                LaggedStart(*[FadeIn(l) for l in in_w_labels + out_w_labels], lag_ratio=0.07),
                run_time=0.5,
            )

            # Draw NN approximation curve on the axes
            nn_curve = DashedVMobject(
                ax.plot(nn_fn, x_range=plot_range, color=WHITE, stroke_width=2.0),
                num_dashes=40,
                dashed_ratio=0.55,
            )
            self.play(Create(nn_curve), run_time=0.7)

            static_mobs.add(
                VGroup(*flat_neurons, *list(edges.values()), *in_w_labels, *out_w_labels),
                nn_curve,
            )

            # ── Sweep: x moves left→right, neuron values update live ──
            self.next_slide()

            x_line = always_redraw(
                lambda: DashedLine(
                    ax.c2p(x_tracker.get_value(), -2.4),
                    ax.c2p(x_tracker.get_value(),  2.4),
                    color=C_GREY, stroke_width=1.0, dash_length=0.1,
                ).set_z_index(1)
            )
            true_dot = always_redraw(
                lambda: Dot(
                    ax.c2p(x_tracker.get_value(), true_fn(x_tracker.get_value())),
                    color=color, radius=0.13, fill_opacity=1.0,
                ).set_z_index(6)
            )
            nn_dot = always_redraw(
                lambda: Dot(
                    ax.c2p(x_tracker.get_value(), nn_fn(x_tracker.get_value())),
                    color=WHITE, radius=0.10, fill_opacity=0.9,
                ).set_z_index(6)
            )

            self.add(x_line, true_dot, nn_dot)
            self.play(
                x_tracker.animate.set_value(SWEEP_END),
                run_time=3.5,
                rate_func=linear,
            )

            # Clean up all dynamic mobs — static geometry stays for FadeOut next round
            self.remove(x_line, true_dot, nn_dot, *node_lbls)

        # ── Punchline ─────────────────────────────────────────────────
        self.next_slide()
        self.remove(*node_lbls)   # last function's labels (already removed, harmless)
        self.play(FadeOut(static_mobs), run_time=0.4)

        punchline = Text(
            "NNs can approximate any function", font_size=32, color=C_YELLOW
        )
        punchline.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(punchline, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
