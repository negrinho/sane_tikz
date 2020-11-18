import sane_tikz.core as stz
import sane_tikz.formatting as fmt
import numpy as np
import math

width = 2.5
line_width = 3.0 * fmt.standard_line_width
rectangle_roundness = 0.1
connector_roundness = 0.2
to_add_norm_spacing = 0.15
per_line_height = 0.40
percent_width_trident_spacing = 0.45
plus_circle_radius = 0.2
sine_circle_radius = 2 * plus_circle_radius
spacing_between_text_and_arrows = 0.0
arrow_length = 0.6
residual_spacing = 2.0
trident_alpha = 0.75
trident_spacing = 0.4
spacing_between_towers = 1.5
bbox_spacing = 0.45
bbox_roundness = 0.3

name2color = {
    "emb_color": (252, 224, 225),
    "multi_head_attention_color": (252, 226, 187),
    "add_norm_color": (242, 243, 193),
    "ff_color": (194, 232, 247),
    "softmax_color": (203, 231, 207),
    "linear_color": (220, 223, 240),
    "gray_bbox_color": (243, 243, 244)
}

s_arr = fmt.combine_tikz_strs(
    [fmt.line_width(line_width),
     fmt.arrow_heads("end")])

s_lw = fmt.combine_tikz_strs([fmt.line_width(line_width)])

s_con = s_bbox = fmt.combine_tikz_strs([
    fmt.arrow_heads("end"),
    fmt.line_width(line_width),
    fmt.rounded_corners(connector_roundness)
])

s_bbox = fmt.combine_tikz_strs([
    fmt.fill_color("gray_bbox_color"),
    fmt.line_width(line_width),
    fmt.rounded_corners(bbox_roundness)
])


def trident_coords(e):
    top_left_cs, bottom_right_cs = stz.bbox(e)
    center_cs = stz.bottom_center_coords(top_left_cs, bottom_right_cs)
    left_cs = stz.translate_coords_horizontally(center_cs,
                                                -trident_alpha * width / 2.0)
    right_cs = stz.translate_coords_horizontally(center_cs,
                                                 trident_alpha * width / 2.0)

    cs_lst = [left_cs, center_cs, right_cs]
    translated_cs_lst = [
        stz.translate_coords_vertically(cs, -trident_spacing) for cs in cs_lst
    ]
    return cs_lst, translated_cs_lst


def lst2str(s_lst):
    return " \\vspace{-0.05cm} \\linebreak ".join(s_lst)


def rectangle(height, color_name):
    s_fmt = fmt.combine_tikz_strs([
        fmt.line_width(line_width),
        fmt.fill_color(color_name),
        fmt.rounded_corners(rectangle_roundness)
    ])
    return stz.rectangle_from_width_and_height([0, 0], height, width, s_fmt)


def rectangle_with_text(color_name, s_lst):
    height = 0.1 + per_line_height * len(s_lst)
    s_width = fmt.combine_tikz_strs([fmt.text_width(width), "align=center"])
    r = rectangle(height, color_name)
    cs = stz.center_coords(r)
    s = " \\vspace{-0.05cm} \\linebreak ".join(s_lst)
    t = stz.latex(cs, s, s_width)
    return [r, t]


def rectangle_with_add_norm(color_name, s_lst):
    r1 = rectangle_with_text("add_norm_color", ["Add \\& Norm"])
    r2 = rectangle_with_text(color_name, s_lst)

    top_left_cs, bottom_right_cs = stz.bbox(r2)
    cs = stz.translate_coords_vertically(
        stz.top_center_coords(top_left_cs, bottom_right_cs),
        to_add_norm_spacing)
    stz.translate_bbox_bottom_center_to_coords(r1, cs)
    c = connect_straight_vertical(r2, r1)
    return [r1, r2, c]


def connect_straight_vertical(e_from, e_to):
    from_cs = stz.coords_from_bbox_with_fn(e_from, stz.top_center_coords)
    to_cs = stz.coords_from_bbox_with_fn(e_to, stz.bottom_center_coords)
    return stz.line_segment(from_cs, to_cs, s_lw)


def connect_straight_horizontal(e_from, e_to):
    from_cs = stz.coords_from_bbox_with_fn(e_from, stz.right_center_coords)
    to_cs = stz.coords_from_bbox_with_fn(e_to, stz.left_center_coords)
    return stz.line_segment(from_cs, to_cs, s_lw)


def connect_straight_with_arrow(e_from, e_to):
    from_cs = stz.coords_from_bbox_with_fn(e_from, stz.top_center_coords)
    to_cs = stz.coords_from_bbox_with_fn(e_to, stz.bottom_center_coords)
    return stz.line_segment(from_cs, to_cs, s_arr)


