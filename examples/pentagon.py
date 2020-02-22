# answer to latex exchange question: https://tex.stackexchange.com/questions/528863/how-do-you-name-nodes-vertices-with-this-type-of-code/528885#528885

import sane_tikz as stz
import formatting as fmt

label_spacing = 0.25
pentagon_radius = 1.2
x_axis_length = 4.0
y_axis_length = 3.0
extra_length = 0.4
a_circle_radius = 0.08
s_fmt = fmt.arrow_heads("end")
f_fmt = fmt.line_and_fill_colors('black', 'black')

cs = [
    stz.coords_on_circle([0, 0], pentagon_radius, 90.0 + i * (360.0 / 5))
    for i in range(5)
]
e = stz.closed_path(cs)

origin_cs = stz.translate_coords_horizontally(cs[2], -1.0)
x_end_cs = stz.translate_coords_horizontally(origin_cs, x_axis_length)
y_end_cs = stz.translate_coords_vertically(origin_cs, y_axis_length)
x_start_cs = stz.translate_coords_horizontally(origin_cs, -extra_length)
y_start_cs = stz.translate_coords_vertically(origin_cs, -extra_length)
x_label_cs = stz.translate_coords_vertically(x_end_cs, -label_spacing)
y_label_cs = stz.translate_coords_horizontally(y_end_cs, -label_spacing)
origin_label_cs = stz.translate_coords_diagonally(origin_cs, -label_spacing)

axes = [
    stz.line_segment(x_start_cs, x_end_cs, s_fmt),
    stz.line_segment(y_start_cs, y_end_cs, s_fmt)
]

labels = [
    stz.latex([cs[0][0], cs[0][1] + label_spacing], "$C$"),
    stz.latex([cs[1][0] - label_spacing, cs[1][1]], "$B$"),
    stz.latex([cs[2][0], cs[2][1] - a_circle_radius - label_spacing],
              "$A(1, 0)$"),
    stz.latex([cs[3][0], cs[3][1] - label_spacing], "$E$"),
    stz.latex([cs[4][0] + label_spacing, cs[4][1]], "$D$"),
    stz.circle(cs[2], a_circle_radius, f_fmt),
    stz.latex(x_label_cs, "$x$"),
    stz.latex(y_label_cs, "$y$"),
    stz.latex(origin_label_cs, "$O$"),
]

stz.draw_to_tikz_standalone([e, labels, axes], "pentagon.tex")
