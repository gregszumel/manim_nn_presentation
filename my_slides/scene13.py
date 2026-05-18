from manim import *
from manim_slides import Slide
from my_slides.shared import *
from my_slides.scene11 import (
    W1,
    B1,
    N_HIDDEN,
    LR,
    true_fn,
    forward,
    grad_step,
    W2_INIT,
    B2_INIT,
)
from my_slides.scene12 import TRAIN_XS, N_EPOCHS
import numpy as np


# ── Replay scene12's training to get the final trained weights ────
def _train_final_weights():
    W2 = W2_INIT.copy()
    b2 = float(B2_INIT)
    for _ in range(N_EPOCHS):
        for x in TRAIN_XS:
            W2, b2 = grad_step(float(x), true_fn(float(x)), W2, b2)
    return W2, b2


W2_FINAL, B2_FINAL = _train_final_weights()


def trained_forward(x):
    return forward(x, W2_FINAL, B2_FINAL)


def fill_between(ax, f1, f2, x_range, color, opacity=0.30):
    """Polygon filling the area between two curves over x_range."""
    xs = np.linspace(x_range[0], x_range[1], 220)
    top = [ax.c2p(float(x), float(f1(x))) for x in xs]
    bot = [ax.c2p(float(x), float(f2(x))) for x in reversed(xs)]
    return Polygon(
        *top,
        *bot,
        color=color,
        fill_color=color,
        fill_opacity=opacity,
        stroke_width=0,
    ).set_z_index(-1)


