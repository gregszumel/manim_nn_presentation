from manim import *
from manim_slides import Slide
from my_slides.shared import *


# ══════════════════════════════════════════════════════════════════
# Slide 10 — Real World: Images, Audio & Language
# ══════════════════════════════════════════════════════════════════
class Slide10RealWorld(Slide):
    def construct(self):
        self.next_slide()

        title = section_title("but these are just numbers")
        self.play(FadeIn(title), run_time=0.5)

        # ── Layout constants ───────────────────────────────────────
        NET_X  =  0.9   # x-center for all networks
        FLAT_X = -2.9   # x-center for vertical input columns
        GRID_X = -5.3   # x-center for grids / waveform / tokens
        PS     =  0.32  # pixel square side length
        NS     =  0.60  # network scale (smaller to fit 3 rows)
        ROW1_Y =  1.70
        ROW2_Y =  0.0
        ROW3_Y = -1.70

        # ── Shared helpers ─────────────────────────────────────────
        def make_net(y):
            _, _, net = build_network([4, 3, 2], h_spacing=1.2, v_spacing=0.55)
            net.scale(NS).move_to([NET_X, y, 0])
            return net

        def col_positions(center_y, n, spacing):
            """Evenly spaced vertical column of n points centered at center_y."""
            top = center_y + (n - 1) / 2 * spacing
            return [np.array([FLAT_X, top - i * spacing, 0]) for i in range(n)]

        def make_pixel_grid(color_list, center):
            return VGroup(*[
                Square(
                    side_length=PS,
                    fill_color=color_list[r][c],
                    fill_opacity=1,
                    stroke_color=DARK_BG,
                    stroke_width=1,
                ).move_to(np.array([c * PS - 1.5 * PS, -r * PS + 1.5 * PS, 0]))
                for r in range(4)
                for c in range(4)
            ]).move_to(center)

        # ── ROW 1: Image classifier — cat then dog ─────────────────
        cat_colors = [
            ["#FF8C42", "#FF8C42", "#AAAAAA", "#AAAAAA"],
            ["#FF8C42", "#FFDD88", "#FFDD88", "#AAAAAA"],
            ["#AAAAAA", "#FFDD88", "#FFDD88", "#FF8C42"],
            ["#AAAAAA", "#AAAAAA", "#FF8C42", "#FF8C42"],
        ]
        dog_colors = [
            ["#8B6914", "#A67C2E", "#8B6914", "#6B5010"],
            ["#A67C2E", "#C8963C", "#C8963C", "#8B6914"],
            ["#8B6914", "#C8963C", "#C8963C", "#A67C2E"],
            ["#6B5010", "#8B6914", "#A67C2E", "#8B6914"],
        ]
        cat_vals = [0.8, 0.8, 0.5, 0.5, 0.8, 0.9, 0.9, 0.5,
                    0.5, 0.9, 0.9, 0.8, 0.5, 0.5, 0.8, 0.8]
        dog_vals = [0.4, 0.5, 0.4, 0.3, 0.5, 0.6, 0.6, 0.4,
                    0.4, 0.6, 0.6, 0.5, 0.3, 0.4, 0.5, 0.4]

        N_PIX     = 16
        PIX_SP    = 0.115   # vertical spacing between pixel values
        PIX_SCALE = 0.28    # scale factor when pixel flies to column

        net1     = make_net(ROW1_Y)
        cat_grid = make_pixel_grid(cat_colors, [GRID_X, ROW1_Y, 0])
        cat_lbl  = Text("cat image", font_size=16, color=C_GREY).next_to(cat_grid, DOWN, buff=0.12)

        self.play(FadeIn(cat_grid), FadeIn(cat_lbl), run_time=0.5)
        self.next_slide()

        # Each pixel flies from grid position to its slot in the vertical column
        col1_pos = col_positions(ROW1_Y, N_PIX, PIX_SP)
        self.play(
            *[cat_grid[i].animate.move_to(col1_pos[i]).scale(PIX_SCALE) for i in range(N_PIX)],
            FadeOut(cat_lbl),
            run_time=0.8,
        )
        # Swap tiny colored squares → decimal values (keep pixel colors)
        cat_col = VGroup(*[
            DecimalNumber(cat_vals[i], num_decimal_places=1, font_size=10,
                          color=cat_colors[i // 4][i % 4])
            .move_to(col1_pos[i])
            for i in range(N_PIX)
        ])
        self.play(FadeOut(cat_grid), FadeIn(cat_col), run_time=0.3)

        arr1    = Arrow(cat_col.get_right(), net1.get_left(), buff=0.08,
                        stroke_width=1.5, color=C_GREY, max_tip_length_to_length_ratio=0.12)
        out_cat = Text('"cat"', font_size=22, color=C_GREEN).next_to(net1, RIGHT, buff=0.3)
        self.play(FadeIn(net1), Create(arr1), run_time=0.5)
        self.play(FadeIn(out_cat), run_time=0.4)
        self.next_slide()

        # Swap to dog — same network, different input column
        dog_grid   = make_pixel_grid(dog_colors, [GRID_X, ROW1_Y, 0])
        dog_lbl    = Text("dog image", font_size=16, color=C_GREY).next_to(dog_grid, DOWN, buff=0.12)
        out_notcat = Text('"not cat"', font_size=22, color=C_RED).next_to(net1, RIGHT, buff=0.3)

        self.play(FadeOut(out_cat), FadeOut(cat_col), FadeOut(arr1), run_time=0.3)
        self.play(FadeIn(dog_grid), FadeIn(dog_lbl), run_time=0.4)
        self.next_slide()

        self.play(
            *[dog_grid[i].animate.move_to(col1_pos[i]).scale(PIX_SCALE) for i in range(N_PIX)],
            FadeOut(dog_lbl),
            run_time=0.8,
        )
        dog_col = VGroup(*[
            DecimalNumber(dog_vals[i], num_decimal_places=1, font_size=10,
                          color=dog_colors[i // 4][i % 4])
            .move_to(col1_pos[i])
            for i in range(N_PIX)
        ])
        self.play(FadeOut(dog_grid), FadeIn(dog_col), run_time=0.3)

        arr1b = Arrow(dog_col.get_right(), net1.get_left(), buff=0.08,
                      stroke_width=1.5, color=C_GREY, max_tip_length_to_length_ratio=0.12)
        self.play(Create(arr1b), run_time=0.4)
        self.play(FadeIn(out_notcat), run_time=0.4)
        self.next_slide()

        # ── ROW 2: Audio — waveform → sample dots → numbers → rotate ──
        waveform_fn = lambda x: np.sin(x) * np.exp(-0.1 * x) * 1.1

        ax_audio = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.3, 1.3, 1],
            x_length=2.1,
            y_length=1.0,
            axis_config={"stroke_width": 0.8, "stroke_color": C_GREY},
            tips=False,
        ).move_to([GRID_X, ROW2_Y, 0])
        waveform  = ax_audio.plot(waveform_fn, x_range=[0, 4 * PI],
                                  color=C_INPUT, stroke_width=2)
        audio_lbl = Text("audio", font_size=16, color=C_GREY).next_to(ax_audio, DOWN, buff=0.1)

        self.play(Create(ax_audio), Create(waveform), FadeIn(audio_lbl), run_time=0.6)
        self.next_slide()

        # Sample 8 points along waveform — show as dots
        N_AUD  = 8
        samp_x = np.linspace(0.3, 4 * PI - 0.3, N_AUD)
        samp_y = [waveform_fn(x) for x in samp_x]
        samp_v = [round(y, 1) for y in samp_y]

        sample_dots = VGroup(*[
            Dot(ax_audio.c2p(x, y), radius=0.055, color=C_YELLOW)
            for x, y in zip(samp_x, samp_y)
        ])
        self.play(FadeIn(sample_dots), run_time=0.4)

        # Waveform fades; numbers emerge at the sample-dot positions
        h_nums = VGroup(*[
            DecimalNumber(v, num_decimal_places=1, font_size=11, color=C_YELLOW)
            .move_to(ax_audio.c2p(x, y))
            for x, y, v in zip(samp_x, samp_y, samp_v)
        ])
        self.play(
            FadeOut(ax_audio), FadeOut(waveform),
            FadeOut(audio_lbl), FadeOut(sample_dots),
            FadeIn(h_nums),
            run_time=0.5,
        )

        # Rotate: numbers animate from scattered horizontal positions → vertical column
        net2      = make_net(ROW2_Y)
        col2_pos  = col_positions(ROW2_Y, N_AUD, 0.24)
        self.play(
            *[h_nums[i].animate.move_to(col2_pos[i]) for i in range(N_AUD)],
            run_time=0.7,
        )

        arr2      = Arrow(h_nums.get_right(), net2.get_left(), buff=0.08,
                          stroke_width=1.5, color=C_GREY, max_tip_length_to_length_ratio=0.12)
        out_audio = Text('"Ten-four"', font_size=22, color=C_GREEN).next_to(net2, RIGHT, buff=0.3)
        self.play(FadeIn(net2), Create(arr2), run_time=0.5)
        self.play(FadeIn(out_audio), run_time=0.4)
        self.next_slide()

        # ── ROW 3: Text tokens → token IDs → rotate vertical ──────────
        token_words = ["And", "the", "killer", "was", "..."]
        token_ids   = [1870, 262, 8479, 373, 986]
        N_TOK       = len(token_words)

        token_rects = VGroup(*[
            Rectangle(width=0.52, height=0.28,
                      fill_color=C_CLAIM, fill_opacity=0.25,
                      stroke_color=C_CLAIM, stroke_width=1)
            for _ in token_words
        ]).arrange(RIGHT, buff=0.05)
        token_labels = VGroup(*[
            Text(w, font_size=11, color=C_CLAIM).move_to(token_rects[i])
            for i, w in enumerate(token_words)
        ])
        token_group = VGroup(token_rects, token_labels).move_to([GRID_X, ROW3_Y, 0])
        llm_lbl     = Text("mystery novel", font_size=16, color=C_GREY).next_to(
            token_group, DOWN, buff=0.1
        )

        self.play(FadeIn(token_group), FadeIn(llm_lbl), run_time=0.5)
        self.next_slide()

        # Words → numeric token IDs (swap labels in place, keep rects)
        id_labels = VGroup(*[
            Text(str(tid), font_size=11, color=C_CLAIM).move_to(token_rects[i].get_center())
            for i, tid in enumerate(token_ids)
        ])
        self.play(FadeOut(token_labels), FadeIn(id_labels), run_time=0.4)

        # Rotate: horizontal token blocks animate to vertical column
        net3     = make_net(ROW3_Y)
        col3_pos = col_positions(ROW3_Y, N_TOK, 0.30)
        self.play(
            *[token_rects[i].animate.move_to(col3_pos[i]) for i in range(N_TOK)],
            *[id_labels[i].animate.move_to(col3_pos[i]) for i in range(N_TOK)],
            FadeOut(llm_lbl),
            run_time=0.7,
        )

        arr3    = Arrow(token_rects.get_right(), net3.get_left(), buff=0.08,
                        stroke_width=1.5, color=C_GREY, max_tip_length_to_length_ratio=0.12)
        out_llm = Text('"Mustard"', font_size=22, color=C_GREEN).next_to(net3, RIGHT, buff=0.3)
        self.play(FadeIn(net3), Create(arr3), run_time=0.5)
        self.play(FadeIn(out_llm), run_time=0.4)
        self.next_slide()

        # ── Tagline ────────────────────────────────────────────────────
        tagline = Text(
            "all just numbers — NNs approximate the function that maps them",
            font_size=19,
            color=C_YELLOW,
        ).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(tagline, shift=UP * 0.1), run_time=0.6)
        self.next_slide()

        self.play(FadeOut(Group(*self.mobjects)))
