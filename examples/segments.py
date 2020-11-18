import sane_tikz.core as stz

label_spacing = 0.25
tick_label_spacing = 0.25
tick_length = 0.25
segment_spacing = 0.6
length_multiplier = 0.8


def segment(length, label_str, left_tick_label_str, right_tick_label_str):
    seg = stz.line_segment([0, 0], [length, 0])
    left_tick = stz.centered_vertical_line_segment([0, 0], tick_length)
    right_tick = stz.centered_vertical_line_segment([length, 0], tick_length)
    left_tick_label = stz.latex([0, 0], left_tick_label_str)
    right_tick_label = stz.latex([0, 0], right_tick_label_str)
    stz.place_above_and_align_to_the_center(left_tick_label, left_tick,
                                            tick_label_spacing)
    stz.place_above_and_align_to_the_center(right_tick_label, right_tick,
                                            tick_label_spacing)
    seg_label = stz.latex([-label_spacing, 0], label_str)
    return [
        seg, left_tick, right_tick, left_tick_label, right_tick_label, seg_label
    ]


segs = [
    segment(length_multiplier * 5, "A", "0", "5"),
    segment(length_multiplier * 1, "B", "2", "3"),
    segment(length_multiplier * 3, "C", "1", "4")
]

stz.distribute_vertically_with_spacing(segs[::-1], segment_spacing)
stz.draw_to_tikz_standalone(segs, "segments.tex")
