# answer to latex exchange question: https://tex.stackexchange.com/questions/528846/horizontal-bar-graph-with-pgfplot-and-equal-sized-ticks/529041#529041

import sane_tikz.core as stz
import sane_tikz.formatting as fmt

large_data = [4, 2, 1, 1, 0, 5, 4, 2, 2, 0]
large_label_strs = [
    "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten"
]
small_data = [1, 3, 0, 5]
small_label_strs = large_label_strs[:4]

tick_spacing = 1.0
num_ticks = 5
tick_length = 0.1
rectangle_height = 0.3
rectangle_spacing = 0.2
label_spacing = 0.1
r_fmt = fmt.fill_color('gray')
margin = 0.2

frame_width = num_ticks * tick_spacing
frame_spacing = 1.6
t_fmt = fmt.line_color('gray')


def get_ticks(e):
    top_left_cs, bottom_right_cs = stz.bbox(e)
    bottom_left_cs = stz.bottom_left_coords(top_left_cs, bottom_right_cs)
    top_ticks = []
    bottom_ticks = []
    for i in range(1, num_ticks):
        top_cs = stz.translate_coords_horizontally(top_left_cs,
                                                   i * tick_spacing)
        top_t = stz.vertical_line_segment(top_cs, -tick_length, t_fmt)
        top_ticks.append(top_t)

        bottom_cs = stz.translate_coords_horizontally(bottom_left_cs,
                                                      i * tick_spacing)
        bottom_t = stz.vertical_line_segment(bottom_cs, tick_length, t_fmt)
        bottom_ticks.append(bottom_t)
    return [bottom_ticks, top_ticks]


def bar_plot(data, label_strs):
    cs = [0, 0]
    rs = [
        stz.rectangle_from_width_and_height(cs, rectangle_height, x, r_fmt)
        for x in data
    ]

    stz.distribute_vertically_with_spacing(rs, rectangle_spacing)
    frame_height = (len(data) * rectangle_height +
                    (len(data) - 1) * rectangle_spacing + 2.0 * margin)
    frame = stz.rectangle_from_width_and_height(cs, frame_height, frame_width)
    stz.align_centers_vertically([frame, rs], 0.0)

    labels = []
    for i, r in enumerate(rs):
        l_cs = stz.coords_from_bbox_with_fn(r, stz.left_center_coords)
        l_cs = stz.translate_coords_horizontally(l_cs, -label_spacing)
        l_s = label_strs[i]
        lab = stz.latex(l_cs, l_s, fmt.anchor('right_center'))
        labels.append(lab)

    ticks = get_ticks(frame)
    return [rs, labels, frame, ticks]


e_large = bar_plot(large_data, large_label_strs)
e_small = bar_plot(small_data, small_label_strs)
stz.distribute_horizontally_with_spacing([e_small, e_large], frame_spacing)
stz.align_bottoms([e_large, e_small], 0)

stz.draw_to_tikz_standalone([e_small, e_large], "boxes.tex")