def connect_residual(e_with_addnorm, bottom_spacing, side_spacing):
    from_cs = stz.coords_from_bbox_with_fn(e_with_addnorm,
                                           stz.bottom_center_coords)
    from_cs = stz.translate_coords_vertically(from_cs, -bottom_spacing)

    if side_spacing < 0:
        to_cs = stz.coords_from_bbox_with_fn(e_with_addnorm[0],
                                             stz.left_center_coords)
    else:
        to_cs = stz.coords_from_bbox_with_fn(e_with_addnorm[0],
                                             stz.right_center_coords)
    cs = stz.translate_coords_horizontally(from_cs, side_spacing)
    return stz.open_path([from_cs, cs, [cs[0], to_cs[1]], to_cs], s_con)


def circle_with_sine():
    r = sine_circle_radius
    alpha = 0.6 * r
    delta = 0.02
    circle = stz.circle([0, 0], r, s_lw)
    k = 2.0 * math.pi
    xs = np.linspace(0.0, k)
    ys = np.sin(xs)
    cs_lst = []
    for x, y in zip(xs, ys):
        cs_lst.append([
            stz.axis_value_to_canvas_value(-r + delta, 0.0, r - delta, k, x),
            stz.axis_value_to_canvas_value(-r + delta, -r / alpha, r - delta,
                                           r / alpha, y)
        ])
    sine = stz.open_path(cs_lst, s_lw)
    return [circle, sine]


def circle_with_plus():
    r = plus_circle_radius
    circle = stz.circle([0, 0], r, s_lw)
    plus = [
        stz.centered_horizontal_line_segment([0, 0], 1.6 * r, s_lw),
        stz.centered_vertical_line_segment([0, 0], 1.6 * r, s_lw),
    ]
    return [circle, plus]


def arrow_in(e):
    to_cs = stz.coords_from_bbox_with_fn(e, stz.bottom_center_coords)
    from_cs = stz.translate_coords_vertically(to_cs, -arrow_length)
    return stz.line_segment(from_cs, to_cs, s_arr)


def arrow_out(e):
    from_cs = stz.coords_from_bbox_with_fn(e, stz.top_center_coords)
    to_cs = stz.translate_coords_vertically(from_cs, arrow_length)
    return stz.line_segment(from_cs, to_cs, s_arr)


### left tower
ier = rectangle_with_text("emb_color", ["Input", "Embedding"])
cl = circle_with_plus()
sl = circle_with_sine()
mha1_an = rectangle_with_add_norm("multi_head_attention_color",
                                  ["Multi-Head", "Attention"])
ff1_an = rectangle_with_add_norm("ff_color", ["Feed", "Forward"])

stz.place_above_and_align_to_the_center(cl, ier, 0.4)
stz.place_to_the_left_and_align_to_the_center(sl, cl, 0.3)
stz.place_above_and_align_to_the_center(mha1_an, cl, 1.33)
stz.place_above_and_align_to_the_center(ff1_an, mha1_an, 1.0)

### right tower
oer = rectangle_with_text("emb_color", ["Output", "Embedding"])
cr = circle_with_plus()
sr = circle_with_sine()
mha2_an = rectangle_with_add_norm("multi_head_attention_color",
                                  ["Multi-Head", "Attention"])
mmha_an = rectangle_with_add_norm("multi_head_attention_color",
                                  ["Masked", "Multi-Head", "Attention"])
ff2_an = rectangle_with_add_norm("ff_color", ["Feed", "Forward"])
linear = rectangle_with_text("linear_color", ["Linear"])
softmax = rectangle_with_text("softmax_color", ["Softmax"])

stz.place_to_the_right_and_align_to_the_bottom(oer, ier, spacing_between_towers)
stz.place_above_and_align_to_the_center(cr, oer, 0.4)
stz.place_to_the_right_and_align_to_the_center(sr, cr, 0.3)
stz.place_above_and_align_to_the_center(mmha_an, cr, 1.33)
stz.place_above_and_align_to_the_center(mha2_an, mmha_an, 1.0)
stz.place_above_and_align_to_the_center(ff2_an, mha2_an, 1.0)
stz.place_above_and_align_to_the_center(ff2_an, mha2_an, 1.0)
stz.place_above_and_align_to_the_center(linear, ff2_an, 0.6)
stz.place_above_and_align_to_the_center(softmax, linear, 0.6)

#####
connections = [
    connect_straight_with_arrow(mha1_an, ff1_an),
    connect_straight_with_arrow(mha2_an, ff2_an),
    connect_straight_with_arrow(ff2_an, linear),
    connect_straight_with_arrow(linear, softmax),
    connect_straight_with_arrow(ier, cl),
    connect_straight_with_arrow(cl, mha1_an),
    connect_straight_with_arrow(cr, mmha_an),
    connect_straight_with_arrow(oer, cr),
    connect_straight_horizontal(sl, cl),
    connect_straight_horizontal(cr, sr)
]

connections.extend([
    connect_residual(ff1_an, 0.6, -residual_spacing),
    connect_residual(mha1_an, 0.6, -residual_spacing),
    connect_residual(mmha_an, 0.6, residual_spacing),
    connect_residual(mha2_an, 0.6, residual_spacing),
    connect_residual(ff2_an, 0.6, residual_spacing)
])

