from manim import *
from manim_slides import Slide
from my_slides.shared import *


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
        pixels = (
            VGroup(
                *[
                    Square(
                        side_length=ps,
                        fill_color=pixel_colors[r][c],
                        fill_opacity=1,
                        stroke_color=DARK_BG,
                        stroke_width=1,
                    ).move_to(np.array([c * ps, -r * ps, 0]))
                    for r in range(4)
                    for c in range(4)
                ]
            )
            .center()
            .shift(LEFT * 5.2 + UP * 0.5)
        )
        cat_label = Text("image", font_size=20, color=C_GREY).next_to(
            pixels, DOWN, buff=0.2
        )

        self.play(FadeIn(pixels), FadeIn(cat_label), run_time=0.6)
        self.next_slide()

        flat_vals = [
            0.8,
            0.8,
            0.5,
            0.5,
            0.8,
            0.9,
            0.9,
            0.5,
            0.5,
            0.9,
            0.9,
            0.8,
            0.5,
            0.5,
            0.8,
            0.8,
        ]
        num_mobs = (
            VGroup(
                *[
                    DecimalNumber(v, num_decimal_places=1, font_size=13, color=C_GREY)
                    for v in flat_vals
                ]
            )
            .arrange(RIGHT, buff=0.07)
            .shift(LEFT * 2.5 + UP * 0.5)
        )

        arr_flat = Arrow(
            pixels.get_right(),
            num_mobs.get_left(),
            buff=0.1,
            stroke_width=1.5,
            color=C_GREY,
        )
        self.play(Create(arr_flat), FadeIn(num_mobs), run_time=0.6)
        self.next_slide()

        _, _, net_img = build_network([4, 3, 2], h_spacing=1.4, v_spacing=0.65)
        net_img.shift(RIGHT * 0.8 + UP * 0.5)
        arr_net = Arrow(
            num_mobs.get_right(),
            net_img.get_left(),
            buff=0.1,
            stroke_width=1.5,
            color=C_GREY,
        )
        out_cat = Text('"cat"', font_size=26, color=C_GREEN).next_to(
            net_img, RIGHT, buff=0.4
        )

        self.play(Create(arr_net), FadeIn(net_img), run_time=0.6)
        self.play(FadeIn(out_cat), run_time=0.4)
        self.next_slide()

        # Audio waveform
        ax_audio = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 1],
            x_length=3.0,
            y_length=1.6,
            axis_config={"stroke_width": 1.0, "stroke_color": C_GREY},
            tips=False,
        ).shift(LEFT * 4.5 + DOWN * 2.0)
        waveform = ax_audio.plot(
            lambda x: np.sin(x) * np.exp(-0.1 * x) * 1.2,
            x_range=[0, 4 * PI],
            color=C_INPUT,
            stroke_width=2,
        )
        audio_label = Text("audio", font_size=20, color=C_GREY).next_to(
            ax_audio, DOWN, buff=0.2
        )

        self.play(Create(ax_audio), Create(waveform), FadeIn(audio_label), run_time=0.7)
        self.next_slide()

        out_audio = Text('"Ten-four"', font_size=26, color=C_GREEN).shift(
            RIGHT * 1.0 + DOWN * 2.0
        )
        arr_audio = Arrow(
            ax_audio.get_right(),
            out_audio.get_left(),
            buff=0.2,
            stroke_width=1.5,
            color=C_GREY,
        )
        self.play(Create(arr_audio), FadeIn(out_audio), run_time=0.6)
        self.next_slide()

        tagline = Text(
            "all just numbers — NNs approximate the function that maps them",
            font_size=22,
            color=C_YELLOW,
        )
        tagline.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(tagline, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
