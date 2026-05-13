from manim import *
from manim_slides import Slide
from my_slides.shared import *
import numpy as np

# ── Training architecture (shared between scene11 & scene12) ──────
# 1 → N_HIDDEN → 1.  Fixed W1/B1 = ReLU basis.  Only W2/b2 learn.
# Break points placed AWAY from origin so b2_optimal stays small
# (validated in script/validate_gd.py — converges to 0 cleanly).
N_HIDDEN = 6
W1 = np.array([1.0, 1.0, 1.0, -1.0, -1.0, -1.0])
B1 = np.array([-0.5, -1.0, -1.5, -0.5, -1.0, -1.5])
# break points: +0.5, +1.0, +1.5, -0.5, -1.0, -1.5

LR = 0.15


def true_fn(x):
    return 0.6 * float(x) ** 2 - 1.0


def relu(x):
    return np.maximum(0.0, x)


def forward(x, W2, b2):
    h = relu(W1 * float(x) + B1)
    return float(np.dot(W2, h) + b2)


def grad_step(x, y_true, W2, b2, lr=LR):
    h = relu(W1 * float(x) + B1)
    y_pred = float(np.dot(W2, h) + b2)
    error = y_pred - y_true
    return W2 - lr * 2.0 * error * h, b2 - lr * 2.0 * error


# Random init — same seed for scene11 and scene12 so they start aligned
_rng = np.random.default_rng(7)
W2_INIT = _rng.normal(0, 0.4, N_HIDDEN)
B2_INIT = float(_rng.normal(0, 0.3))


