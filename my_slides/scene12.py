from manim import *
from manim_slides import Slide
from my_slides.shared import *
from my_slides.scene11 import (
    N_HIDDEN,
    W1,
    B1,
    LR,
    true_fn,
    forward,
    grad_step,
    W2_INIT,
    B2_INIT,
    build_training_view,
    animate_step,
)
import numpy as np

# 8 training points evenly across [-1.6, 1.6], visited each epoch
TRAIN_XS = np.linspace(-1.6, 1.6, 8)
N_EPOCHS = 10


# ══════════════════════════════════════════════════════════════════
# Slide 12 — Watching Gradient Descent  (full training, 3 epochs)
# ══════════════════════════════════════════════════════════════════
class Slide12TrainingInAction(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("watching gradient descent")
        self.play(FadeIn(title), run_time=0.5)

        # ── Axes (left) ────────────────────────────────────────────
        ax = Axes(
            x_range=[-2.0, 2.0, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=5.0,
            y_length=3.8,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(LEFT * 2.7 + DOWN * 0.6)
        self.play(Create(ax), run_time=0.4)

        # Target curve
        target = ax.plot(true_fn, x_range=[-1.9, 1.9], color=C_GREEN, stroke_width=3)
        target_lbl = Text("target", font_size=16, color=C_GREEN)
        target_lbl.next_to(ax, UP, buff=0.1).shift(LEFT * 1.0)

        # NN diagram + live weights
        view = build_training_view(self)
        W2_trackers, b2_tracker = view["trackers"]
        flat_neurons = [n for layer in view["neurons"] for n in layer]

        self.play(
            Create(target),
            FadeIn(target_lbl),
            LaggedStart(*[FadeIn(n) for n in flat_neurons], lag_ratio=0.05),
            run_time=0.6,
        )
        self.play(
            LaggedStart(*[Create(e) for e in view["edges"].values()], lag_ratio=0.02),
            run_time=0.5,
        )
        self.add(*view["w1_lbls"], *view["w2_lbls"], view["b2_lbl"])
        # Reveal neuron-value labels with a brief FadeIn so the audience
        # notices them appearing inside each neuron.
        self.play(
            *[FadeIn(lbl) for lbl in view["node_lbls"]],
            run_time=0.4,
        )

        # NN curve (live)
        nn_curve = always_redraw(
            lambda: ax.plot(
                view["current_forward"],
                x_range=[-1.9, 1.9],
                color=C_YELLOW,
                stroke_width=2.5,
            )
        )
        nn_lbl = Text("NN", font_size=16, color=C_YELLOW)
        nn_lbl.next_to(target_lbl, RIGHT, buff=0.4)
        self.add(nn_curve)
        self.play(FadeIn(nn_lbl), run_time=0.3)

        # Training point markers along the x-axis
        train_marks = VGroup(
            *[
                Dot(ax.c2p(float(x), 0), radius=0.05, color=C_GREY, fill_opacity=0.7)
                for x in TRAIN_XS
            ]
        )
        self.play(FadeIn(train_marks), run_time=0.3)

        # Epoch + loss counter (bottom)
        epoch_lbl = Text("epoch 0", font_size=20, color=C_INPUT)
        epoch_lbl.to_edge(DOWN, buff=0.4).shift(LEFT * 4.0)

        # Live loss: static "loss = " + DecimalNumber updater (avoids the
        # always_redraw-with-Text SVG-cache race condition).
        loss_prefix = Text("loss =", font_size=20, color=C_ORANGE)
        loss_value = DecimalNumber(
            0.0,
            num_decimal_places=3,
            font_size=32,
            color=C_ORANGE,
        )
        loss_lbl = VGroup(loss_prefix, loss_value).arrange(RIGHT, buff=0.10)
        loss_lbl.to_edge(DOWN, buff=0.4).shift(RIGHT * 4.0)
        loss_value.add_updater(
            lambda d: d.set_value(
                float(
                    np.mean(
                        [
                            (view["current_forward"](x) - true_fn(x)) ** 2
                            for x in TRAIN_XS
                        ]
                    )
                )
            )
        )
        self.add(loss_lbl)
        self.play(FadeIn(epoch_lbl), run_time=0.3)
        self.next_slide()

        # ══════════════════════════════════════════════════════════
        # Training loop — N_EPOCHS passes through TRAIN_XS
        # ══════════════════════════════════════════════════════════
        for epoch in range(1, N_EPOCHS + 1):
            new_epoch_lbl = Text(f"epoch {epoch}", font_size=20, color=C_INPUT)
            new_epoch_lbl.move_to(epoch_lbl)
            self.play(Transform(epoch_lbl, new_epoch_lbl), run_time=0.2)

            for x_train in TRAIN_XS:
                animate_step(
                    self,
                    view,
                    ax,
                    float(x_train),
                    run_time=0.18,
                    flash_error=True,
                )

            self.next_slide()

        # ── Convergence punchline ──────────────────────────────────
        punchline = Text(
            "the network has learned the function",
            font_size=22,
            color=C_ORANGE,
        )
        punchline.to_edge(DOWN, buff=0.4).move_to(epoch_lbl, aligned_edge=LEFT).shift(
            RIGHT * 0.5
        )
        self.remove(epoch_lbl)
        self.play(FadeIn(punchline, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        # # ════════════════════════════════════════════════════════════
        # # — Overfitting: zoom out to show extrapolation failure —
        # # ════════════════════════════════════════════════════════════
        #
        # self.play(
        #     FadeOut(punchline, target_lbl, nn_lbl, train_marks),
        #     run_time=0.4,
        # )
        # self.remove(nn_curve, target, loss_lbl)
        # self.play(FadeOut(ax), run_time=0.4)
        #
        # # Wide-range axes — same physical size, larger coordinate ranges
        # old_center = ax.get_center()
        # ax_wide = Axes(
        #     x_range=[-6, 6, 2],
        #     y_range=[-8, 25, 5],
        #     x_length=5.0,
        #     y_length=3.8,
        #     axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
        #     tips=False,
        # ).move_to(old_center)
        # self.play(Create(ax_wide), run_time=0.5)
        #
        # # Re-plot target and trained NN on the wide range
        # target_wide = ax_wide.plot(
        #     true_fn, x_range=[-5.8, 5.8], color=C_GREEN, stroke_width=3,
        # )
        # nn_wide = ax_wide.plot(
        #     view["current_forward"],
        #     x_range=[-5.8, 5.8],
        #     color=C_YELLOW,
        #     stroke_width=2.5,
        # )
        #
        # t_lbl = Text("target", font_size=14, color=C_GREEN)
        # t_lbl.next_to(ax_wide, UP, buff=0.12)
        # n_lbl = Text("NN", font_size=14, color=C_YELLOW)
        # n_lbl.next_to(t_lbl, RIGHT, buff=0.3)
        #
        # self.play(
        #     Create(target_wide), Create(nn_wide),
        #     FadeIn(t_lbl), FadeIn(n_lbl),
        #     run_time=0.7,
        # )
        # self.next_slide()
        #
        # # Highlight the original training range [-1.6, 1.6]
        # left_pt = ax_wide.c2p(-1.6, ax_wide.y_range[0])
        # right_pt = ax_wide.c2p(1.6, ax_wide.y_range[1])
        # band_w = right_pt[0] - left_pt[0]
        # train_band = Rectangle(
        #     width=band_w,
        #     height=ax_wide.y_length,
        #     fill_color=C_GREY,
        #     fill_opacity=0.15,
        #     stroke_color=C_GREY,
        #     stroke_width=1.5,
        #     stroke_opacity=0.4,
        # )
        # train_band.move_to(ax_wide.get_center())
        #
        # train_lbl = Text("training\nrange", font_size=16, color=C_GREY, line_spacing=0.9)
        # train_lbl.next_to(train_band, DOWN, buff=0.15)
        #
        # self.play(
        #     FadeIn(train_band), FadeIn(train_lbl),
        #     run_time=0.5,
        # )
        # self.next_slide()
        #
        # # The punchline: overfitting
        # diverge = Text(
        #     "matches perfectly where it trained,\nfalls apart everywhere else",
        #     font_size=20, color=C_RED,
        #     line_spacing=1.1,
        # )
        # diverge.to_edge(DOWN, buff=0.4)
        # self.play(FadeIn(diverge, shift=UP * 0.1), run_time=0.6)
        # self.next_slide()
        #
        # # Cleanup
        # self.remove(
        #     nn_wide,
        #     *view["w2_lbls"], view["b2_lbl"],
        #     *view["node_lbls"],
        # )
        # self.play(FadeOut(Group(*self.mobjects)))
