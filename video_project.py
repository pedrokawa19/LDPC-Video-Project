from manim import *


# ─────────────────────────────────────────────────────────────────────────────
# Scene 1 — RowhammerIntro
# Jongwook voiceover Part A (title+binary): ~78 words × 0.4 = 31.2 sec
# Jongwook voiceover Part B (DRAM grid):  ~111 words × 0.4 = 44.4 sec
# ─────────────────────────────────────────────────────────────────────────────
class RowhammerIntro(Scene):
    def construct(self):

        # ═════════════════════════════════════════════════════════════════════
        # PART 1 — Title Card + Binary Stream
        # ═════════════════════════════════════════════════════════════════════

        # "We live in a world entirely dependent on digital data."
        # 10 words × 0.4 = 4.0 sec
        # (title visible through first sentence)
        title    = Text("Low Density Parity Check Codes", font_size=64, weight=BOLD)
        subtitle = Text("& their Applications", font_size=38, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.4)
        title_group = VGroup(title, subtitle)

        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle), run_time=0.5)
        self.wait(4.0 - 1.5 - 0.8)   # 1.7 sec remaining

        # "But whether that data is flying through the air as a Wi-Fi signal
        #  or sitting quietly in a server, it is physically vulnerable to noise."
        # 25 words × 0.4 = 10.0 sec
        self.wait(10.0)

        # "This is where coding theory comes in. Coding theory is the
        #  mathematical study of how to add redundancy to data so that we can
        #  detect and correct errors introduced by noise."
        # 33 words × 0.4 = 13.2 sec
        self.wait(13.2)

        # "Today, we focus on a specific failure mode inside modern computers
        #  called Rowhammer."
        # 14 words × 0.4 = 5.6 sec  (Rowhammer label covers this)

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

        # Binary stream is visible during the transition — show briefly
        self.play(FadeIn(bits, lag_ratio=0.04), run_time=1.5)
        self.wait(1.5)   # brief pause on binary stream

        # "Today, we focus on a specific failure mode inside modern computers
        #  called Rowhammer."
        # 14 words × 0.4 = 5.6 sec
        rowhammer_label = Text("Rowhammer", font_size=80, color=RED, weight=BOLD)
        self.play(FadeOut(bits), FadeIn(rowhammer_label), run_time=1.0)
        self.wait(5.6 - 1.0)   # 4.6 sec
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
        #  rows and columns. As manufacturers pack these rows closer together
        #  to increase capacity, a dangerous electrical vulnerability becomes
        #  more prominent."
        # 36 words × 0.4 = 14.4 sec
        self.play(FadeIn(dram_title), Write(row_labels), run_time=1.0)
        self.play(FadeIn(all_cells_vgroup, lag_ratio=0.03), run_time=1.5)
        self.wait(14.4 - 1.0 - 1.5)   # 11.9 sec remaining

        # "If a malicious program repeatedly accesses, or 'hammers,' a specific
        #  row of memory, the electrical charge leaks."
        # 18 words × 0.4 = 7.2 sec

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

        self.wait(7.2 - 0.6 - 0.4 - 3 * 0.5)   # 4.7 sec remaining

        # "This can physically flip the 1s and 0s in the adjacent rows,
        #  corrupting data or allowing hackers to bypass security privileges."
        # 21 words × 0.4 = 8.4 sec

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
        # "Unlike random cosmic-ray bit flips, Rowhammer produces structured
        #  errors — burst errors clustered in nearby memory cells. This matters
        #  because Hamming codes assume random independent errors. Rowhammer
        #  violates this assumption entirely."
        # 8.4 + 37 words × 0.4 = 8.4 + 14.8 = 23.2 sec total for flip section
        self.wait(23.2 - 1.2)   # 22.0 sec


# ─────────────────────────────────────────────────────────────────────────────
# Scene 2 — HammingFails
# Eli voiceover Part A (SEC-DED intro):  ~67 words × 0.4 = 26.8 sec
# Eli voiceover Part B (multi-bit fail): ~118 words × 0.4 = 47.2 sec
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
        #  specifically SEC-DED Hamming codes. Before data is stored, it is
        #  mathematically encoded with extra parity bits."
        # 27 words × 0.4 = 10.8 sec
        self.play(FadeIn(title), run_time=0.6)
        self.play(FadeIn(block_group, lag_ratio=0.1), FadeIn(type_labels), run_time=1.5)
        self.play(FadeIn(legend), run_time=0.4)
        self.wait(10.8 - 0.6 - 1.5 - 0.4)   # 8.3 sec

        # "Before data is stored, it is mathematically encoded with extra parity bits."
        # Already counted above — pulse parity during the same window
        # 0.4 + 0.4 = 0.8 sec for parity pulse
        self.play(
            *[blocks[i][0].animate.set_fill(GRAY, opacity=0.85) for i in range(4, N)],
            run_time=0.4
        )
        self.play(
            *[blocks[i][0].animate.set_fill(DARK_GRAY, opacity=0.55) for i in range(4, N)],
            run_time=0.4
        )

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

        # "But here is the problem. SEC-DED stands for Single Error Correction,
        #  Double Error Detection. It can correct exactly one bit error."
        # 22 words × 0.4 = 8.8 sec
        problem_text = Text("But here is the problem.", font_size=34, color=YELLOW, weight=BOLD)
        problem_text.to_edge(DOWN, buff=1.2)
        self.play(FadeOut(legend), FadeIn(problem_text), run_time=0.5)
        self.wait(2.0 - 0.5)   # show "the problem" briefly (2.0 sec)

        # SEC-DED description appears
        sec_ded_text = Text(
            "SEC-DED = Single Error Correction, Double Error Detection",
            font_size=23, color=WHITE
        )
        sec_ded_text.next_to(block_group, DOWN, buff=0.85)
        self.play(FadeOut(problem_text), FadeIn(sec_ded_text), run_time=0.5)
        self.wait(3.6 - 0.5)   # 3.1 sec  (fills remaining of 8.8-sec window)

        # "It can only fix one mistake at a time. For example, if two bits
        #  flip at once, the parity checks produce a pattern that could
        #  correspond to multiple possible error locations."
        # 35 words × 0.4 = 14.0 sec
        limit_text = Text("Can fix: 1 error only", font_size=24, color=RED_B)
        limit_text.next_to(sec_ded_text, DOWN, buff=0.35)
        self.play(FadeIn(limit_text), run_time=0.4)
        self.wait(14.0 - 0.4)   # 13.6 sec

        # "A Rowhammer attack causes multiple bits to flip simultaneously.
        #  Rowhammer doesn't cause isolated errors; it creates bursts of
        #  multiple bit flips at once, which violates the assumptions that
        #  Hamming codes rely on."
        # 36 words × 0.4 = 14.4 sec
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
        self.wait(14.4 - 0.7 - 0.3)   # 13.4 sec

        # "The standard Hamming code can be instantly overwhelmed, leaving the
        #  system compromised. To protect modern DRAM, we need a mathematically
        #  stronger solution."
        # 24 words × 0.4 = 9.6 sec
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
        self.wait(9.6 - 0.7 - 0.6)   # 8.3 sec

        # "To protect modern DRAM, we need a mathematically stronger shield."
        # Already counted above — shield text visible during same block
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


