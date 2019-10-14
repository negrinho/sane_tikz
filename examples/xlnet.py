# Reproduction of Figure 1 (top left) https://arxiv.org/pdf/1906.08237.pdf

import sane_tikz as stz
import formatting as fmt

square_side = 0.85
rectangle_width = 1.4
roundness_in_cm = 0.1
line_width = 2.0 * fmt.standard_line_width
opacity_level = 0.5
horizontal_spacing = 1.0
vertical_spacing = 1.0
legend_spacing = 0.5

name2color = {
    "my_grey": (217, 217, 217),
    "my_yellow": (255, 212, 76),
    "my_blue": (1, 176, 240),
    "my_green": (50, 192, 115),
    "my_red": (255, 102, 102)
}

m_fmt = fmt.line_and_fill_colors("my_grey", "my_grey")
x1_fmt = fmt.line_and_fill_colors("my_yellow", "my_yellow")
x2_fmt = fmt.line_and_fill_colors("my_blue", "my_blue")
x3_fmt = fmt.line_and_fill_colors("my_green", "my_green")
x4_fmt = fmt.line_and_fill_colors("my_red", "my_red")
xs_fmt = [x1_fmt, x2_fmt, x3_fmt, x4_fmt]

h_green_rfmt = fmt.combine_tikz_strs(
    [fmt.line_width(2.0 * line_width),
     fmt.line_color("my_green")])
h_grey_rfmt = fmt.line_color("my_grey")
h_grey_lfmt = fmt.text_color("my_grey")


def rectangle_with_latex(width, expr, rectangle_tikz_str="", latex_tikz_str=""):
    r_fmt = fmt.combine_tikz_strs([
        # fmt.alignment("center"),
        fmt.rounded_corners(roundness_in_cm),
        fmt.line_width(line_width),
        rectangle_tikz_str
    ])
    l_fmt = fmt.combine_tikz_strs([latex_tikz_str])
    r = stz.rectangle_from_width_and_height([0, 0], square_side, width, r_fmt)
    l = stz.latex(stz.center_coords(r), expr, l_fmt)
    return [r, l]


def sq_fn(expr, square_tikz_str="", latex_tikz_str=""):
    return rectangle_with_latex(square_side, expr, square_tikz_str,
                                latex_tikz_str)


def rct_fn(expr, rectangle_tikz_str="", latex_tikz_str=""):
    return rectangle_with_latex(rectangle_width, expr, rectangle_tikz_str,
                                latex_tikz_str)


def connect(e_from, e_to):
    cs_from = stz.coords_from_bbox_with_fn(e_from, stz.top_center_coords)
    cs_to = stz.coords_from_bbox_with_fn(e_to, stz.bottom_center_coords)
    s_fmt = fmt.combine_tikz_strs(
        [fmt.line_width(line_width),
         fmt.arrow_heads("end")])
    return stz.line_segment(cs_from, cs_to, s_fmt)


xs = [sq_fn("$x_%d$" % (i + 1,), xs_fmt[i]) for i in range(4)]
hs1 = [
    sq_fn("$h_%d^{(1)}$" % (i + 1,), h_grey_rfmt if i != 2 else h_green_rfmt,
          h_grey_lfmt if i != 2 else "") for i in range(4)
]
hs2 = [
    sq_fn("$h_%d^{(2)}$" % (i + 1,), h_grey_rfmt if i != 2 else h_green_rfmt,
          h_grey_lfmt if i != 2 else "") for i in range(4)
]
m1, m2 = [rct_fn("$\\text{mem}^{(%d)}$" % (i + 1,), m_fmt) for i in range(2)]
x_out = [sq_fn("$x_3$", x3_fmt)]

row1 = [m1] + xs
row2 = [m2] + hs1

stz.distribute_horizontally_with_spacing([m1] + xs, horizontal_spacing)
stz.distribute_horizontally_with_spacing([m2] + hs1, horizontal_spacing)
stz.distribute_horizontally_with_spacing(hs2, horizontal_spacing)
stz.distribute_vertically_with_spacing([row1, row2, hs2][::-1],
                                       vertical_spacing)
stz.align_rights([row1, row2, hs2], 0)

stz.place_above_and_align_to_the_center(x_out, hs2[2], vertical_spacing)

legend = stz.latex(
    [0, 0],
    "Factorization order: $3 \\rightarrow 2 \\rightarrow 4 \\rightarrow 1$")
cs = stz.place_below_and_align_to_the_center(legend, xs, legend_spacing)

connections = [
    connect(m1, hs1[2]),
    connect(m2, hs2[2]),
    connect(hs1[2], hs2[2]),
    connect(hs2[2], x_out)
]

e = [row1, row2, hs2, x_out, connections, legend]
stz.draw_to_tikz_standalone(e, "xlnet.tex", name2color)