# ── Helpers for building the NN diagram with live weights ─────────
def build_training_view(scene, ax_shift_left=3.2, net_shift_right=3.2):
    """
    Build the [1, N_HIDDEN, 1] diagram with live-updating W2 edge labels
    and a live b2 label.  Returns (trackers, neurons, edges, net_mob,
    w2_lbls, b2_lbl, current_W2, current_b2, current_forward).
    """
    W2_trackers = [ValueTracker(float(W2_INIT[j])) for j in range(N_HIDDEN)]
    b2_tracker = ValueTracker(B2_INIT)
    # x_tracker = current input being shown in the live neuron values
    x_tracker = ValueTracker(0.0)

    def current_W2():
        return np.array([t.get_value() for t in W2_trackers])

    def current_b2():
        return b2_tracker.get_value()

    def current_forward(x):
        return forward(x, current_W2(), current_b2())

    neurons, edges, net_mob = build_network(
        [1, N_HIDDEN, 1],
        h_spacing=1.8,
        v_spacing=0.55,
        labels=False,
    )
    net_mob.shift(RIGHT * net_shift_right + DOWN * 0.3)

    for e in edges.values():
        e.set_stroke(opacity=0.45, width=1.0)

    # Helper: pick an "outward" perpendicular offset for an edge label.
    # `bundle_y` is the y of the neuron the edges converge to / diverge from.
    def _outward_offset(midpoint_y, bundle_y, magnitude):
        if midpoint_y > bundle_y + 0.02:
            return UP * magnitude
        if midpoint_y < bundle_y - 0.02:
            return DOWN * magnitude
        return UP * magnitude  # center → arbitrary, default up

    # W1 edge labels (fixed, grey) — input → hidden weights
    # Anchored 70% along the edge so they cluster near the (spread-out) hidden
    # neurons rather than the single input neuron.  Offset perpendicular to
    # the input neuron's y-line so top-half labels go UP, bottom-half go DOWN.
    input_y = neurons[0][0].get_center()[1]
    w1_lbls = []
    for j in range(N_HIDDEN):
        e = edges[(0, 0, j)]
        anchor = 0.3 * e.get_start() + 0.7 * e.get_end()
        offset = _outward_offset(anchor[1], input_y, 0.10)
        lbl = Text(f"{W1[j]:+.0f}", font_size=10, color=C_GREY)
        lbl.move_to(anchor + offset)
        lbl.set_z_index(11)
        w1_lbls.append(lbl)

    # W2 edge labels (animated, yellow) — hidden → output weights
    # DecimalNumber + updater (NOT always_redraw with Text — that hits a
    # manim SVG-cache race condition and crashes mid-render).
    output_y = neurons[2][0].get_center()[1]
    w2_lbls = []
    for j in range(N_HIDDEN):
        e = edges[(1, j, 0)]
        mid = (e.get_start() + e.get_end()) * 0.5
        offset = _outward_offset(mid[1], output_y, 0.13)
        lbl = DecimalNumber(
            float(W2_trackers[j].get_value()),
            num_decimal_places=2,
            include_sign=True,
            font_size=22,
            color=C_YELLOW,
        )
        lbl.move_to(mid + offset)
        lbl.set_z_index(11)
        lbl.add_updater(lambda d, j=j: d.set_value(float(W2_trackers[j].get_value())))
        w2_lbls.append(lbl)

    # b2 label: static "b=" prefix + live DecimalNumber
    out_neuron = neurons[2][0]
    b2_prefix = Text("b=", font_size=14, color=C_YELLOW)
    b2_value = DecimalNumber(
        float(b2_tracker.get_value()),
        num_decimal_places=2,
        include_sign=True,
        font_size=22,
        color=C_YELLOW,
    )
    b2_lbl = VGroup(b2_prefix, b2_value).arrange(RIGHT, buff=0.05)
    b2_lbl.next_to(out_neuron, RIGHT, buff=0.15).set_z_index(11)
    b2_value.add_updater(lambda d: d.set_value(float(b2_tracker.get_value())))

    # ── Live neuron-value labels (input, hidden, output) ──────────
    # All DecimalNumbers — positioned once at the neuron center, updated
    # in place via set_value/set_color so the SVG cache stays calm.
    # Re-center inside the updaters because DecimalNumber.set_value
    # uses edge_to_fix=LEFT by default, which can drift the position.
    input_center = neurons[0][0].get_center()
    input_lbl = DecimalNumber(
        0.0,
        num_decimal_places=2,
        include_sign=True,
        font_size=28,
        color=C_INPUT,
    )
    input_lbl.move_to(input_center).set_z_index(12)

    def _update_input(d):
        d.set_value(float(x_tracker.get_value()))
        d.move_to(input_center)
        d.set_z_index(12)

    input_lbl.add_updater(_update_input)

    hidden_lbls = []
    for j in range(N_HIDDEN):
        v_init = float(np.maximum(0.0, W1[j] * x_tracker.get_value() + B1[j]))
        h_center = neurons[1][j].get_center()
        lbl = DecimalNumber(
            v_init,
            num_decimal_places=2,
            font_size=22,
            color=C_HIDDEN if v_init > 1e-6 else C_GREY,
        )
        lbl.move_to(h_center).set_z_index(12)

        def _update_hidden(d, j=j, c=h_center):
            v = float(np.maximum(0.0, W1[j] * x_tracker.get_value() + B1[j]))
            d.set_value(v)
            d.move_to(c)
            d.set_color(C_HIDDEN if v > 1e-6 else C_GREY)
            d.set_z_index(12)

        lbl.add_updater(_update_hidden)
        hidden_lbls.append(lbl)

    output_center = neurons[2][0].get_center()
    output_lbl = DecimalNumber(
        current_forward(x_tracker.get_value()),
        num_decimal_places=2,
        include_sign=True,
        font_size=28,
        color=C_YELLOW,
    )
    output_lbl.move_to(output_center).set_z_index(12)

    def _update_output(d):
        h = np.maximum(0.0, W1 * x_tracker.get_value() + B1)
        v = float(np.dot(current_W2(), h) + current_b2())
        d.set_value(v)
        d.move_to(output_center)
        d.set_z_index(12)

    output_lbl.add_updater(_update_output)

    node_lbls = [input_lbl, *hidden_lbls, output_lbl]
    node_lbls = [lbl.set_z_index(10) for lbl in node_lbls]

    return {
        "trackers": (W2_trackers, b2_tracker),
        "x_tracker": x_tracker,
        "neurons": neurons,
        "edges": edges,
        "net_mob": net_mob,
        "w1_lbls": w1_lbls,
        "w2_lbls": w2_lbls,
        "b2_lbl": b2_lbl,
        "node_lbls": node_lbls,
        "current_W2": current_W2,
        "current_b2": current_b2,
        "current_forward": current_forward,
    }


def make_err_visuals(view, ax, x_t):
    """
    Build (err_line, err_lbl, err_arrow) for one training point.
    Label is anchored on the OPPOSITE side of the axes from x_t
    so it never overlaps with the curves at that x.  Arrow points
    from the label to the midpoint of the error bar.

    All three are always_redraw — they follow the live curve as it
    morphs during a gradient step.
    """
    y_t = true_fn(x_t)
    # Label position: top of the axes, on the side opposite x_t
    lbl_x = 1.1 if x_t < 0 else -1.1
    lbl_anchor = ax.c2p(lbl_x, 1.25)
    arrow_start_anchor = ax.c2p(lbl_x, 1.0)

    err_line = always_redraw(
        lambda: Line(
            ax.c2p(x_t, view["current_forward"](x_t)),
            ax.c2p(x_t, y_t),
            color=C_RED,
            stroke_width=4,
        )
    )

    # Error label: static "error = " prefix + live DecimalNumber.
    # (Avoids the always_redraw-with-Text SVG-cache race condition.)
    err_prefix = Text("error =", font_size=18, color=C_RED)
    err_value = DecimalNumber(
        view["current_forward"](x_t) - y_t,
        num_decimal_places=2,
        include_sign=True,
        font_size=30,
        color=C_RED,
    )
    err_lbl = VGroup(err_prefix, err_value).arrange(RIGHT, buff=0.10)
    err_lbl.move_to(lbl_anchor)
    err_value.add_updater(lambda d: d.set_value(view["current_forward"](x_t) - y_t))

    err_arrow = always_redraw(
        lambda: Arrow(
            start=arrow_start_anchor,
            end=ax.c2p(x_t, (view["current_forward"](x_t) + y_t) / 2),
            color=C_RED,
            stroke_width=2.5,
            buff=0.15,
            max_tip_length_to_length_ratio=0.12,
        )
    )
    return err_line, err_lbl, err_arrow