# ══════════════════════════════════════════════════════════════════
# Slide 13 — Zoom out: training vs. validation vs. test
# ══════════════════════════════════════════════════════════════════
class Slide13RandomFunction(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("but did it really learn the function?")
        self.play(FadeIn(title), run_time=0.5)

        # ── Narrow axes: same view as scene12 ─────────────────────
        ax = Axes(
            x_range=[-2.0, 2.0, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=7.5,
            y_length=4.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(DOWN * 0.3)
        self.play(Create(ax), run_time=0.5)

        target = ax.plot(true_fn, x_range=[-1.9, 1.9], color=C_GREEN, stroke_width=3)
        nn_curve = ax.plot(
            trained_forward,
            x_range=[-1.9, 1.9],
            color=C_YELLOW,
            stroke_width=2.5,
        )
        target_lbl = Text("target", font_size=18, color=C_GREEN)
        nn_lbl = Text("NN", font_size=18, color=C_YELLOW)
        target_lbl.next_to(ax, UP, buff=0.1).shift(LEFT * 1.0)
        nn_lbl.next_to(target_lbl, RIGHT, buff=0.4)

        train_dots = VGroup(
            *[
                Dot(ax.c2p(float(x), true_fn(float(x))), radius=0.06, color=C_GREY)
                for x in TRAIN_XS
            ]
        )

        self.play(
            Create(target),
            Create(nn_curve),
            FadeIn(target_lbl),
            FadeIn(nn_lbl),
            FadeIn(train_dots),
            run_time=1.0,
        )
        self.next_slide()

        # ── Zoom out: replace with wider axes ─────────────────────
        ax_wide = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 14, 2],
            x_length=7.5,
            y_length=4.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).move_to(ax.get_center())

        target_wide = ax_wide.plot(
            true_fn,
            x_range=[-4.8, 4.8],
            color=C_GREEN,
            stroke_width=3,
        )
        nn_wide = ax_wide.plot(
            trained_forward,
            x_range=[-4.8, 4.8],
            color=C_YELLOW,
            stroke_width=2.5,
        )
        train_dots_wide = VGroup(
            *[
                Dot(ax_wide.c2p(float(x), true_fn(float(x))), radius=0.06, color=C_GREY)
                for x in TRAIN_XS
            ]
        )

        self.play(
            ReplacementTransform(ax, ax_wide),
            ReplacementTransform(target, target_wide),
            ReplacementTransform(nn_curve, nn_wide),
            ReplacementTransform(train_dots, train_dots_wide),
            run_time=1.4,
        )
        self.next_slide()

        # ── Fill the gap with red: "look at that error" ───────────
        err_fill = fill_between(
            ax_wide,
            true_fn,
            trained_forward,
            x_range=[-4.8, 4.8],
            color=C_RED,
            opacity=0.32,
        )
        err_caption = Text(
            "the error is huge outside the training domain",
            font_size=22,
            color=C_RED,
        )
        err_caption.to_edge(DOWN, buff=0.4)
        self.play(
            FadeIn(err_fill),
            FadeIn(err_caption, shift=UP * 0.1),
            run_time=0.8,
        )
        self.next_slide()

        # ── Red circle around training domain ─────────────────────
        # Use an Ellipse sized in screen space so it cleanly encloses
        # the training points (which lie on the target curve in [-1.6, 1.6]).
        left_pt = ax_wide.c2p(-1.6, true_fn(-1.6))
        right_pt = ax_wide.c2p(1.6, true_fn(1.6))
        bottom_pt = ax_wide.c2p(0.0, true_fn(0.0))
        center = ax_wide.c2p(0.0, (true_fn(0.0) + true_fn(1.6)) / 2)

        width = (right_pt[0] - left_pt[0]) + 0.6
        height = (left_pt[1] - bottom_pt[1]) * 2 + 0.6

        train_circle = Ellipse(
            width=width,
            height=height,
            color=C_RED,
            stroke_width=3,
            fill_color=C_RED,
            fill_opacity=0.12,
        ).move_to(center)
        train_label = Text("training data", font_size=20, color=C_RED)
        train_label.next_to(train_circle, DOWN, buff=0.15)

        self.play(
            FadeOut(err_fill),
            FadeOut(err_caption),
            Create(train_circle),
            FadeIn(train_label, shift=UP * 0.1),
            run_time=0.8,
        )
        self.next_slide()

        # ── Validation points: a few inside, some just outside ────
        val_xs = [-1.8, -0.9, 0.3, 1.1, 2.2, -2.4]
        val_dots = VGroup(
            *[
                Dot(ax_wide.c2p(x, true_fn(x)), radius=0.08, color=C_INPUT)
                for x in val_xs
            ]
        )
        val_label = Text("validation", font_size=20, color=C_INPUT)
        val_label.to_edge(UP, buff=0.9).shift(RIGHT * 4.0)

        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in val_dots], lag_ratio=0.1),
            FadeIn(val_label),
            run_time=1.0,
        )
        self.next_slide()

        # ── Test points: clearly out-of-domain ────────────────────
        test_xs = [-4.2, -3.5, 3.3, 4.0, 4.6]
        test_dots = VGroup(
            *[
                Dot(ax_wide.c2p(x, true_fn(x)), radius=0.08, color=C_ORANGE)
                for x in test_xs
            ]
        )
        test_label = Text("test data", font_size=20, color=C_ORANGE)
        test_label.next_to(val_label, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in test_dots], lag_ratio=0.1),
            FadeIn(test_label),
            run_time=1.0,
        )
        self.next_slide()

        # ── Punchline ─────────────────────────────────────────────
        # Floats in the middle of the chart with a dark backing card so
        # it reads clearly against the curves and dots behind it.
        caption_text = Text(
            "the network only learned the function on the training domain",
            font_size=22,
            color=C_ORANGE,
        )
        caption_bg = SurroundingRectangle(
            caption_text,
            color=C_ORANGE,
            buff=0.22,
            fill_color=DARK_BG,
            fill_opacity=0.92,
            corner_radius=0.12,
            stroke_width=1.5,
        )
        caption = VGroup(caption_bg, caption_text)
        caption.move_to(ax_wide.c2p(0, 7.5)).set_z_index(20)
        self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        # ══════════════════════════════════════════════════════════
        # Tie back to universal function approximation:
        # the same idea applies to image → label functions.
        # ══════════════════════════════════════════════════════════

        # Zoom back in to the training axes; drop dots, circle, curves.
        ax_zoom = Axes(
            x_range=[-2.0, 2.0, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=7.5,
            y_length=4.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
            tips=False,
        ).move_to(ax_wide.get_center())

        self.play(
            FadeOut(train_circle),
            FadeOut(train_label),
            FadeOut(val_dots),
            FadeOut(val_label),
            FadeOut(test_dots),
            FadeOut(test_label),
            FadeOut(train_dots_wide),
            FadeOut(target_wide),
            FadeOut(nn_wide),
            FadeOut(target_lbl),
            FadeOut(nn_lbl),
            FadeOut(caption),
            ReplacementTransform(ax_wide, ax_zoom),
            run_time=1.0,
        )
        self.next_slide()

        # Reframe the axes: below y=0 is "cat", above is "not cat".
        not_cat_lbl = Text("not cat", font_size=20, color=C_INPUT)
        cat_lbl = Text("cat", font_size=20, color=C_ORANGE)
        not_cat_lbl.next_to(ax_zoom.c2p(-2.0, 0.75), RIGHT, buff=0.1)
        cat_lbl.next_to(ax_zoom.c2p(-2.0, -0.75), RIGHT, buff=0.1)

        boundary = DashedLine(
            ax_zoom.c2p(-2.0, 0),
            ax_zoom.c2p(2.0, 0),
            color=C_GREY,
            stroke_width=1.5,
            dash_length=0.12,
        )
        self.play(
            Create(boundary),
            FadeIn(not_cat_lbl),
            FadeIn(cat_lbl),
            run_time=0.6,
        )
        self.next_slide()

        # ── Fade in training images ───────────────────────────────
        # All cats here are MY personal cat (training set = "my cat" only).
        # Cats: bottom-left quadrant only — no cats in bottom-right!
        # Non-cats: top half, spread across BOTH sides.
        # All training points sit ON the parabola — y == true catness.
        def _cat(path, x):
            return (path, x, true_fn(x))

        cat_specs = [
            _cat("assets/cat1.jpeg", -1.15),
            _cat("assets/cat2.jpg", -0.75),
            _cat("assets/cat3.jpeg", -0.40),
            _cat("assets/cat4.jpeg", -0.10),
        ]
        not_cat_specs = [
            _cat("assets/goat.jpg", -1.85),  # swapped with dog
            _cat("assets/dog.jpg", -1.50),  # swapped with goat
            _cat("assets/bison.jpeg", 1.50),  # swapped with hawk
            _cat("assets/hawk.jpg", 1.85),  # swapped with bison
        ]

        def _make_img(path, x, y, h=0.75):
            img = ImageMobject(path)
            img.height = h
            img.move_to(ax_zoom.c2p(x, y))
            img.set_z_index(5)
            return img

        cat_imgs = [_make_img(p, x, y) for (p, x, y) in cat_specs]
        not_cat_imgs = [_make_img(p, x, y) for (p, x, y) in not_cat_specs]

        self.play(
            LaggedStart(
                *[FadeIn(im, scale=0.8) for im in (not_cat_imgs + cat_imgs)],
                lag_ratio=0.12,
            ),
            run_time=1.4,
        )
        self.next_slide()

        # ── Condense each image into its training dot ─────────────
        cat_dots = [
            Dot(ax_zoom.c2p(x, y), radius=0.08, color=C_ORANGE)
            for (_, x, y) in cat_specs
        ]
        not_cat_dots = [
            Dot(ax_zoom.c2p(x, y), radius=0.08, color=C_INPUT)
            for (_, x, y) in not_cat_specs
        ]

        shrink_anims = []
        for im, dot in zip(cat_imgs + not_cat_imgs, cat_dots + not_cat_dots):
            shrink_anims.append(
                AnimationGroup(
                    im.animate.scale(0.05).move_to(dot.get_center()),
                    FadeIn(dot),
                    lag_ratio=0.7,
                )
            )
        self.play(
            LaggedStart(*shrink_anims, lag_ratio=0.08),
            run_time=1.6,
        )
        self.remove(*cat_imgs, *not_cat_imgs)
        self.next_slide()

        # ── Reveal the TRUE function (parabola) — ghosted ─────────
        # This is the "true catness" function we wish we could learn.
        # Negative ⇒ cat. The model never sees this directly.
        true_curve = ax_zoom.plot(
            true_fn,
            x_range=[-1.95, 1.95],
            color=C_GREEN,
            stroke_width=2.5,
        )
        # set_opacity() would set fill_opacity too (and color= seeded the
        # fill green), so use set_stroke() to dim only the stroke.
        true_curve.set_stroke(opacity=0.55).set_fill(opacity=0)
        true_curve_lbl = Text("true 'catness' (unknown)", font_size=16, color=C_GREEN)
        true_curve_lbl.next_to(ax_zoom, UP, buff=0.1).shift(LEFT * 2.0)
        self.play(
            Create(true_curve),
            FadeIn(true_curve_lbl),
            run_time=0.9,
        )
        self.next_slide()

        # ── The NN learns a "cat dip" — overfit to where cats appeared ─
        # Positive baseline (says "not cat") except for a Gaussian dip
        # around x = -0.6, where the training cats clustered.
        def learned_fn(x):
            return 0.4 - 1.4 * float(np.exp(-2.5 * (x + 0.6) ** 2))

        learned_curve = ax_zoom.plot(
            learned_fn,
            x_range=[-1.95, 1.95],
            color=C_YELLOW,
            stroke_width=3,
        )
        learned_lbl = Text("what the NN learned", font_size=16, color=C_YELLOW)
        learned_lbl.next_to(true_curve_lbl, RIGHT, buff=0.4)
        self.play(
            Create(learned_curve),
            FadeIn(learned_lbl),
            run_time=1.0,
        )
        self.next_slide()

        # ── The reveal: an orange cat in the bottom-right ─────────
        # On the parabola, just like training cats — true catness ≈ -0.51.
        orange_x = 0.9
        orange_y = true_fn(orange_x)
        orange_img = ImageMobject("assets/orange cat.jpeg")
        orange_img.height = 0.75
        orange_img.move_to(ax_zoom.c2p(orange_x, orange_y))
        orange_img.set_z_index(6)
        self.play(FadeIn(orange_img, scale=0.8), run_time=0.6)
        self.next_slide()

        # Vertical probe line at x = orange cat's x.
        # The cat itself sits ON the parabola — it IS the "true catness"
        # intersection — so we only mark the NN intersection separately.
        learn_y = learned_fn(orange_x)
        probe = DashedLine(
            ax_zoom.c2p(orange_x, orange_y),
            ax_zoom.c2p(orange_x, learn_y),
            color=C_GREY,
            stroke_width=1.5,
            dash_length=0.10,
        )
        learn_hit = Dot(
            ax_zoom.c2p(orange_x, learn_y),
            radius=0.09,
            color=C_YELLOW,
        ).set_z_index(7)

        true_call = Text("true: cat ✓", font_size=18, color=C_GREEN)
        nn_call = Text("NN: not cat ✗", font_size=18, color=C_RED)
        true_call.next_to(orange_img, DOWN, buff=0.1)
        nn_call.next_to(learn_hit, UP + RIGHT, buff=0.1)

        self.play(FadeIn(true_call), run_time=0.4)
        self.play(Create(probe), run_time=0.4)
        self.play(
            FadeIn(learn_hit),
            FadeIn(nn_call),
            run_time=0.5,
        )
        self.next_slide()

        # ── Closing tie-back ──────────────────────────────────────
        tie_back = Text(
            "we learned a function — just not the one we wanted",
            font_size=22,
            color=C_ORANGE,
        )
        tie_back.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(tie_back, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        # ══════════════════════════════════════════════════════════
        # WHISPER — a real-world example of the same idea
        # ══════════════════════════════════════════════════════════
        # Sweep the chart, keep the orange cat as the metaphor anchor.
        chart_mobs = [
            ax_zoom,
            boundary,
            not_cat_lbl,
            cat_lbl,
            true_curve,
            true_curve_lbl,
            learned_curve,
            learned_lbl,
            probe,
            learn_hit,
            true_call,
            nn_call,
            tie_back,
            *cat_dots,
            *not_cat_dots,
        ]
        self.play(
            *[FadeOut(m) for m in chart_mobs],
            FadeOut(title),
            orange_img.animate.scale(2.4).move_to(LEFT * 4.7 + UP * 2.3),
            run_time=1.0,
        )

        whisper_title = section_title("this happened with Whisper")
        self.play(FadeIn(whisper_title), run_time=0.6)
        self.next_slide()

        whisper_beats = [
            ("- we fine-tuned Whisper on English-only audio", C_CLAIM),
            ("- it got better at English ✓", C_GREEN),
            ("- but it lost its ability to detect other languages ✗", C_RED),
            ("- the orange cat was Spanish", C_ORANGE),
        ]
        whisper_mobs = VGroup(
            *[Text(b, font_size=26, color=c) for (b, c) in whisper_beats]
        )
        whisper_mobs.arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        whisper_mobs.move_to(RIGHT * 0.5 + DOWN * 0.2)
        for m in whisper_mobs:
            m.set_opacity(0)
        self.add(whisper_mobs)

        for m in whisper_mobs:
            self.play(m.animate.set_opacity(1.0), run_time=0.5)
            self.next_slide()

        # ── Transition to the prompts epilogue ────────────────────
        self.play(
            FadeOut(whisper_mobs),
            FadeOut(whisper_title),
            run_time=0.5,
        )

        # ══════════════════════════════════════════════════════════
        # EPILOGUE — call to action: this is how prompting works too
        # ══════════════════════════════════════════════════════════
        epilogue_title = section_title("the same thing happens with prompts")
        self.play(FadeIn(epilogue_title), run_time=0.6)
        self.next_slide()

        # ── Three beats ───────────────────────────────────────────
        beats = [
            "- prompting on a few examples is like training on as many",
            "- they can therefore also have 'orange cats' - out of domain examples",
            "- keep a holdout set you never tune against, you only evaluate on",
            "- as soon as you evaluate on hold-out set enough, it \nhas become your training set",
        ]
        beat_mobs = VGroup(*[Text(b, font_size=26, color=C_GREEN) for b in beats])
        beat_mobs.arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        beat_mobs.move_to(RIGHT * 0.5 + DOWN * 0.7)
        for m in beat_mobs:
            m.set_opacity(0)
        self.add(beat_mobs)

        for m in beat_mobs:
            self.play(m.animate.set_opacity(1.0), run_time=0.5)
            self.next_slide()

        # ══════════════════════════════════════════════════════════
        # FINAL CARD — recap + summer-series ask
        # ══════════════════════════════════════════════════════════
        self.play(
            FadeOut(beat_mobs),
            FadeOut(epilogue_title),
            FadeOut(orange_img),
            run_time=0.7,
        )

        recap_title = Text("hopefully this talk:", font_size=32, color=WHITE)
        recap_title.to_edge(UP, buff=0.9).shift(LEFT * 2.5)

        recap_items = [
            "gave you a better understanding of neural networks",
            "showed you how they're trained",
            "showed you how to evaluate your own prompting with LLMs",
        ]
        recap_mobs = VGroup(
            *[Text(f"•  {t}", font_size=24, color=C_GREEN) for t in recap_items]
        )
        recap_mobs.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        recap_mobs.next_to(recap_title, DOWN, buff=0.5, aligned_edge=LEFT).shift(
            RIGHT * 0.3
        )

        self.play(FadeIn(recap_title, shift=UP * 0.1), run_time=0.6)
        for m in recap_mobs:
            self.play(FadeIn(m, shift=RIGHT * 0.1), run_time=0.4)
        self.next_slide()

        cta_line1 = Text(
            "want to learn more — even build your own LLM from scratch?",
            font_size=24,
            color=C_YELLOW,
        )
        cta_line2 = Text(
            "please reach out!",
            font_size=24,
            color=C_YELLOW,
        )
        cta = VGroup(cta_line1, cta_line2).arrange(DOWN, buff=0.25)
        cta.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(cta, shift=UP * 0.1), run_time=0.8)
        self.next_slide()

        thanks = Text("thank you!", font_size=44, slant=ITALIC, color=C_ORANGE)
        thanks.move_to(ORIGIN)

        # Flank the thanks with the two cats from the story:
        # the personal cat (training) and the orange cat (out-of-domain).
        final_cat = ImageMobject("assets/cat1.jpeg")
        final_cat.height = 1.6
        final_cat.next_to(thanks, LEFT, buff=1.0)

        final_orange = ImageMobject("assets/orange cat.jpeg")
        final_orange.height = 1.6
        final_orange.next_to(thanks, RIGHT, buff=1.0)

        self.play(
            FadeOut(recap_title),
            FadeOut(recap_mobs),
            FadeOut(cta),
            FadeIn(thanks, scale=0.9),
            # FadeIn(final_cat, shift=RIGHT * 0.2),
            # FadeIn(final_orange, shift=LEFT * 0.2),
            run_time=0.9,
        )
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
