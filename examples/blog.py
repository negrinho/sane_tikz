

import sane_tikz as stz
import formatting as fmt

# from https://arxiv.org/pdf/1906.08237.pdf
# needs to do opacity stuff.

square_side = 0.85
rectangle_width = 1.4
roundness_in_cm = 0.1
line_width = 2.0 * fmt.standard_line_width
opacity_level = 0.5
horizontal_spacing = 1.0
vertical_spacing = 1.0

tc_fn = lambda e: stz.coords_from_bbox_with_fn(e, stz.top_center_coords)
bc_fn = lambda e: stz.coords_from_bbox_with_fn(e, stz.bottom_center_coords)

def rectangle_with_latex(width, expr, rectangle_tikz_str="", latex_tikz_str=""):
    r_fmt = fmt.combine_tikz_strs([
        # fmt.alignment("center"),
        fmt.rounded_corners(roundness_in_cm),
        latex_tikz_str,
        fmt.line_width(line_width)
        ])
    l_fmt = fmt.combine_tikz_strs([
        latex_tikz_str
    ])
    r = stz.rectangle_from_width_and_height([0, 0], square_side, width, r_fmt)
    l = stz.latex(stz.center_coords(r), expr, l_fmt)
    return [r, l]


def sq_fn(expr, square_tikz_str="", latex_tikz_str=""):
    return rectangle_with_latex(square_side, expr, square_tikz_str, latex_tikz_str)

def rct_fn(expr, rectangle_tikz_str="", latex_tikz_str=""):
    return rectangle_with_latex(rectangle_width, expr, rectangle_tikz_str, latex_tikz_str)

def connect(e_from, e_to):
    cs_from = stz.coords_from_bbox_with_fn(e_from, stz.top_center_coords)
    cs_to = stz.coords_from_bbox_with_fn(e_to, stz.bottom_center_coords)
    s_fmt = fmt.combine_tikz_strs([fmt.line_width(line_width), fmt.arrow_heads("end")])
    return stz.line_segment(cs_from, cs_to, s_fmt)


# # quadrant.
# def f(e, e_other):
#     left_top_cs = stz.bbox(e)
#     stz.bbox(e_other)

# def overlaps(e, e_other):
#     stz.bbox()

# NOTE: do the place above one.

cs = [0, 0]
e = stz.square(cs, square_side)

xs = [sq_fn("$x_%d$" % (i + 1,)) for i in range(4)]
hs1 = [sq_fn("$h_%d^{(1)}$" % (i + 1,)) for i in range(4)]
hs2 = [sq_fn("$h_%d^{(2)}$" % (i + 2,)) for i in range(4)]
m1, m2 = [rct_fn("$\\text{mem}^{(%d)}$" % (i + 1,)) for i in range(2)]
x_out = [sq_fn("$x_3$")]

row1 = [m1] + xs
row2 = [m2] + hs1

stz.distribute_horizontally_with_spacing([m1] + xs, horizontal_spacing)
stz.distribute_horizontally_with_spacing([m2] + hs1, horizontal_spacing)
stz.distribute_horizontally_with_spacing(hs2, horizontal_spacing)
# NOTE: fix this spacing.
stz.distribute_vertically_with_spacing([row1, row2, hs2][::-1], vertical_spacing)
stz.align_rights([row1, row2, hs2], 0)

stz.place_above_and_align_to_the_center(x_out, hs2[2], vertical_spacing)

connections = [
connect(m1, hs1[2]),
connect(m2, hs2[2]),
connect(hs1[2], hs2[2]),
connect(hs2[2], x_out)]

e = [row1, row2, hs2, x_out, connections]
stz.draw_to_tikz_standalone(e, "fig.tex")


#### NOTE: this does it.

# graphical model example.

# place above with some alignment functionality. center, left, right
### TODO: rename to translate? check this?


# TODO: align tops to reference tops

# TODO: perhaps have it such that there is an angle. distance to the closest
# point of the bounding box.
###

# NOTE: think about aspect ratio. (NOTE: this is figure something from some file.)

