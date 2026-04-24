from manim import *


# ─────────────────────────────────────────────────────────────────────────────
# Scene 1 — RowhammerIntro
# Script 1:  81 words × 0.4 sec/word = 32.4 sec
# Script 2:  68 words × 0.4 sec/word = 27.2 sec
# ─────────────────────────────────────────────────────────────────────────────
class RowhammerIntro(Scene):
    def construct(self):

        # ═════════════════════════════════════════════════════════════════════
        # PART 1 — Title Card + Binary Stream
        # ═════════════════════════════════════════════════════════════════════

        # "We live in a world entirely dependent on digital data."
        # 10 words × 0.4 = 4.0 sec
        title    = Text("Coding Theory", font_size=64, weight=BOLD)
        subtitle = Text("& The Rowhammer Attack", font_size=38, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.4)
        title_group = VGroup(title, subtitle)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.wait(4.0 - 1.5 - 0.8)   # 1.7 sec remaining

        # "But whether that data is flying through the air as a Wi-Fi signal
        #  or sitting quietly in a server, it is physically vulnerable to noise."
        # 25 words × 0.4 = 10.0 sec
        self.wait(10.0)

        # "This is where coding theory comes in."
        # 7 words × 0.4 = 2.8 sec
        self.wait(2.8)

        # Fade out title → transition into binary stream
        self.play(FadeOut(title_group), run_time=0.8)

        # Fixed bit positions — no randomness so renders stay reproducible
        BIT_POSITIONS = [
            (-6.0, 2.5), (-4.5, 1.8), (-2.8, 3.0), (-1.2, 2.2), (0.5, 3.1),
            (2.0,  2.6), (3.8,  1.9), (5.5,  2.8),
            (-6.2, 0.5), (-4.0,-0.2), (-2.0, 0.8), (0.0,  0.0), (2.2,  0.4),
            (4.1, -0.5), (5.8,  0.3),
            (-5.5,-1.5), (-3.3,-2.0), (-1.0,-1.2), (1.0, -2.1), (3.0, -1.8),
            (5.0, -2.3),
            (-6.0,-3.1), (-3.8,-3.4), (-1.5,-3.0), (0.8, -3.2), (2.8, -3.5),
            (5.2, -3.1),
        ]
        BIT_VALUES = "10100110011010010100101100101"

        bits = VGroup(*[
            Text(b, font_size=28, color=GREEN if b == "1" else BLUE_B)
            .move_to([x, y, 0])
            for (x, y), b in zip(BIT_POSITIONS, BIT_VALUES)
        ])

        # "Coding theory is the mathematical study of how to transmit and store
        #  data reliably, even when physical interference tries to corrupt it."
        # 23 words × 0.4 = 9.2 sec  (0.8 fade-out + 1.5 fade-in already account for part)
        self.play(FadeIn(bits, lag_ratio=0.04), run_time=1.5)
        self.wait(9.2 - 0.8 - 1.5)   # 6.9 sec remaining

        # "Today, we are looking at a specific physical interference happening
        #  inside our computers called Rowhammer."
        # 16 words × 0.4 = 6.4 sec
        rowhammer_label = Text("Rowhammer", font_size=80, color=RED, weight=BOLD)
        self.play(FadeOut(bits), FadeIn(rowhammer_label), run_time=1.0)
        self.wait(6.4 - 1.0)   # 5.4 sec
        self.play(FadeOut(rowhammer_label), run_time=0.8)

        # ═════════════════════════════════════════════════════════════════════
        # PART 2 — DRAM Grid + Rowhammer Visualization
        # ═════════════════════════════════════════════════════════════════════

        ROWS, COLS = 5, 5
        SIDE, GAP  = 0.82, 0.13
        STEP       = SIDE + GAP        # 0.95 units between cell centers
        HAMMER_ROW = 2                 # index of the "hammered" row

        # Hardcoded 5×5 bit values — fully reproducible
        BIT_DATA = [
            [1, 0, 1, 0, 1],   # Row 0
            [0, 1, 1, 0, 0],   # Row 1 — adjacent (above hammered)
            [1, 0, 0, 1, 1],   # Row 2 — HAMMERED
            [0, 1, 0, 0, 1],   # Row 3 — adjacent (below hammered)
            [1, 1, 0, 1, 0],   # Row 4
        ]

        # Build cells[r][c] = VGroup(Square, Text bit-label)
        cells = []
        all_cells_vgroup = VGroup()
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                sq = Square(side_length=SIDE, fill_opacity=0.35)
                sq.set_fill(BLUE_D)
                sq.set_stroke(BLUE_B, width=1.5)
                sq.move_to([
                    (c - (COLS - 1) / 2) * STEP,
                    ((ROWS - 1) / 2 - r) * STEP - 0.25,
                    0
                ])
                lbl = Text(str(BIT_DATA[r][c]), font_size=20, color=WHITE)
                lbl.move_to(sq)
                cell = VGroup(sq, lbl)
                row.append(cell)
                all_cells_vgroup.add(cell)
            cells.append(row)

        # Row labels on the left
        row_labels = VGroup(*[
            Text(f"Row {r}", font_size=15, color=GRAY)
            .move_to([-(COLS / 2) * STEP - 0.65,
                      ((ROWS - 1) / 2 - r) * STEP - 0.25, 0])
            for r in range(ROWS)
        ])

        dram_title = Text("DRAM Memory", font_size=34, color=WHITE)
        dram_title.to_edge(UP, buff=0.35)

        # "Modern computer memory, or DRAM, is arranged in a massive grid of
        #  rows and columns."
        # 15 words × 0.4 = 6.0 sec
        self.play(FadeIn(dram_title), Write(row_labels), run_time=1.0)
        self.play(FadeIn(all_cells_vgroup, lag_ratio=0.03), run_time=1.5)
        self.wait(6.0 - 1.0 - 1.5)   # 3.5 sec remaining

        # "As manufacturers pack these rows closer together to increase capacity,
        #  a dangerous electrical vulnerability emerges."
        # 14 words × 0.4 = 5.6 sec
        self.wait(5.6)

        # "If a malicious program repeatedly accesses, or 'hammers,' a specific
        #  row of memory, the electrical charge leaks."
        # 17 words × 0.4 = 6.8 sec

        # Colour hammer row red
        self.play(
            *[cells[HAMMER_ROW][c][0].animate
              .set_fill(RED, opacity=0.75).set_stroke(RED_A, width=2.5)
              for c in range(COLS)],
            run_time=0.6
        )
        hammer_note = Text("← Hammered", font_size=20, color=RED)
        hammer_note.next_to(cells[HAMMER_ROW][COLS - 1][0], RIGHT, buff=0.3)
        self.play(FadeIn(hammer_note), run_time=0.4)

        # Pulse the hammered row 3 times to show it being "hammered"
        for _ in range(3):
            self.play(*[cells[HAMMER_ROW][c][0].animate.set_fill(RED, opacity=1.0)
                        for c in range(COLS)], run_time=0.25)
            self.play(*[cells[HAMMER_ROW][c][0].animate.set_fill(RED, opacity=0.6)
                        for c in range(COLS)], run_time=0.25)

        self.wait(6.8 - 0.6 - 0.4 - 3 * 0.5)   # 4.3 sec remaining

        # "This can physically flip the 1s and 0s in the adjacent rows,
        #  corrupting data or allowing hackers to bypass security privileges."
        # 22 words × 0.4 = 8.8 sec

        # Cells to flip — 3 from Row 1 (above) + 2 from Row 3 (below)
        FLIP_IDX = [(1, 1), (1, 3), (3, 0), (3, 2), (3, 4)]

        # Build flipped-bit labels (BLACK text is readable on YELLOW background)
        new_labels = [
            Text(str(1 - BIT_DATA[r][c]), font_size=20, color=BLACK)
            .move_to(cells[r][c][1])
            for r, c in FLIP_IDX
        ]

        flip_note = Text("← Bit Flips!", font_size=20, color=YELLOW, weight=BOLD)
        flip_note.next_to(cells[1][COLS - 1][0], RIGHT, buff=0.3)

        self.play(
            *[cells[r][c][0].animate
              .set_fill(YELLOW, opacity=0.85).set_stroke(YELLOW_A, width=2.5)
              for r, c in FLIP_IDX],
            *[Transform(cells[r][c][1], new_lbl)
              for (r, c), new_lbl in zip(FLIP_IDX, new_labels)],
            FadeIn(flip_note),
            run_time=1.2
        )
        self.wait(8.8 - 1.2)   # 7.6 sec


