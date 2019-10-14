# reproduction of Figure 5 (left) from http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf

import sane_tikz as stz
import formatting as fmt

node_radius = 0.35
node_spacing = 2.4 * node_radius
label_spacing = 0.3
delta_angle = 10.0
horizontal_plate_spacing = 0.5
vertical_plate_spacing = 0.25
plate_label_spacing = 0.24


def connect_horizontally(e_from, e_to):
    s_fmt = fmt.arrow_heads("end")
    cs_from = stz.coords_from_bbox_with_fn(e_from, stz.right_center_coords)
    cs_to = stz.coords_from_bbox_with_fn(e_to, stz.left_center_coords)
    return stz.line_segment(cs_from, cs_to, s_fmt)


def connect_diagonally(e_from, e_to):
    s_fmt = fmt.arrow_heads("end")
    from_center_cs = stz.center_coords(e_from)
    to_center_cs = stz.center_coords(e_to)
    return stz.line_segment_between_circles(from_center_cs, node_radius, -90.0,
                                            to_center_cs, node_radius,
                                            180.0 - delta_angle, s_fmt)


def label_below(e, expr):
    cs_ref = stz.coords_from_bbox_with_fn(e, stz.bottom_center_coords)
    cs = stz.translate_coords_vertically(cs_ref, -label_spacing)
    return stz.latex(cs, expr)


def label_left(e, expr):
    cs_ref = stz.coords_from_bbox_with_fn(e, stz.left_center_coords)
    cs = stz.translate_coords_horizontally(cs_ref, -label_spacing)
    return stz.latex(cs, expr)


def label_right(e, expr):
    cs_ref = stz.coords_from_bbox_with_fn(e, stz.right_center_coords)
    cs = stz.translate_coords_horizontally(cs_ref, label_spacing)
    return stz.latex(cs, expr)


def plate(e_lst, expr):
    top_left_cs, bottom_right_cs = stz.bbox(e_lst)
    r = stz.rectangle_from_additive_resizing(top_left_cs, bottom_right_cs,
                                             2.0 * horizontal_plate_spacing,
                                             2.0 * vertical_plate_spacing)
    l_cs = stz.translate_coords_antidiagonally(
        stz.bbox(r)[1], -plate_label_spacing)
    l = stz.latex(l_cs, expr)
    return [r, l]


alpha_c = stz.circle([0, 0], node_radius)
theta_c = stz.circle([0, 0], node_radius)
z_c = stz.circle([0, 0], node_radius)
w_c = stz.circle([0, 0], node_radius)
eta_c = stz.circle([0, 0], node_radius)
beta_c = stz.circle([0, 0], node_radius)

w_c["tikz_str"] = fmt.combine_tikz_strs(
    [w_c["tikz_str"], fmt.fill_color("gray")])

stz.distribute_horizontally_with_spacing([alpha_c, theta_c, z_c, w_c],
                                         node_spacing)
stz.distribute_horizontally_with_spacing([eta_c, beta_c], node_spacing)
stz.place_above_and_align_to_the_center(
    [eta_c, beta_c], [alpha_c, theta_c, z_c, w_c], node_spacing)

alpha_l = label_below(alpha_c, "$\\alpha$")
theta_l = label_below(theta_c, "$\\theta$")
z_l = label_below(z_c, "$z$")
w_l = label_below(w_c, "$w$")
eta_l = label_left(eta_c, "$\\eta$")
beta_l = label_right(beta_c, "$\\beta$")

connections = [
    connect_horizontally(alpha_c, theta_c),
    connect_horizontally(theta_c, z_c),
    connect_horizontally(z_c, w_c),
    connect_horizontally(eta_c, beta_c),
    connect_diagonally(beta_c, w_c),
]

p1 = plate([z_c, w_c, z_l, w_l], "$N$")
p2 = plate([theta_c, theta_l, p1], "$M$")
p3 = plate([beta_c, beta_l], "$k$")

e = [
    alpha_c, theta_c, z_c, w_c, eta_c, beta_c, alpha_l, theta_l, z_l, w_l,
    eta_l, beta_l, connections, p1, p2, p3
]

stz.draw_to_tikz_standalone(e, "lda.tex")