def animate_step(scene, view, ax, x_train, run_time=0.3, flash_error=False):
    """
    Run one SGD step.

    1. Move x_tracker to x_train (input/hidden/output neuron labels update).
    2. (Optional) Flash a red error bar between curves at x_train.
    3. Animate W2/b2 trackers to the post-gradient-step values
       (curve, error bar, output neuron label all morph in lockstep).
    """
    W2_trackers, b2_tracker = view["trackers"]
    x_tracker = view["x_tracker"]
    W2_cur = view["current_W2"]()
    b2_cur = view["current_b2"]()
    W2_new, b2_new = grad_step(x_train, true_fn(x_train), W2_cur, b2_cur)

    # 1. Move x_tracker so neuron labels reflect the new training point.
    if abs(x_tracker.get_value() - x_train) > 1e-6:
        scene.play(
            x_tracker.animate.set_value(x_train),
            run_time=max(run_time * 0.4, 0.08),
        )

    if flash_error:
        y_p = view["current_forward"](x_train)
        y_t = true_fn(x_train)
        err = Line(
            ax.c2p(x_train, y_p),
            ax.c2p(x_train, y_t),
            color=C_RED,
            stroke_width=3,
        )
        scene.play(Create(err), run_time=0.08)
        scene.play(
            *[
                W2_trackers[j].animate.set_value(float(W2_new[j]))
                for j in range(N_HIDDEN)
            ],
            b2_tracker.animate.set_value(b2_new),
            FadeOut(err),
            run_time=run_time,
        )
    else:
        scene.play(
            *[
                W2_trackers[j].animate.set_value(float(W2_new[j]))
                for j in range(N_HIDDEN)
            ],
            b2_tracker.animate.set_value(b2_new),
            run_time=run_time,
        )