# ─────────────────────────────────────────────────────────────────────────────
# Scene 3 — LDPCSolution
# Pedro Part 1 (intro/Gallager):      ~79 words × 0.4 = 31.6 sec
# Pedro Part 2 (sparse matrix):       ~90 words × 0.4 = 36.0 sec
# Pedro Part 3 (Tanner graph):        ~75 words × 0.4 = 30.0 sec
# Pedro Part 4 (Rowhammer + IBP):     ~90 words × 0.4 = 36.0 sec
# Pedro Part 5 (belief propagation):  ~88 words × 0.4 = 35.2 sec
# ─────────────────────────────────────────────────────────────────────────────
class LDPCSolution(Scene):
    def construct(self):

        # ─────────────────────────────────────────────────────────────────────
        # Shared Tanner-graph topology (used in Parts 3–5)
        # 7 variable nodes,  3 check nodes
        # Connections mirror the sparse 3×7 matrix shown in Part 2
        # ─────────────────────────────────────────────────────────────────────
        EDGES = [
            (0, 0), (1, 0), (3, 0),          # check 0  → bits 0,1,3
            (1, 1), (2, 1), (4, 1), (5, 1),  # check 1  → bits 1,2,4,5
            (0, 2), (3, 2), (5, 2), (6, 2),  # check 2  → bits 0,3,5,6
        ]
        EDGE_COLORS = [BLACK, RED, BLUE]      # one color per check node

        BIT_VALUES  = [1, 0, 1, 0, 1, 0, 1]

        # ═════════════════════════════════════════════════════════════════════
        # PART 1 — LDPC intro: title + sender/receiver diagram
        # ═════════════════════════════════════════════════════════════════════

        # "To solve the Rowhammer problem, we can replace Hamming codes with
        #  Low-Density Parity-Check codes, or LDPC. Invented by Robert Gallager
        #  at MIT in 1960, these codes were actually ignored for decades because
        #  early computers weren't powerful enough to run them. Today, they are
        #  our best mathematical defense against complex multi-bit errors."
        # 66 words × 0.4 = 26.4 sec for this whole Part 1 block
        ldpc_title = Text("LDPC CODES", font_size=72, color=YELLOW, weight=BOLD)
        ldpc_title.to_edge(UP, buff=0.55)

        subtitle1 = Text("Low-Density Parity-Check", font_size=32, color=WHITE)
        subtitle1.next_to(ldpc_title, DOWN, buff=0.35)

        self.play(Write(ldpc_title), run_time=1.2)
        self.play(FadeIn(subtitle1), run_time=0.6)
        self.wait(8.0 - 1.2 - 0.6)   # 6.2 sec (first sentence settling)

        # "Invented by Robert Gallager at MIT in 1960 ..."
        # Gallager + sender/receiver diagram shown during this window
        gallager = Text("Robert Gallager, MIT, 1960", font_size=26, color=BLUE_B)
        gallager.next_to(subtitle1, DOWN, buff=0.55)

        # Sender: circle head + body line + two arms + two legs (flat 2D person)
        def make_stick_person(color=WHITE):
            head = Circle(radius=0.18, color=color).set_fill(color, opacity=0.5)
            body = Line(UP * 0.18, DOWN * 0.45, color=color)
            arm_l = Line(ORIGIN, LEFT * 0.3 + DOWN * 0.2, color=color)
            arm_r = Line(ORIGIN, RIGHT * 0.3 + DOWN * 0.2, color=color)
            leg_l = Line(DOWN * 0.45, LEFT * 0.22 + DOWN * 0.85, color=color)
            leg_r = Line(DOWN * 0.45, RIGHT * 0.22 + DOWN * 0.85, color=color)
            arm_l.shift(DOWN * 0.15)
            arm_r.shift(DOWN * 0.15)
            grp = VGroup(head, body, arm_l, arm_r, leg_l, leg_r)
            grp[0].move_to(UP * 0.5)
            return grp

        sender   = make_stick_person(BLUE_B).scale(0.9).move_to([-4.5, -0.8, 0])
        receiver = make_stick_person(GREEN_B).scale(0.9).move_to([4.5, -0.8, 0])
        channel  = Line([-3.5, -0.6, 0], [3.5, -0.6, 0], color=WHITE, stroke_width=2.5)
        noise_zap = Text("⚡ noise", font_size=22, color=RED).move_to([0, -0.2, 0])
        sender_lbl   = Text("Sender",   font_size=20, color=BLUE_B).next_to(sender,   DOWN, buff=0.15)
        receiver_lbl = Text("Receiver", font_size=20, color=GREEN_B).next_to(receiver, DOWN, buff=0.15)

        self.play(FadeIn(gallager), run_time=0.5)
        self.play(
            FadeIn(sender), FadeIn(sender_lbl),
            FadeIn(receiver), FadeIn(receiver_lbl),
            Create(channel),
            run_time=1.2
        )
        self.play(FadeIn(noise_zap), run_time=0.4)
        self.wait(11.2 - 0.5 - 1.2 - 0.4)   # 9.1 sec  (covers Gallager + sender/receiver)

        # "Today, they are our best mathematical defense against complex
        #  multi-bit errors."
        # 12 words × 0.4 = 4.8 sec
        defense_text = Text(
            "Best defense against multi-bit errors",
            font_size=27, color=GREEN_B
        ).move_to([0, -2.2, 0])
        self.play(FadeIn(defense_text), run_time=0.5)
        self.wait(4.8 - 0.5)   # 4.3 sec

        self.play(
            FadeOut(VGroup(
                ldpc_title, subtitle1, gallager,
                sender, sender_lbl, receiver, receiver_lbl,
                channel, noise_zap, defense_text
            )),
            run_time=0.8
        )

        # ═════════════════════════════════════════════════════════════════════
        # PART 2 — Sparse matrix + low-density triangle visual
        # ═════════════════════════════════════════════════════════════════════

        # "The secret lies in the name: Low-Density. An LDPC code is defined
        #  by a sparse parity-check matrix. In linear algebra, a sparse matrix
        #  is just a grid filled mostly with zeros, and only a very small number
        #  of ones."
        # 40 words × 0.4 = 16.0 sec
        secret_title = Text("The Secret: Low-Density", font_size=40, color=YELLOW, weight=BOLD)
        secret_title.to_edge(UP, buff=0.45)
        self.play(FadeIn(secret_title), run_time=0.6)
        self.wait(3.2 - 0.6)   # 2.6 sec (first sentence beat)

        # Sparse 3×7 matrix data — matches EDGES topology above
        # Row 0: bits 0,1,3 → cols 0,1,3 = 1; rest = 0
        # Row 1: bits 1,2,4,5 → cols 1,2,4,5 = 1; rest = 0
        # Row 2: bits 0,3,5,6 → cols 0,3,5,6 = 1; rest = 0
        MAT_DATA = [
            [1, 1, 0, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 1, 1],
        ]

        CELL_S = 0.52
        CELL_G = 0.06
        CELL_STEP = CELL_S + CELL_G
        MAT_ROWS, MAT_COLS = 3, 7

        matrix_cells = []
        matrix_vgroup = VGroup()
        for r in range(MAT_ROWS):
            row = []
            for c in range(MAT_COLS):
                sq = Square(side_length=CELL_S, fill_opacity=0.25)
                sq.set_fill(BLUE_D).set_stroke(BLUE_B, 1.2)
                sq.move_to([
                    -4.8 + c * CELL_STEP,
                    1.6 - r * CELL_STEP,
                    0
                ])
                val = MAT_DATA[r][c]
                lbl = Text(str(val), font_size=20,
                           color=YELLOW if val == 1 else WHITE)
                lbl.move_to(sq)
                cell = VGroup(sq, lbl)
                row.append(cell)
                matrix_vgroup.add(cell)
            matrix_cells.append(row)

        mat_bracket_l = Text("[", font_size=88, color=WHITE).move_to([-5.35, 1.1, 0])
        mat_bracket_r = Text("]", font_size=88, color=WHITE).move_to([-0.25, 1.1, 0])
        mat_label = Text("H  (parity-check matrix)", font_size=23, color=GRAY)
        mat_label.move_to([-2.8, -0.55, 0])

        # "An LDPC code is defined by a sparse parity-check matrix."
        # Matrix appears during this window
        self.play(
            FadeIn(mat_bracket_l), FadeIn(mat_bracket_r),
            FadeIn(matrix_vgroup, lag_ratio=0.03),
            run_time=1.5
        )
        self.play(FadeIn(mat_label), run_time=0.4)
        self.wait(4.4 - 1.5 - 0.4)   # 2.5 sec

        # "In linear algebra, a sparse matrix is just a grid filled mostly with
        #  zeros, and only a very small number of ones. The columns of this
        #  matrix represent our message bits, and the rows represent our parity
        #  check equations. Because the matrix is sparse, each parity equation
        #  only checks a very small, specific handful of bits."
        # Already started above; 1s highlight covers the visual
        # "The columns represent message bits, and the rows represent parity
        #  check equations."
        # 12 words × 0.4 = 4.8 sec  — highlight 1s during this
        # "Because the matrix is sparse, each parity equation only checks a
        #  very small, specific handful of bits."
        # 17 words × 0.4 = 6.8 sec  — triangle visual
        self.play(
            *[cell[0].animate.set_fill(YELLOW, opacity=0.6) for cell in one_cells],
            run_time=0.8
        )
        self.wait(8.4 - 0.8)   # 7.6 sec  (1s highlighted)

        # "The columns represent message bits, and the rows represent parity
        #  check equations. Because each equation only depends on a few bits,
        #  each error creates only a small number of inconsistencies, making
        #  it much easier to isolate."
        # 38 words × 0.4 = 15.2 sec (column/row arrows + triangle visual)
        self.play(GrowArrow(col_arrow), FadeIn(col_note), run_time=0.5)
        self.play(GrowArrow(row_arrow), FadeIn(row_note), run_time=0.5)
        self.wait(4.8 - 0.5 - 0.5)   # 3.8 sec  (columns+rows beat)

        # "Because the matrix is sparse..." — triangle visual covers remainder
        # 7 tiny bit labels
        TINY_BIT_X = [1.5 + i * 0.72 for i in range(7)]
        TINY_BIT_Y = 2.0
        tiny_bits = VGroup(*[
            Text(str(BIT_VALUES[i]), font_size=20, color=WHITE)
            .move_to([TINY_BIT_X[i], TINY_BIT_Y, 0])
            for i in range(7)
        ])

        # 4 check squares below
        CHECK_X = [2.22 + i * 1.44 for i in range(4)]
        CHECK_Y = 0.3
        check_squares = VGroup(*[
            Square(side_length=0.36, fill_opacity=1.0)
            .set_fill(BLACK).set_stroke(WHITE, 1.5)
            .move_to([CHECK_X[i], CHECK_Y, 0])
            for i in range(4)
        ])

        # Semi-transparent grey triangles from each check up over its bits
        tri_polys = VGroup()
        for i, cx in enumerate(CHECK_X):
            spread = 1.1
            top_l = [cx - spread, TINY_BIT_Y - 0.15, 0]
            top_r = [cx + spread, TINY_BIT_Y - 0.15, 0]
            bot   = [cx, CHECK_Y + 0.18, 0]
            tri = Polygon(top_l, top_r, bot,
                          fill_color=LIGHT_GRAY, fill_opacity=0.18,
                          stroke_color=LIGHT_GRAY, stroke_width=0.8)
            tri_polys.add(tri)

        density_label = Text("Low Density: each check sees only a few bits",
                             font_size=20, color=GREEN_B).move_to([3.2, -0.7, 0])

        self.play(FadeIn(tiny_bits), FadeIn(check_squares), run_time=0.6)
        self.play(FadeIn(tri_polys), run_time=0.6)
        self.play(FadeIn(density_label), run_time=0.4)
        self.wait(15.2 - (0.5 + 0.5 + 3.8) - 0.6 - 0.6 - 0.4)   # 9.3 sec

        self.play(
            FadeOut(VGroup(
                secret_title, matrix_vgroup, mat_bracket_l, mat_bracket_r,
                mat_label, col_arrow, col_note, row_arrow, row_note,
                tiny_bits, check_squares, tri_polys, density_label,
            )),
            run_time=0.8
        )

        # ═════════════════════════════════════════════════════════════════════
        # PART 3 — Build Tanner Graph
        # ═════════════════════════════════════════════════════════════════════

        # "LDPC codes can correct multiple simultaneous errors because each
        #  bit participates in many independent, sparse constraints, allowing
        #  the decoder to accumulate consistent evidence about which bits are
        #  wrong. To prove why this is so powerful against Rowhammer, we can
        #  visualize this matrix as a bipartite graph, called a Tanner Graph."
        # 62 words × 0.4 = 24.8 sec  (Tanner graph build covers this)

        tanner_title = Text("Tanner Graph", font_size=44, color=YELLOW, weight=BOLD)
        tanner_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(tanner_title), run_time=0.6)

        # 7 variable nodes — short horizontal tick marks
        VAR_Y  = 1.4
        VAR_X  = [(i - 3) * 1.55 for i in range(7)]
        var_ticks = VGroup(*[
            Line([-0.28, 0, 0], [0.28, 0, 0], color=WHITE, stroke_width=2.5)
            .move_to([VAR_X[i], VAR_Y, 0])
            for i in range(7)
        ])

        # Bit labels above ticks: first 4 black/white, last 3 blue
        var_labels = VGroup(*[
            Text(str(BIT_VALUES[i]), font_size=28,
                 color=WHITE if i < 4 else BLUE_B)
            .move_to([VAR_X[i], VAR_Y + 0.52, 0])
            for i in range(7)
        ])

        var_type_labels = VGroup(*[
            Text("m" if i < 4 else "p", font_size=14, color=YELLOW)
            .move_to([VAR_X[i], VAR_Y - 0.35, 0])
            for i in range(7)
        ])

        # 3 check nodes — solid squares
        CHK_Y  = -1.5
        CHK_X  = [-3.1, 0.0, 3.1]
        check_nodes = VGroup(*[
            Square(side_length=0.50, fill_opacity=1.0)
            .set_fill(BLACK).set_stroke(WHITE, 2.0)
            .move_to([CHK_X[k], CHK_Y, 0])
            for k in range(3)
        ])
        check_node_labels = VGroup(*[
            Text(f"c{k}", font_size=18, color=WHITE)
            .move_to([CHK_X[k], CHK_Y - 0.55, 0])
            for k in range(3)
        ])

        # Edges — draw with color matching their check group
        edge_lines = []
        for (v, k) in EDGES:
            line = Line(
                [VAR_X[v], VAR_Y - 0.0, 0],
                [CHK_X[k], CHK_Y + 0.25, 0],
                color=EDGE_COLORS[k],
                stroke_width=1.8
            )
            edge_lines.append(line)
        edge_group = VGroup(*edge_lines)

        self.play(FadeIn(var_ticks), FadeIn(var_labels), FadeIn(var_type_labels), run_time=1.0)
        self.play(FadeIn(check_nodes), FadeIn(check_node_labels), run_time=0.8)
        self.play(Create(edge_group, lag_ratio=0.05), run_time=1.5)
        self.wait(9.2 - 0.6 - 1.0 - 0.8 - 1.5)   # 5.3 sec  (first beat—Tanner title + nodes appear)

        # "The circles at the top are the bits of our data."
        # 11 words × 0.4 = 4.4 sec
        bit_arrow = Arrow(start=[0, 2.55, 0], end=[0, VAR_Y + 0.7, 0],
                          color=WHITE, buff=0.05, stroke_width=2.0)
        bit_note  = Text("Variable nodes (data bits)", font_size=22, color=WHITE)
        bit_note.move_to([0, 2.9, 0])
        self.play(FadeIn(bit_note), GrowArrow(bit_arrow), run_time=0.6)
        self.wait(4.4 - 0.6)   # 3.8 sec

        # "The squares at the bottom are our parity checks. The lines
        #  connecting them are exactly where the ones were in our sparse matrix."
        # 23 words × 0.4 = 9.2 sec
        chk_arrow = Arrow(start=[0, -2.55, 0], end=[0, CHK_Y - 0.3, 0],
                          color=WHITE, buff=0.05, stroke_width=2.0)
        chk_note  = Text("Check nodes (parity eqs.)", font_size=22, color=WHITE)
        chk_note.move_to([0, -2.9, 0])
        self.play(FadeIn(chk_note), GrowArrow(chk_arrow), run_time=0.6)
        self.wait(9.2 - 0.6)   # 8.6 sec

        self.play(
            FadeOut(bit_note), FadeOut(bit_arrow),
            FadeOut(chk_note), FadeOut(chk_arrow),
            run_time=0.5
        )

        # ═════════════════════════════════════════════════════════════════════
        # PART 4 — Rowhammer attack: question marks + upward belief messages
        # ═════════════════════════════════════════════════════════════════════

        # "When a Rowhammer attack flips multiple bits, the LDPC decoder
        #  doesn't just crash like a Hamming code. Instead, it uses an
        #  algorithm called Iterative Belief Propagation. It's an iterative
        #  inference process: each parity check provides a local constraint,
        #  and the decoder repeatedly aggregates these constraints to estimate
        #  the most likely value of each bit."
        # 61 words × 0.4 = 24.4 sec

        ATTACK_IDX = [1, 2, 4]   # bits 1, 2, 4 get attacked

        q_marks = VGroup(*[
            Text("?", font_size=32, color=RED, weight=BOLD)
            .move_to([VAR_X[i], VAR_Y + 0.52, 0])
            for i in ATTACK_IDX
        ])

        # Replace attacked bit labels with red "?"
        attacked_labels = VGroup(*[var_labels[i] for i in ATTACK_IDX])
        self.play(
            FadeOut(attacked_labels),
            FadeIn(q_marks),
            run_time=0.6
        )
        self.wait(7.6 - 0.6)   # 7.0 sec  (attack shown)

        # "Instead, it uses Iterative Belief Propagation..."
        ibp_text = Text("Iterative Belief Propagation", font_size=30, color=YELLOW)
        ibp_text.move_to([0, -3.4, 0])
        self.play(FadeIn(ibp_text), run_time=0.5)
        self.wait(4.0 - 0.5)   # 3.5 sec

        # "You can think of this like a network of voters..."
        telephone_text = Text("A network of voters", font_size=24, color=WHITE)
        telephone_text.next_to(ibp_text, DOWN, buff=0.25)
        self.play(FadeIn(telephone_text), run_time=0.4)

        # "The check nodes look at bits and send messages upward."
        # Belief dot animation — dots travel UP from checks to variable nodes
        def make_dot(start, end, color=YELLOW):
            dot = Dot(point=start, radius=0.09, color=color)
            return dot, MoveAlongPath(
                dot,
                Line(start, end),
                run_time=0.9,
                rate_func=linear
            )

        # Only edges touching attacked variable nodes
        attack_edges_up = [
            (v, k) for v, k in EDGES if v in ATTACK_IDX
        ]
        dots_up = []
        anims_up = []
        for v, k in attack_edges_up:
            start = np.array([CHK_X[k], CHK_Y + 0.25, 0])
            end   = np.array([VAR_X[v], VAR_Y,         0])
            dot, anim = make_dot(start, end, color=YELLOW)
            dots_up.append(dot)
            anims_up.append(anim)

        dot_group_up = VGroup(*dots_up)
        self.add(dot_group_up)
        self.play(*anims_up)
        self.remove(dot_group_up)
        # "Over multiple rounds, these local updates reinforce each other,
        #  and the system gradually converges to a globally consistent solution.
        #  Because each parity check only involves a small number of bits,
        #  errors remain localized rather than contaminating the entire system."
        # 40 words × 0.4 = 16.0 sec — remaining Part 4 time after IBP intro
        self.wait(16.0 - 0.4 - 0.9)   # 14.7 sec

        self.play(FadeOut(ibp_text), FadeOut(telephone_text), run_time=0.4)

        # ═════════════════════════════════════════════════════════════════════
        # PART 5 — Belief propagation iterations → correction
        # ═════════════════════════════════════════════════════════════════════

        # "The bits receive messages from all their connected checks, update
        #  their own probability of being a 1 or a 0, and send that updated
        #  belief back down to the checks. They pass these probabilities back
        #  and forth iteratively."
        # 43 words × 0.4 = 17.2 sec

        # Edges touching attacked nodes for DOWN pass (var → check)
        attack_edges_down = [(v, k) for v, k in EDGES if v in ATTACK_IDX]

        def one_pass_up():
            dots, anims = [], []
            for v, k in attack_edges_up:
                start = np.array([CHK_X[k], CHK_Y + 0.25, 0])
                end   = np.array([VAR_X[v], VAR_Y,         0])
                dot, anim = make_dot(start, end, YELLOW)
                dots.append(dot)
                anims.append(anim)
            grp = VGroup(*dots)
            return grp, anims

        def one_pass_down():
            dots, anims = [], []
            for v, k in attack_edges_down:
                start = np.array([VAR_X[v], VAR_Y,         0])
                end   = np.array([CHK_X[k], CHK_Y + 0.25, 0])
                dot, anim = make_dot(start, end, YELLOW)
                dots.append(dot)
                anims.append(anim)
            grp = VGroup(*dots)
            return grp, anims

        # Iteration 1: down then up
        grp_d1, anims_d1 = one_pass_down()
        self.add(grp_d1)
        self.play(*anims_d1)
        self.remove(grp_d1)

        grp_u1, anims_u1 = one_pass_up()
        self.add(grp_u1)
        self.play(*anims_u1)
        self.remove(grp_u1)

        self.wait(13.2 - 0.9 - 0.9)   # 11.4 sec  (pause after iteration 1 — long belief exchange)

        # "They pass these probabilities back and forth iteratively. Because
        #  the connections are sparse, the errors don't easily spread."
        # ~19 words × 0.4 = 7.6 sec

        # Iteration 2
        grp_d2, anims_d2 = one_pass_down()
        self.add(grp_d2)
        self.play(*anims_d2)
        self.remove(grp_d2)

        grp_u2, anims_u2 = one_pass_up()
        self.add(grp_u2)
        self.play(*anims_u2)
        self.remove(grp_u2)

        self.wait(7.6 - 0.9 - 0.9)   # 5.8 sec  (pause after iteration 2)

        # "Because the connections are sparse, the errors don't easily spread
        #  to other equations. Within just a few iterations, the network
        #  reaches a mathematical consensus, isolating and correcting the
        #  multi-bit Rowhammer errors."
        # 36 words × 0.4 = 14.4 sec
        sparse_note = Text("Sparse connections = errors stay isolated",
                           font_size=24, color=GREEN_B)
        sparse_note.move_to([0, -3.4, 0])
        self.play(FadeIn(sparse_note), run_time=0.5)
        self.wait(5.6 - 0.5)   # 5.1 sec  (sparse note beat)

        # "Within just a few iterations, the network reaches a mathematical
        #  consensus, isolating and correcting the multi-bit Rowhammer errors.
        #  Of course, this process is not perfect. Designing LDPC codes is
        #  a careful balance between sparsity, redundancy, and performance."
        # 44 words × 0.4 = 17.6 sec

        # Iteration 3 (final) then correction
        grp_d3, anims_d3 = one_pass_down()
        self.add(grp_d3)
        self.play(*anims_d3)
        self.remove(grp_d3)

        grp_u3, anims_u3 = one_pass_up()
        self.add(grp_u3)
        self.play(*anims_u3)
        self.remove(grp_u3)

        # Replace "?" marks with corrected bit values in GREEN
        corrected_labels = VGroup(*[
            Text(str(BIT_VALUES[i]), font_size=28, color=GREEN)
            .move_to([VAR_X[i], VAR_Y + 0.52, 0])
            for i in ATTACK_IDX
        ])
        self.play(FadeOut(q_marks), FadeIn(corrected_labels), run_time=0.6)
        self.wait(17.6 - 0.9 - 0.9 - 0.6)   # 15.2 sec

        # Fade everything out
        self.play(
            FadeOut(VGroup(
                tanner_title, var_ticks, var_labels, var_type_labels,
                check_nodes, check_node_labels, edge_group,
                corrected_labels, sparse_note
            )),
            run_time=1.0
        )