### bounding boxes
b = stz.bbox([ff1_an, mha1_an, connections[-4]])
bb1 = stz.rectangle_from_additive_resizing(b[0], b[1], bbox_spacing,
                                           bbox_spacing, s_bbox)
b = stz.bbox([ff2_an, mmha_an, connections[-2], connections[-3]])
bb2 = stz.rectangle_from_additive_resizing(b[0], b[1], bbox_spacing,
                                           bbox_spacing, s_bbox)

### trident connections
tri_cs, translated_tri_cs = trident_coords(mha1_an)
e1 = stz.open_path([
    translated_tri_cs[1],
    stz.bottom_left_coords(translated_tri_cs[1], tri_cs[0]), tri_cs[0]
], s_con)
e2 = stz.open_path([
    translated_tri_cs[1],
    stz.bottom_right_coords(translated_tri_cs[1], tri_cs[2]), tri_cs[2]
], s_con)
connections.extend([e1, e2])

tri_cs, translated_tri_cs = trident_coords(mmha_an)
e1 = stz.open_path([
    translated_tri_cs[1],
    stz.bottom_left_coords(translated_tri_cs[1], tri_cs[0]), tri_cs[0]
], s_con)
e2 = stz.open_path([
    translated_tri_cs[1],
    stz.bottom_right_coords(translated_tri_cs[1], tri_cs[2]), tri_cs[2]
], s_con)
connections.extend([e1, e2])

tri_cs, translated_tri_cs = trident_coords(mha2_an)
# the leftmost two
from_cs = stz.coords_from_bbox_with_fn(ff1_an, stz.top_center_coords)
mid_cs = stz.midway_coords(stz.bbox(bb1)[1], stz.bbox(bb2)[0])
to_cs = translated_tri_cs[0]
cs = stz.translate_coords_vertically(from_cs, 1.0)
e1 = stz.open_path([
    from_cs, cs, [mid_cs[0], cs[1]], [mid_cs[0], to_cs[1]],
    translated_tri_cs[0], tri_cs[0]
], s_con)

e2 = stz.open_path([
    from_cs, cs, [mid_cs[0], cs[1]], [mid_cs[0], to_cs[1]],
    translated_tri_cs[1], tri_cs[1]
], s_con)

# the rightmost one
from_cs = stz.coords_from_bbox_with_fn(mmha_an, stz.top_center_coords)
e3 = stz.open_path(
    [from_cs, translated_tri_cs[1], translated_tri_cs[2], tri_cs[2]], s_con)
connections.extend([e1, e2, e3])

arrows = [arrow_in(ier), arrow_in(oer), arrow_out(softmax)]

### annotations
# arrow text
s_fmt = fmt.combine_tikz_strs(
    [fmt.text_width(width), "anchor=north", "align=center"])
cs = stz.translate_coords_vertically(
    stz.coords_from_bbox_with_fn(arrows[0], stz.bottom_center_coords),
    -spacing_between_text_and_arrows)
a1 = stz.latex(cs, "Inputs", s_fmt)

cs = stz.translate_coords_vertically(
    stz.coords_from_bbox_with_fn(arrows[1], stz.bottom_center_coords),
    -spacing_between_text_and_arrows)
a2 = stz.latex(cs, lst2str(["Outputs", "(shifted right)"]), s_fmt)

s_fmt = fmt.combine_tikz_strs(
    [fmt.text_width(width), "anchor=south", "align=center"])

cs = stz.translate_coords_vertically(
    stz.coords_from_bbox_with_fn(arrows[2], stz.top_center_coords),
    spacing_between_text_and_arrows)
a3 = stz.latex(cs, lst2str(["Output", "Probabilities"]), s_fmt)

# side text
spacing = 0.2
cs = stz.coords_from_bbox_with_fn(bb1, stz.left_center_coords)
a4 = stz.latex([cs[0] - spacing, cs[1]], "$N\\times$",
               fmt.anchor("right_center"))
cs = stz.coords_from_bbox_with_fn(bb2, stz.right_center_coords)
a5 = stz.latex([cs[0] + spacing, cs[1]], "$N\\times$",
               fmt.anchor("left_center"))

s_fn = lambda side: fmt.combine_tikz_strs(
    [fmt.text_width(2.0), fmt.anchor(side + "_center")])
cs = stz.coords_from_bbox_with_fn(sl, stz.left_center_coords)
a6 = stz.latex([cs[0] + 0.3, cs[1]], lst2str(["Positional", "Encoding"]),
               s_fn("right"))
cs = stz.coords_from_bbox_with_fn(sr, stz.right_center_coords)
a7 = stz.latex([cs[0] + 0.2, cs[1]], lst2str(["Positional", "Encoding"]),
               s_fn("left"))

annotations = [a1, a2, a3, a4, a5, a6, a7]

# all
e = [
    bb1, bb2, ier, oer, mha1_an, mha2_an, mmha_an, ff1_an, ff2_an, linear,
    softmax, cl, cr, sl, sr, connections, arrows, annotations
]

stz.draw_to_tikz_standalone(e, "transformer.tex", name2color)