# ══════════════════════════════════════════════════════════════════
# Slide 11 — How Do We Train?  (concept + first gradient step)
# ══════════════════════════════════════════════════════════════════
class Slide11Training(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("how do we train?")
        self.play(FadeIn(title), run_time=0.5)

        # ── Axes (left) ────────────────────────────────────────────
        ax = Axes(
            x_range=[-2.0, 2.0, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=5.0,
            y_length=3.8,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(LEFT * 3.2 + DOWN * 0.3)
        self.play(Create(ax), run_time=0.5)

        # ── Target ─────────────────────────────────────────────────
        target = ax.plot(true_fn, x_range=[-1.9, 1.9], color=C_GREEN, stroke_width=3)
        target_lbl = Text("target (quadratic)", font_size=16, color=C_GREEN)
        target_lbl.next_to(ax, UP, buff=0.1).shift(LEFT * 0.5)
        self.play(Create(target), FadeIn(target_lbl), run_time=0.7)
        self.next_slide()

        # ── NN diagram + live weights ──────────────────────────────
        view = build_training_view(self)
        W2_trackers, b2_tracker = view["trackers"]
        flat_neurons = [n for layer in view["neurons"] for n in layer]

        self.play(
            LaggedStart(*[FadeIn(n) for n in flat_neurons], lag_ratio=0.07),
            run_time=0.5,
        )
        self.play(
            LaggedStart(*[Create(e) for e in view["edges"].values()], lag_ratio=0.03),
            run_time=0.5,
        )
        self.add(*view["w1_lbls"], *view["w2_lbls"], view["b2_lbl"])
        # Reveal neuron-value labels with a brief FadeIn.
        self.play(
            *[FadeIn(lbl) for lbl in view["node_lbls"]],
            run_time=0.4,
        )
        self.next_slide()

        # ── Initial NN curve (random init, far from target) ────────
        nn_curve = always_redraw(
            lambda: ax.plot(
                view["current_forward"],
                x_range=[-1.9, 1.9],
                color=C_YELLOW,
                stroke_width=2.5,
            )
        )
        nn_lbl = Text("NN (random init)", font_size=16, color=C_YELLOW)
        nn_lbl.next_to(target_lbl, DOWN, buff=0.1, aligned_edge=LEFT)
        self.add(nn_curve)
        self.play(FadeIn(nn_lbl), run_time=0.4)
        self.next_slide()

        # ── Training loop callout ──────────────────────────────────
        steps_text = [
            "1. pick an x",
            "2. compute the error",
            "3. nudge weights",
            "4. repeat",
        ]
        loop = VGroup(*[Text(s, font_size=18, color=C_GREY) for s in steps_text])
        loop.arrange(DOWN, buff=0.10, aligned_edge=LEFT)
        loop.to_edge(DOWN, buff=0.3).shift(LEFT * 4.5)
        self.play(
            LaggedStart(*[FadeIn(s, shift=RIGHT * 0.1) for s in loop], lag_ratio=0.2),
            run_time=1.0,
        )
        self.next_slide()

        # ══════════════════════════════════════════════════════════
        # ONE detailed gradient step
        # ══════════════════════════════════════════════════════════
        x_train = -1.4
        y_t = true_fn(x_train)
        y_p = view["current_forward"](x_train)

        # 1. pick an x — also animate x_tracker so input/hidden/output
        # neuron labels reflect the chosen training point.
        self.play(loop[0].animate.set_color(C_ORANGE), run_time=0.25)
        v_line = DashedLine(
            ax.c2p(x_train, -1.4),
            ax.c2p(x_train, 1.4),
            color=C_GREY,
            stroke_width=1.0,
            dash_length=0.1,
        )
        dot_t = Dot(ax.c2p(x_train, y_t), color=C_GREEN, radius=0.10)
        dot_p = always_redraw(
            lambda: Dot(
                ax.c2p(x_train, view["current_forward"](x_train)),
                color=C_YELLOW,
                radius=0.10,
            )
        )
        self.play(
            Create(v_line),
            FadeIn(dot_t),
            view["x_tracker"].animate.set_value(x_train),
            run_time=0.6,
        )
        self.add(dot_p)
        self.next_slide()

        # 2. compute error
        self.play(
            loop[0].animate.set_color(C_GREY),
            loop[1].animate.set_color(C_ORANGE),
            run_time=0.25,
        )
        err_line, err_lbl, err_arrow = make_err_visuals(view, ax, x_train)
        self.add(err_line, err_lbl, err_arrow)
        self.play(FadeIn(err_line), FadeIn(err_lbl), FadeIn(err_arrow), run_time=0.4)
        self.next_slide()

        # 3. nudge weights → curve updates, error shrinks, all live
        self.play(
            loop[1].animate.set_color(C_GREY),
            loop[2].animate.set_color(C_ORANGE),
            run_time=0.25,
        )
        animate_step(self, view, ax, x_train, run_time=1.0)
        self.next_slide()

        # 4. repeat
        self.play(
            loop[2].animate.set_color(C_GREY),
            loop[3].animate.set_color(C_ORANGE),
            run_time=0.25,
        )

        # Take a couple more steps to show the pattern
        for x_next in [1.2, -0.6, 0.6]:
            new_v = DashedLine(
                ax.c2p(x_next, -1.4),
                ax.c2p(x_next, 1.4),
                color=C_GREY,
                stroke_width=1.0,
                dash_length=0.1,
            )
            new_dot_t = Dot(ax.c2p(x_next, true_fn(x_next)), color=C_GREEN, radius=0.10)
            # Rebuild error visuals for the new training point.
            # make_err_visuals closes over x_t by parameter (no aliasing).
            self.remove(dot_p, err_line, err_lbl, err_arrow)
            dot_p = always_redraw(
                lambda xn=x_next: Dot(
                    ax.c2p(xn, view["current_forward"](xn)),
                    color=C_YELLOW,
                    radius=0.10,
                )
            )
            err_line, err_lbl, err_arrow = make_err_visuals(view, ax, x_next)
            self.play(
                Transform(v_line, new_v),
                Transform(dot_t, new_dot_t),
                run_time=0.3,
            )
            self.add(dot_p, err_line, err_lbl, err_arrow)
            animate_step(self, view, ax, x_next, run_time=0.5)
            self.next_slide()

        # Closing message
        caption = Text(
            "every step shrinks the error a little",
            font_size=20,
            color=C_ORANGE,
        )
        caption.to_edge(DOWN, buff=0.3).shift(RIGHT * 1.5)
        self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.5)
        self.next_slide()

        # Remove always_redraw mobs before fade
        self.remove(
            nn_curve,
            dot_p,
            err_line,
            err_lbl,
            err_arrow,
            *view["w2_lbls"],
            view["b2_lbl"],
            *view["node_lbls"],
        )
        self.play(FadeOut(Group(*self.mobjects)))