# ─────────────────────────────────────────────────────────────────────────────
# Scene 4 — RealWorld
# Pedro Part 1 (DRAM latency):    ~85 words × 0.4 = 34.0 sec
# Pedro Part 2 (SSD + industries): ~110 words × 0.4 = 44.0 sec
# Pedro Part 3 (5G/Wi-Fi/Sat):    ~72 words  × 0.4 = 28.8 sec
# Pedro Part 4 (future + refs):   ~92 words  × 0.4 = 36.8 sec
# ─────────────────────────────────────────────────────────────────────────────
class RealWorld(Scene):
    def construct(self):

        # ═════════════════════════════════════════════════════════════════════
        # PART 1 — The DRAM latency problem: clock visual
        # ═════════════════════════════════════════════════════════════════════

        # "If LDPC codes are so powerful, why aren't they already in our
        #  computer's DRAM? It comes down to speed and hardware complexity.
        #  DRAM operates under extremely tight latency constraints, often on
        #  the order of tens of nanoseconds."
        # 40 words × 0.4 = 16.0 sec
        question = Text(
            "If LDPC is so powerful…\nwhy not use it in DRAM?",
            font_size=40, color=WHITE, line_spacing=1.3
        ).to_edge(UP, buff=0.6)
        self.play(Write(question), run_time=1.4)
        self.wait(8.4 - 1.4)   # 7.0 sec (first question)

        # "It comes down to speed and hardware complexity."
        # 8 words × 0.4 = 3.2 sec
        speed_text = Text("It comes down to speed.", font_size=34, color=YELLOW)
        speed_text.next_to(question, DOWN, buff=0.55)
        self.play(FadeIn(speed_text), run_time=0.5)
        self.wait(3.2 - 0.5)   # 2.7 sec

        # "Hamming decoding can be done in essentially a single step using
        #  simple logic. But LDPC decoding requires multiple rounds of message
        #  passing, additional memory access, and more complex circuitry.
        #  This increases both latency and energy consumption."
        # 38 words × 0.4 = 15.2 sec  (latency eq + clock covers this)
        latency_eq = Text("Iterative Decoding  =  High Latency",
                          font_size=34, color=RED_B)
        latency_eq.move_to([0, 0.3, 0])
        self.play(FadeIn(latency_eq), run_time=0.6)
        self.wait(4.0 - 0.6)   # 3.4 sec  (equation settled)

        # "This increases both latency and energy consumption, making it
        #  historically impractical for main memory."
        # Clock spinning covers this window — 16.0 - (8.4 + 3.2 + 4.0) = 0.4 sec budget
        # Total Part 1 = 34.0 sec: 8.4 + 3.2 + 4.0 + 15.2 (clock) + misc = ~34 sec
        # Clock face (circle + 12 tick lines + hour/minute hands that spin)
        clock_face   = Circle(radius=0.85, color=WHITE, stroke_width=2.5)
        clock_face.move_to([0, -1.9, 0])
        clock_center = Dot(point=clock_face.get_center(), radius=0.07, color=WHITE)

        ticks = VGroup()
        for n in range(12):
            angle = n * TAU / 12
            inner = clock_face.get_center() + 0.66 * np.array([np.sin(angle), np.cos(angle), 0])
            outer = clock_face.get_center() + 0.82 * np.array([np.sin(angle), np.cos(angle), 0])
            ticks.add(Line(inner, outer, color=WHITE, stroke_width=1.5))

        hour_hand = Arrow(
            start=clock_face.get_center(),
            end=clock_face.get_center() + np.array([0, 0.48, 0]),
            color=WHITE, buff=0, stroke_width=3.5, max_tip_length_to_length_ratio=0.2
        )
        minute_hand = Arrow(
            start=clock_face.get_center(),
            end=clock_face.get_center() + np.array([0, 0.70, 0]),
            color=YELLOW, buff=0, stroke_width=2.5, max_tip_length_to_length_ratio=0.15
        )
        nano_label = Text("needs: nanoseconds ⚡", font_size=22, color=RED)
        nano_label.next_to(clock_face, DOWN, buff=0.3)

        self.play(
            FadeIn(clock_face), FadeIn(clock_center),
            FadeIn(ticks), FadeIn(hour_hand), FadeIn(minute_hand),
            run_time=0.5
        )
        # Spin the minute hand 4 full rotations to show speed
        self.play(
            Rotating(minute_hand, angle=4 * TAU,
                     about_point=clock_face.get_center(), run_time=3.5, rate_func=linear),
            Rotating(hour_hand,   angle=TAU / 3,
                     about_point=clock_face.get_center(), run_time=3.5, rate_func=linear),
        )
        self.play(FadeIn(nano_label), run_time=0.4)
        self.wait(15.2 - 0.5 - 3.5 - 0.4)   # 10.8 sec  (clock + latency window)

        self.play(
            FadeOut(VGroup(
                question, speed_text, latency_eq,
                clock_face, clock_center, ticks,
                hour_hand, minute_hand, nano_label
            )),
            run_time=0.8
        )

        # ═════════════════════════════════════════════════════════════════════
        # PART 2 — SSD health bar + micro Tanner graph overlay
        # ═════════════════════════════════════════════════════════════════════

        # "However, LDPC is currently dominating almost every other industry.
        #  In 5G cellular networks, signals travel through noisy environments
        #  with interference from many sources, often causing multiple
        #  simultaneous errors."
        # Part 2 total: ~110 words × 0.4 = 44.0 sec
        ssd_title = Text("SSDs: Flash Memory", font_size=42, color=YELLOW, weight=BOLD)
        ssd_title.to_edge(UP, buff=0.45)
        self.play(FadeIn(ssd_title), run_time=0.6)

        # Stylized microchip square
        chip_body = Square(side_length=2.2, fill_opacity=0.25)
        chip_body.set_fill(BLUE_D).set_stroke(BLUE_B, 2.5)
        chip_body.move_to([0, -0.4, 0])
        chip_label = Text("SSD", font_size=30, color=WHITE, weight=BOLD)
        chip_label.move_to(chip_body)

        # Pin lines on all four sides
        pins = VGroup()
        for side, direction in [
            (chip_body.get_top(),    UP),
            (chip_body.get_bottom(), DOWN),
            (chip_body.get_left(),   LEFT),
            (chip_body.get_right(),  RIGHT),
        ]:
            for offset in [-0.55, 0, 0.55]:
                perp = np.array([direction[1], direction[0], 0])
                start = side + perp * offset
                end   = start + direction * 0.35
                pins.add(Line(start, end, color=BLUE_B, stroke_width=2.0))

        chip_group = VGroup(chip_body, chip_label, pins)
        self.play(FadeIn(chip_group, lag_ratio=0.05), run_time=0.9)
        self.wait(5.6 - 0.6 - 0.9)   # 4.1 sec  (industry intro)

        # "Take the Solid-State Drive inside your computer right now.
        #  Flash memory physically degrades over time."
        # 14 words × 0.4 = 5.6 sec

        self.wait(5.6)

        # "The silicon oxide layers wear out, causing severe multi-bit errors."
        # 10 words × 0.4 = 4.0 sec  (bar depleting covers this)

        # Health bar — starts full green, depletes to red
        BAR_W, BAR_H = 3.2, 0.38
        BAR_POS = chip_body.get_top() + UP * 0.8

        bar_bg = Rectangle(width=BAR_W, height=BAR_H,
                           fill_opacity=0.25, fill_color=DARK_GRAY,
                           stroke_color=WHITE, stroke_width=1.5)
        bar_bg.move_to(BAR_POS)
        bar_fill = Rectangle(width=BAR_W, height=BAR_H,
                             fill_opacity=0.85, fill_color=GREEN,
                             stroke_color=GREEN, stroke_width=0)
        bar_fill.move_to(BAR_POS)
        bar_label = Text("Drive Health", font_size=18, color=WHITE)
        bar_label.next_to(bar_bg, LEFT, buff=0.2)

        self.play(FadeIn(bar_bg), FadeIn(bar_fill), FadeIn(bar_label), run_time=0.5)

        # Deplete bar slowly to ~20% (red zone) while describing flash degradation
        # "The silicon oxide layers wear out, causing severe multi-bit errors."
        # 10 words × 0.4 = 4.0 sec  (depletion animation = 2.8 sec, rest waits)
        bar_depleted = Rectangle(
            width=BAR_W * 0.18, height=BAR_H,
            fill_opacity=0.85, fill_color=RED,
            stroke_color=RED, stroke_width=0
        )
        bar_depleted.move_to(BAR_POS + LEFT * (BAR_W * (1 - 0.18) / 2))
        self.play(
            Transform(bar_fill, bar_depleted),
            run_time=2.8
        )
        self.wait(4.0 - 0.5 - 2.8)   # 0.7 sec  (bar fully depleted)

        # "Older drives used simpler codes, but modern SSDs survive because
        #  of LDPC. By using soft-decision decoding, LDPC extends the lifespan
        #  of your drive by years, keeping your files from corruption.
        #  In Wi-Fi, signals bounce off walls creating multipath interference.
        #  In flash memory, storage cells degrade causing multiple nearby bits
        #  to fail together. In all these cases, the error model is complex
        #  and structured — exactly where LDPC excels."
        # ~66 words × 0.4 = 26.4 sec  (Tanner overlay + bar recovery + industry bullets)

        # Overlay faint Tanner graph on the chip
        mini_var_x = [-0.7, -0.23, 0.23, 0.7]
        mini_var_y = chip_body.get_top()[1] - 0.35
        mini_chk_x = [-0.47, 0.47]
        mini_chk_y = chip_body.get_bottom()[1] + 0.35

        mini_var_nodes = VGroup(*[
            Circle(radius=0.10, fill_opacity=0.5, fill_color=YELLOW, stroke_color=YELLOW, stroke_width=1.0)
            .move_to([x, mini_var_y, 0])
            for x in mini_var_x
        ])
        mini_chk_nodes = VGroup(*[
            Square(side_length=0.18, fill_opacity=0.5, fill_color=WHITE, stroke_color=WHITE, stroke_width=1.0)
            .move_to([x, mini_chk_y, 0])
            for x in mini_chk_x
        ])
        mini_edges = VGroup(*[
            Line([mini_var_x[v], mini_var_y, 0],
                 [mini_chk_x[k], mini_chk_y, 0],
                 color=YELLOW, stroke_opacity=0.5, stroke_width=1.0)
            for v, k in [(0,0),(1,0),(2,0),(1,1),(2,1),(3,1)]
        ])
        mini_tanner = VGroup(mini_edges, mini_var_nodes, mini_chk_nodes)
        self.play(FadeIn(mini_tanner, lag_ratio=0.05), run_time=0.6)

        # Pulse the Tanner graph twice while describing LDPC benefit
        for _ in range(2):
            self.play(mini_tanner.animate.set_opacity(1.0), run_time=0.3)
            self.play(mini_tanner.animate.set_opacity(0.45), run_time=0.3)

        self.wait(10.4 - 0.6 - 2 * 0.6)   # 8.6 sec  (industry bullets)

        # "By using soft-decision decoding—those probabilities we passed back
        #  and forth—LDPC extends the lifespan of your drive by years, keeping
        #  your files from corruption."
        # 26 words × 0.4 = 10.4 sec

        # Stabilize health bar → green
        bar_stable = Rectangle(
            width=BAR_W * 0.75, height=BAR_H,
            fill_opacity=0.85, fill_color=GREEN,
            stroke_color=GREEN, stroke_width=0
        )
        bar_stable.move_to(BAR_POS + LEFT * (BAR_W * (1 - 0.75) / 2))
        extend_label = Text("Lifespan extended!", font_size=19, color=GREEN)
        extend_label.next_to(bar_bg, RIGHT, buff=0.2)
        self.play(Transform(bar_fill, bar_stable), run_time=1.2)
        self.play(FadeIn(extend_label), run_time=0.4)
        self.wait(26.4 - (0.7 + 2.8 + 0.7) - (0.6 + 2 * 0.6 + 8.6) - 1.2 - 0.4)   # ~9.4 sec

        self.play(
            FadeOut(VGroup(
                ssd_title, chip_group, bar_bg, bar_fill, bar_label,
                mini_tanner, extend_label
            )),
            run_time=0.8
        )

        # ═════════════════════════════════════════════════════════════════════
        # PART 3 — 5G / Wi-Fi / Satellite + Shannon Limit graph
        # ═════════════════════════════════════════════════════════════════════

        # "It is also the official error correction standard for 5G cellular
        #  networks, Wi-Fi 6, and satellite broadcasting."
        # 18 words × 0.4 = 7.2 sec
        wireless_title = Text("5G · Wi-Fi 6 · Satellite", font_size=42, color=YELLOW, weight=BOLD)
        wireless_title.to_edge(UP, buff=0.45)
        self.play(FadeIn(wireless_title), run_time=0.6)

        # ── 5G Cell Tower (left) ──────────────────────────────────────────────
        t_x = -4.2
        tower_mast     = Line([t_x, -2.6, 0], [t_x,  0.5, 0], color=WHITE, stroke_width=3.0)
        tower_base_l   = Line([t_x - 0.55, -2.6, 0], [t_x, -2.6, 0], color=WHITE, stroke_width=3.0)
        tower_base_r   = Line([t_x + 0.55, -2.6, 0], [t_x, -2.6, 0], color=WHITE, stroke_width=3.0)
        tower_sup_l    = Line([t_x - 0.55, -1.8, 0], [t_x, -2.6, 0], color=WHITE, stroke_width=1.5)
        tower_sup_r    = Line([t_x + 0.55, -1.8, 0], [t_x, -2.6, 0], color=WHITE, stroke_width=1.5)
        tower_cross    = Line([t_x - 0.4,  0.1, 0],  [t_x + 0.4, 0.1, 0], color=WHITE, stroke_width=2.0)
        tower = VGroup(tower_mast, tower_base_l, tower_base_r,
                       tower_sup_l, tower_sup_r, tower_cross)
        tower_lbl = Text("5G", font_size=20, color=BLUE_B, weight=BOLD)
        tower_lbl.next_to(tower_cross, UP, buff=0.15)

        arc_center_t = np.array([t_x, 0.5, 0])
        tower_arcs = VGroup()
        for r, op in [(0.5, 0.9), (1.0, 0.6), (1.6, 0.35)]:
            arc = Arc(radius=r, angle=PI * 0.75, start_angle=PI * 0.625,
                      color=BLUE_B, stroke_width=2.2, stroke_opacity=op)
            arc.move_arc_center_to(arc_center_t)
            tower_arcs.add(arc)

        # ── Wi-Fi Router (center) ─────────────────────────────────────────────
        r_x = 0.0
        router_body = Rectangle(width=1.05, height=0.42,
                                fill_opacity=0.55, fill_color=DARK_GRAY,
                                stroke_color=WHITE, stroke_width=1.8)
        router_body.move_to([r_x, -1.6, 0])
        # Three antennas
        router_ant = VGroup(
            Line([r_x - 0.32, -1.39, 0], [r_x - 0.38, -0.72, 0], color=WHITE, stroke_width=2.0),
            Line([r_x,        -1.39, 0], [r_x,         -0.68, 0], color=WHITE, stroke_width=2.0),
            Line([r_x + 0.32, -1.39, 0], [r_x + 0.38, -0.72, 0], color=WHITE, stroke_width=2.0),
        )
        router_base = Line([r_x - 0.2, -1.81, 0], [r_x + 0.2, -1.81, 0], color=WHITE, stroke_width=1.5)
        router_lbl = Text("Wi-Fi 6", font_size=20, color=YELLOW)
        router_lbl.next_to(router_body, DOWN, buff=0.22)
        router = VGroup(router_body, router_ant, router_base)

        arc_center_r = np.array([r_x, -0.65, 0])
        router_arcs = VGroup()
        for r, op in [(0.42, 0.9), (0.80, 0.6), (1.22, 0.35)]:
            arc = Arc(radius=r, angle=PI * 0.75, start_angle=PI * 0.625,
                      color=YELLOW, stroke_width=2.0, stroke_opacity=op)
            arc.move_arc_center_to(arc_center_r)
            router_arcs.add(arc)

        # ── Satellite (right) ─────────────────────────────────────────────────
        s_x = 3.8
        sat_body = Rectangle(width=0.55, height=0.38,
                             fill_opacity=0.6, fill_color=DARK_GRAY,
                             stroke_color=WHITE, stroke_width=1.8)
        sat_body.move_to([s_x, 0.5, 0])
        # Solar panels: rectangles attached left + right
        panel_l = Rectangle(width=0.62, height=0.22,
                             fill_opacity=0.5, fill_color=BLUE_D,
                             stroke_color=BLUE_B, stroke_width=1.2)
        panel_l.next_to(sat_body, LEFT, buff=0.05)
        panel_r = Rectangle(width=0.62, height=0.22,
                             fill_opacity=0.5, fill_color=BLUE_D,
                             stroke_color=BLUE_B, stroke_width=1.2)
        panel_r.next_to(sat_body, RIGHT, buff=0.05)
        # Dish (small arc pointing downward)
        dish = Arc(radius=0.22, angle=PI, start_angle=0,
                   color=WHITE, stroke_width=2.0)
        dish.move_to(sat_body.get_bottom() + DOWN * 0.22)
        dish_stem = Line(sat_body.get_bottom(), dish.get_top(), color=WHITE, stroke_width=1.5)
        satellite = VGroup(sat_body, panel_l, panel_r, dish, dish_stem)
        sat_lbl = Text("Satellite", font_size=20, color=GREEN_B)
        sat_lbl.next_to(satellite, DOWN, buff=0.55)

        # Downlink signal lines from satellite
        sat_signals = VGroup(*[
            DashedLine(
                sat_body.get_bottom() + RIGHT * dx * 0.15,
                sat_body.get_bottom() + RIGHT * dx * 0.15 + DOWN * 1.3,
                color=GREEN_B, stroke_width=1.5, dash_length=0.12, stroke_opacity=0.7
            )
            for dx in [-1, 0, 1]
        ])

        # "When sending data through the air, you are fighting against intense
        #  background noise and interference."
        # 16 words × 0.4 = 6.4 sec
        noise_label = Text("⚡ noise + interference", font_size=22, color=RED)
        noise_label.to_edge(DOWN, buff=0.55)

        # \"It is also the official error correction standard for 5G cellular
        #  networks, Wi-Fi 6, and satellite broadcasting.\"
        # 18 words × 0.4 = 7.2 sec  (devices appear one by one)\n
        # Bring all three devices in one by one
        self.play(Create(tower), FadeIn(tower_lbl), run_time=0.7)
        self.play(LaggedStart(*[Create(a) for a in tower_arcs], lag_ratio=0.25), run_time=0.6)
        self.play(FadeIn(router), FadeIn(router_lbl), run_time=0.5)
        self.play(LaggedStart(*[Create(a) for a in router_arcs], lag_ratio=0.25), run_time=0.6)
        self.play(FadeIn(satellite), FadeIn(sat_lbl), run_time=0.5)
        self.play(LaggedStart(*[Create(s) for s in sat_signals], lag_ratio=0.2), run_time=0.5)
        self.wait(7.2 - 0.6 - 0.7 - 0.6 - 0.5 - 0.6 - 0.5 - 0.5)   # 3.2 sec

        # \"In 5G cellular networks, signals travel through noisy environments.
        #  In Wi-Fi, signals bounce off walls creating multipath interference.
        #  In flash memory, storage cells degrade causing multiple nearby bits
        #  to fail together. In all of these cases, the error model is complex
        #  and structured — exactly where LDPC excels.\"
        # 54 words × 0.4 = 21.6 sec  (noise label visible during this)
        self.play(FadeIn(noise_label), run_time=0.4)
        self.wait(21.6 - 0.4)   # 21.2 sec

        self.play(
            FadeOut(VGroup(
                wireless_title, tower, tower_lbl, tower_arcs,
                router, router_lbl, router_arcs,
                satellite, sat_lbl, sat_signals,
                noise_label
            )),
            run_time=0.8
        )

        # ═════════════════════════════════════════════════════════════════════
        # PART 4 — AI servers → Rowhammer → LDPC in DRAM → References
        # ═════════════════════════════════════════════════════════════════════

        # ── 4a: Title writes in and immediately moves to top ─────────────────

        # "As we move into the AI era, servers are experiencing heavier
        #  DRAM workloads and denser memory chips than ever before, making
        #  them prime targets for Rowhammer."
        # 30 words leading into server visual — Part 4 total ~92 words
        future_title = Text("The Future of DRAM Security",
                            font_size=40, color=YELLOW, weight=BOLD)
        future_title.to_edge(UP, buff=0.45)
        self.play(Write(future_title), run_time=1.2)
        self.wait(5.6 - 1.2)   # 4.4 sec  (future title settles)

        # ── 4b: AI server rack with load bars ────────────────────────────────

        # "As we move into the AI era, servers experiencing heavier workloads."
        # Server rack appears (1.0 sec) + bars fill (2.0 sec)
        # 20 words × 0.4 = 8.0 sec

        # Three server units stacked vertically
        SERVER_W, SERVER_H = 3.6, 0.70
        SERVER_GAP = 0.22
        SERVER_Y = [0.9 - i * (SERVER_H + SERVER_GAP) for i in range(3)]
        SERVER_LABELS = ["GPU Node", "GPU Node", "Memory Controller"]

        server_boxes = VGroup()
        server_lbls  = VGroup()
        for i, y in enumerate(SERVER_Y):
            box = Rectangle(width=SERVER_W, height=SERVER_H,
                            fill_opacity=0.25, fill_color=BLUE_D,
                            stroke_color=BLUE_B, stroke_width=1.8)
            box.move_to([-1.8, y, 0])
            lbl = Text(SERVER_LABELS[i], font_size=16, color=WHITE)
            lbl.move_to(box)
            server_boxes.add(box)
            server_lbls.add(lbl)

        rack_frame = Rectangle(
            width=SERVER_W + 0.55, height=3 * SERVER_H + 2 * SERVER_GAP + 0.45,
            fill_opacity=0.0, stroke_color=GRAY, stroke_width=2.5
        )
        rack_frame.move_to([-1.8, SERVER_Y[1], 0])
        rack_lbl = Text("AI Server Rack", font_size=19, color=GRAY)
        rack_lbl.next_to(rack_frame, UP, buff=0.15)

        self.play(
            FadeIn(rack_frame), FadeIn(rack_lbl),
            FadeIn(server_boxes, lag_ratio=0.2),
            FadeIn(server_lbls,  lag_ratio=0.2),
            run_time=1.0
        )

        # CPU/load indicators — small green bars that fill up on each server
        load_bars = VGroup()
        load_fills = []
        for i, y in enumerate(SERVER_Y):
            bar_bg = Rectangle(width=1.1, height=0.18,
                               fill_opacity=0.3, fill_color=DARK_GRAY,
                               stroke_color=WHITE, stroke_width=0.8)
            bar_bg.move_to([-1.8 + SERVER_W / 2 - 0.72, y - 0.15, 0])
            bar_fill = Rectangle(width=0.0, height=0.18,
                                 fill_opacity=0.9, fill_color=GREEN,
                                 stroke_color=GREEN, stroke_width=0)
            bar_fill.move_to(bar_bg.get_left() + RIGHT * 0.0)
            bar_fill.align_to(bar_bg, LEFT)
            load_bars.add(bar_bg)
            load_fills.append(bar_fill)
            self.add(bar_fill)

        self.add(load_bars)

        # Animate bars filling to ~90% (high load)
        full_fills = []
        for bf in load_fills:
            target = bf.copy()
            target.stretch_to_fit_width(1.1 * 0.90)
            target.set_fill(RED, opacity=0.9)
            target.set_stroke(RED, 0)
            target.align_to(bf, LEFT)
            full_fills.append(target)

        self.play(*[Transform(load_fills[i], full_fills[i]) for i in range(3)],
                  run_time=2.0)
        heavy_label = Text("Heavy AI Workloads ↑", font_size=20, color=RED)
        heavy_label.move_to([1.6, SERVER_Y[1], 0])
        self.play(FadeIn(heavy_label), run_time=0.4)
        self.wait(8.0 - 1.0 - 2.0 - 0.4)   # 4.6 sec

        # ── 4c: Zoom into chip → DRAM rows → Rowhammer ───────────────────────

        # "…making them prime targets for Rowhammer attacks."
        # 8 words × 0.4 = 3.2 sec  (chip zoom covers this)

        # Fade out server rack, zoom into a chip representation
        self.play(
            FadeOut(rack_frame), FadeOut(rack_lbl),
            FadeOut(server_boxes), FadeOut(server_lbls),
            FadeOut(load_bars),
            *[FadeOut(load_fills[i]) for i in range(3)],
            FadeOut(heavy_label),
            run_time=0.6
        )

        # AI chip die — square with grid of tiny cells inside
        chip_die = Square(side_length=2.8, fill_opacity=0.30,
                          fill_color=BLUE_D, stroke_color=BLUE_B, stroke_width=2.5)
        chip_die.move_to(ORIGIN)
        chip_die_lbl = Text("AI Chip", font_size=22, color=WHITE, weight=BOLD)
        chip_die_lbl.move_to(chip_die.get_top() + DOWN * 0.28)

        # Tiny DRAM row grid inside the chip (5×8)
        DROWS, DCOLS = 5, 8
        DS, DG = 0.24, 0.04
        DSTEP = DS + DG
        dram_cells_inner = VGroup()
        inner_cells_list = []
        for r in range(DROWS):
            row = []
            for c in range(DCOLS):
                sq = Square(side_length=DS, fill_opacity=0.45,
                            fill_color=BLUE_D, stroke_color=BLUE_B, stroke_width=0.6)
                sq.move_to([
                    (c - (DCOLS - 1) / 2) * DSTEP,
                    (( DROWS - 1) / 2 - r) * DSTEP - 0.15,
                    0
                ])
                dram_cells_inner.add(sq)
                row.append(sq)
            inner_cells_list.append(row)

        self.play(FadeIn(chip_die), FadeIn(chip_die_lbl), run_time=0.5)
        self.play(FadeIn(dram_cells_inner, lag_ratio=0.01), run_time=0.6)

        # Zoom into chip using ScaleInPlace + move camera (scale the whole thing up)
        chip_group_zoom = VGroup(chip_die, chip_die_lbl, dram_cells_inner)
        self.play(chip_group_zoom.animate.scale(1.7).move_to(ORIGIN), run_time=1.0)

        dram_zoom_lbl = Text("DRAM Rows", font_size=20, color=GRAY)
        dram_zoom_lbl.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(dram_zoom_lbl), run_time=0.3)
        self.wait(3.2 - 0.5 - 0.6 - 1.0 - 0.3)   # 0.8 sec  (chip zoomed in + DRAM rows visible)

        # Rowhammer attack: hammer row 2 red, flip cells in rows 1 and 3 yellow
        HAMMER_ROW = 2
        FLIP_CELLS = [(1, 1), (1, 4), (1, 6), (3, 0), (3, 3), (3, 5), (3, 7)]

        # "While it requires a slightly more complex hardware implementation,
        #  bringing the iterative mathematical power of LDPC codes into DRAM
        #  is no longer just a theoretical exercise."
        # 28 words × 0.4 = 11.2 sec  (Rowhammer pulse + flip covers this)

        # Colour hammer row red + pulse 3×
        self.play(
            *[inner_cells_list[HAMMER_ROW][c].animate
              .set_fill(RED, opacity=0.85).set_stroke(RED_A, 0.8)
              for c in range(DCOLS)],
            run_time=0.5
        )
        for _ in range(3):
            self.play(*[inner_cells_list[HAMMER_ROW][c].animate
                        .set_fill(RED, opacity=1.0) for c in range(DCOLS)],
                      run_time=0.18)
            self.play(*[inner_cells_list[HAMMER_ROW][c].animate
                        .set_fill(RED, opacity=0.6) for c in range(DCOLS)],
                      run_time=0.18)

        # Flip adjacent cells to yellow
        self.play(
            *[inner_cells_list[r][c].animate
              .set_fill(YELLOW, opacity=0.9).set_stroke(YELLOW_A, 0.8)
              for r, c in FLIP_CELLS],
            run_time=0.5
        )
        rh_label = Text("Rowhammer!", font_size=26, color=RED, weight=BOLD)
        rh_label.to_edge(DOWN, buff=0.5)
        self.play(FadeOut(dram_zoom_lbl), FadeIn(rh_label), run_time=0.3)
        self.wait(11.2 - 0.5 - 3 * 0.36 - 0.5 - 0.3)   # 8.3 sec

        # ── 4d: Zoom back out → LDPC shield overlaid on DRAM ─────────────────

        # LDPC shield + zoom-out covers the remaining ~21.6-sec block

        # "It is rapidly becoming a strict security necessity for the future
        #  of computing."
        # 13 words × 0.4 = 5.2 sec

        # Reset cells, zoom back out
        self.play(
            *[inner_cells_list[r][c].animate
              .set_fill(BLUE_D, opacity=0.45).set_stroke(BLUE_B, 0.6)
              for r in range(DROWS) for c in range(DCOLS)],
            chip_group_zoom.animate.scale(1 / 1.7).move_to([-2.5, 0, 0]),
            FadeOut(rh_label),
            run_time=1.0
        )

        # LDPC Tanner-graph shield on the right side
        SHIELD_VAR_Y =  1.3
        SHIELD_CHK_Y = -0.9
        svx = [0.8 + i * 0.85 for i in range(5)]
        scx = [1.25 + i * 1.7  for i in range(3)]
        SHIELD_EDGES = [(0,0),(1,0),(2,0),(1,1),(2,1),(3,1),(2,2),(3,2),(4,2)]
        SHIELD_ECOLORS = [GREEN, YELLOW, BLUE_B]   # one per check

        shield_var = VGroup(*[
            Circle(radius=0.14, fill_opacity=0.7,
                   fill_color=GREEN, stroke_color=GREEN_B, stroke_width=1.5)
            .move_to([x, SHIELD_VAR_Y, 0])
            for x in svx
        ])
        shield_chk = VGroup(*[
            Square(side_length=0.28, fill_opacity=0.9,
                   fill_color=BLACK, stroke_color=WHITE, stroke_width=1.8)
            .move_to([x, SHIELD_CHK_Y, 0])
            for x in scx
        ])
        shield_edges = VGroup(*[
            Line([svx[v], SHIELD_VAR_Y - 0.14, 0],
                 [scx[k], SHIELD_CHK_Y + 0.14, 0],
                 color=SHIELD_ECOLORS[k], stroke_width=1.5)
            for v, k in SHIELD_EDGES
        ])
        shield_lbl = Text("LDPC Shield", font_size=24, color=GREEN_B, weight=BOLD)
        shield_lbl.move_to([2.55, -1.7, 0])

        arrow_shield = Arrow(
            start=[chip_die.get_right()[0] + 0.2, 0, 0],
            end=[svx[0] - 0.3, 0, 0],
            color=GREEN_B, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.18
        )

        self.play(FadeIn(shield_var, lag_ratio=0.1), FadeIn(shield_chk, lag_ratio=0.1),
                  run_time=0.6)
        self.play(Create(shield_edges, lag_ratio=0.05), run_time=0.7)
        self.play(GrowArrow(arrow_shield), FadeIn(shield_lbl), run_time=0.5)

        # Pulse the whole shield twice to suggest active protection
        shield_group = VGroup(shield_var, shield_chk, shield_edges)
        for _ in range(2):
            self.play(shield_group.animate.set_opacity(1.0), run_time=0.25)
            self.play(shield_group.animate.set_opacity(0.55), run_time=0.25)
        self.play(shield_group.animate.set_opacity(1.0), run_time=0.2)

        protected_lbl = Text("Multi-bit errors corrected ✓", font_size=20, color=GREEN)
        protected_lbl.move_to([2.55, -2.2, 0])
        self.play(FadeIn(protected_lbl), run_time=0.4)
        self.wait(21.6 - (0.6 + 0.7 + 0.5 + 2 * 0.5 + 0.2 + 0.4) - 1.0)   # 16.1 sec (remaining future narration)

        self.play(
            FadeOut(VGroup(
                chip_group_zoom, arrow_shield,
                shield_group, shield_lbl, protected_lbl
            )),
            run_time=0.8
        )

        # ── 4e-pre: Background & Prerequisites ───────────────────────────────

        # ~85 words ÷ 200 wpm × 60 sec ≈ 25 sec display time
        prereq_header = Text("Assumed Background & Prerequisites",
                             font_size=26, color=YELLOW, weight=BOLD)
        prereq_body = Text(
            "This video is designed for a mathematically curious audience. We do\n"
            "not assume any prior knowledge of DRAM architecture, Rowhammer\n"
            "attacks, or Error Correcting Codes. However, to fully grasp the LDPC\n"
            "solution, viewers should understand the basic idea of sending\n"
            "information and the possibility of information being corrupted.",
            font_size=18, color=WHITE
        )
        prereq_cta = Text(
            "For more insight on how LDPC codes work, check out the video below:",
            font_size=17, color=LIGHT_GRAY
        )
        prereq_title = Text(
            "Error Correction for 5G Communication (LDPC codes) — Art of the Problem",
            font_size=17, color=BLUE_B
        )
        prereq_url = Text(
            "youtube.com/watch?v=RWUxtGh-guY",
            font_size=16, color=BLUE_C
        )

        prereq_group = VGroup(prereq_header, prereq_body, prereq_cta,
                              prereq_title, prereq_url)
        prereq_group.arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        prereq_group.to_edge(LEFT, buff=0.6)

        self.play(FadeIn(prereq_header), run_time=0.5)
        self.play(FadeIn(prereq_body), run_time=0.8)
        self.play(FadeIn(prereq_cta), FadeIn(prereq_title),
                  FadeIn(prereq_url), run_time=0.6)
        # ~85 words ÷ 200 wpm × 60 sec ≈ 25 sec total; subtract animation time
        self.wait(25.0 - 0.5 - 0.8 - 0.6)   # 23.1 sec reading time
        self.play(FadeOut(prereq_group), run_time=0.6)

        # ── 4e: References ────────────────────────────────────────────────────

        ref_header = Text("References", font_size=28, color=WHITE, weight=BOLD)
        ref_1 = Text("- Gallager, R. G. (1962). Low-density parity-check codes.",
                     font_size=21, color=LIGHT_GRAY)
        ref_2 = Text("- Mutlu, O. (2019). RowHammer in DRAM.",
                     font_size=21, color=LIGHT_GRAY)
        ref_3 = Text("- Synopsys. ECC Memory Error Correction.",
                     font_size=21, color=LIGHT_GRAY)

        refs = VGroup(ref_header, ref_1, ref_2, ref_3)
        refs.arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        refs.move_to([0, -0.6, 0])

        self.play(FadeIn(ref_header), run_time=0.5)
        self.play(FadeIn(ref_1), run_time=0.5)
        self.play(FadeIn(ref_2), run_time=0.5)
        self.play(FadeIn(ref_3), run_time=0.5)

        # Leave references on screen — end of video
        self.wait(12.0)