# ─────────────────────────────────────────────────────────────────────────────
# Scene 2 — HammingFails
# Script 1:  58 words × 0.4 sec/word = 23.2 sec
# Script 2:  54 words × 0.4 sec/word = 21.6 sec
# ─────────────────────────────────────────────────────────────────────────────
class HammingFails(Scene):
    def construct(self):

        # ═════════════════════════════════════════════════════════════════════
        # SETUP — 7 blocks: 4 data (blue) + 3 parity (dark gray)
        # ═════════════════════════════════════════════════════════════════════

        N    = 7
        SIDE = 0.92
        GAP  = 0.18
        STEP = SIDE + GAP                           # 1.10 units between centers

        BIT_VALUES  = [1, 0, 1, 1, 0, 1, 0]         # D1 D2 D3 D4 | P1 P2 P3
        ORIG_COLORS = [BLUE] * 4 + [DARK_GRAY] * 3

        def make_blocks():
            blks, grp = [], VGroup()
            for i in range(N):
                sq = Square(side_length=SIDE, fill_opacity=0.55)
                sq.set_fill(ORIG_COLORS[i])
                sq.set_stroke(WHITE, width=1.8)
                sq.move_to([(i - (N - 1) / 2) * STEP, 0.3, 0])
                lbl = Text(str(BIT_VALUES[i]), font_size=30, color=WHITE)
                lbl.move_to(sq)
                cell = VGroup(sq, lbl)
                blks.append(cell)
                grp.add(cell)
            return blks, grp

        blocks, block_group = make_blocks()

        # Type tags  D1–D4  |  P1–P3
        type_labels = VGroup(*[
            Text(f"D{i + 1}" if i < 4 else f"P{i - 3}",
                 font_size=18,
                 color=BLUE_B if i < 4 else LIGHT_GRAY)
            .move_to([(i - (N - 1) / 2) * STEP, 0.3 - SIDE / 2 - 0.32, 0])
            for i in range(N)
        ])

        title = Text("[7, 4, 3] Hamming Code", font_size=40, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.4)

        legend_data = VGroup(
            Square(side_length=0.28, fill_opacity=0.65)
            .set_fill(BLUE).set_stroke(WHITE, 1),
            Text("Data bits (4)", font_size=20, color=WHITE),
        ).arrange(RIGHT, buff=0.25)
        legend_parity = VGroup(
            Square(side_length=0.28, fill_opacity=0.65)
            .set_fill(DARK_GRAY).set_stroke(WHITE, 1),
            Text("Parity bits (3)", font_size=20, color=WHITE),
        ).arrange(RIGHT, buff=0.25)
        legend = VGroup(legend_data, legend_parity).arrange(RIGHT, buff=0.7)
        legend.to_edge(DOWN, buff=0.55)

        # ═════════════════════════════════════════════════════════════════════
        # PART 1 — SEC-DED intro: draw blocks, single error, correction
        # ═════════════════════════════════════════════════════════════════════

        # "To fight bit flips, DRAM uses Error Correcting Codes,
        #  specifically SEC-DED Hamming codes."
        # 13 words × 0.4 = 5.2 sec
        self.play(FadeIn(title), run_time=0.6)
        self.play(FadeIn(block_group, lag_ratio=0.1), FadeIn(type_labels), run_time=1.5)
        self.play(FadeIn(legend), run_time=0.4)
        self.wait(5.2 - 0.6 - 1.5 - 0.4)   # 2.7 sec

        # "Before data is stored, it is mathematically encoded with extra parity bits."
        # 12 words × 0.4 = 4.8 sec
        # Pulse the parity blocks to draw the viewer's attention
        self.play(
            *[blocks[i][0].animate.set_fill(GRAY, opacity=0.85) for i in range(4, N)],
            run_time=0.4
        )
        self.play(
            *[blocks[i][0].animate.set_fill(DARK_GRAY, opacity=0.55) for i in range(4, N)],
            run_time=0.4
        )
        self.wait(4.8 - 0.4 - 0.4)   # 4.0 sec

        # "When the data is read back, the system checks these bits."
        # 11 words × 0.4 = 4.4 sec
        self.wait(4.4)

        # "If a single bit has flipped due to normal background radiation,
        #  the SEC-DED code mathematically isolates the error and flips it back."
        # 22 words × 0.4 = 8.8 sec

        ERROR_IDX = 2   # D3: 1 → (flip) → 0, then corrected back to 1

        flipped_lbl = Text(str(1 - BIT_VALUES[ERROR_IDX]), font_size=30, color=WHITE)
        flipped_lbl.move_to(blocks[ERROR_IDX][1])
        error_note = Text("Error!", font_size=22, color=RED)
        error_note.next_to(blocks[ERROR_IDX][0], UP, buff=0.25)

        self.play(
            blocks[ERROR_IDX][0].animate.set_fill(RED, opacity=0.85).set_stroke(RED_A, 2.5),
            Transform(blocks[ERROR_IDX][1], flipped_lbl),
            run_time=0.6
        )
        self.play(FadeIn(error_note), run_time=0.3)
        self.wait(1.5)   # pause — error visible on screen

        corrected_lbl = Text(str(BIT_VALUES[ERROR_IDX]), font_size=30, color=WHITE)
        corrected_lbl.move_to(blocks[ERROR_IDX][1])
        corrected_note = Text("Corrected", font_size=22, color=GREEN)
        corrected_note.next_to(blocks[ERROR_IDX][0], UP, buff=0.25)

        self.play(
            blocks[ERROR_IDX][0].animate.set_fill(GREEN, opacity=0.85).set_stroke(GREEN_A, 2.5),
            Transform(blocks[ERROR_IDX][1], corrected_lbl),
            FadeOut(error_note),
            run_time=0.6
        )
        self.play(FadeIn(corrected_note), run_time=0.3)
        self.wait(8.8 - 0.6 - 0.3 - 1.5 - 0.6 - 0.3)   # 5.5 sec

        # ═════════════════════════════════════════════════════════════════════
        # PART 2 — Multi-bit failure: Rowhammer overwhelms Hamming
        # ═════════════════════════════════════════════════════════════════════

        # Reset all blocks to original colors and bit values
        reset_lbls = [
            Text(str(BIT_VALUES[i]), font_size=30, color=WHITE).move_to(blocks[i][1])
            for i in range(N)
        ]
        self.play(
            *[blocks[i][0].animate
              .set_fill(ORIG_COLORS[i], opacity=0.55).set_stroke(WHITE, 1.8)
              for i in range(N)],
            *[Transform(blocks[i][1], reset_lbls[i]) for i in range(N)],
            FadeOut(corrected_note),
            run_time=0.8
        )

        # "But here is the problem."
        # 5 words × 0.4 = 2.0 sec
        problem_text = Text("But here is the problem.", font_size=34, color=YELLOW, weight=BOLD)
        problem_text.to_edge(DOWN, buff=1.2)
        self.play(FadeOut(legend), FadeIn(problem_text), run_time=0.5)
        self.wait(2.0 - 0.5)   # 1.5 sec

        # "SEC-DED stands for Single Error Correction, Double Error Detection."
        # 9 words × 0.4 = 3.6 sec
        sec_ded_text = Text(
            "SEC-DED = Single Error Correction, Double Error Detection",
            font_size=23, color=WHITE
        )
        sec_ded_text.next_to(block_group, DOWN, buff=0.85)
        self.play(FadeOut(problem_text), FadeIn(sec_ded_text), run_time=0.5)
        self.wait(3.6 - 0.5)   # 3.1 sec

        # "It can only fix one mistake at a time."
        # 9 words × 0.4 = 3.6 sec
        limit_text = Text("Can fix: 1 error only", font_size=24, color=RED_B)
        limit_text.next_to(sec_ded_text, DOWN, buff=0.35)
        self.play(FadeIn(limit_text), run_time=0.4)
        self.wait(3.6 - 0.4)   # 3.2 sec

        # "A Rowhammer attack causes multiple bits to flip simultaneously."
        # 9 words × 0.4 = 3.6 sec
        MULTI_IDX = [0, 2, 3]   # D1, D3, D4 all flip at once
        flip_lbls = [
            Text(str(1 - BIT_VALUES[i]), font_size=30, color=WHITE)
            .move_to(blocks[i][1])
            for i in MULTI_IDX
        ]
        self.play(
            *[blocks[i][0].animate.set_fill(RED, opacity=0.85).set_stroke(RED_A, 2.5)
              for i in MULTI_IDX],
            *[Transform(blocks[i][1], flip_lbls[j]) for j, i in enumerate(MULTI_IDX)],
            run_time=0.7
        )
        multi_note = Text("3 simultaneous bit flips!", font_size=22, color=RED, weight=BOLD)
        multi_note.next_to(block_group, UP, buff=0.3)
        self.play(FadeIn(multi_note), run_time=0.3)
        self.wait(3.6 - 0.7 - 0.3)   # 2.6 sec

        # "The standard Hamming code is instantly overwhelmed,
        #  leaving the system completely compromised."
        # 12 words × 0.4 = 4.8 sec
        x_marks = VGroup(*[
            Text("X", font_size=48, color=RED_D, weight=BOLD).move_to(blocks[i][0])
            for i in range(N)
        ])
        fail_banner = Text("SYSTEM FAILURE", font_size=44, color=RED, weight=BOLD)
        fail_banner.to_edge(DOWN, buff=1.0)

        self.play(
            *[blocks[i][0].animate.set_fill(DARK_GRAY, opacity=0.30).set_stroke(GRAY, 1.0)
              for i in range(N)],
            FadeOut(VGroup(*[blocks[i][1] for i in range(N)])),
            FadeOut(multi_note),
            run_time=0.7
        )
        self.play(FadeIn(x_marks), FadeIn(fail_banner), run_time=0.6)
        self.wait(4.8 - 0.7 - 0.6)   # 3.5 sec

        # "To protect modern DRAM, we need a mathematically stronger shield."
        # 10 words × 0.4 = 4.0 sec
        shield_text = Text(
            "We need a mathematically stronger shield.",
            font_size=30, color=YELLOW_B
        )
        shield_text.to_edge(DOWN, buff=0.5)
        self.play(FadeOut(fail_banner), FadeIn(shield_text), run_time=0.6)
        self.wait(4.0 - 0.6)   # 3.4 sec

        # Fade everything out
        self.play(
            FadeOut(VGroup(
                title, block_group, type_labels,
                sec_ded_text, limit_text, x_marks, shield_text
            )),
            run_time=1.0
        )