# Figure 5 in https://arxiv.org/pdf/1909.13404.pdf (towards modular and programmable architecture search)

import sane_tikz as stz
import formatting as fmt

frame_height = 9.5
frame_width = 10.0
frame_spacing = 0.2
frame_roundness = 0.6
frame_line_width = 4.5 * fmt.standard_line_width
module_height = 1.6
module_width = 2.8
io_height = 0.40
io_long_side = 0.9
io_short_side = 1.0 * io_long_side
io_spacing = 0.12
p_height = 1.2 * io_height
p_width = 1.2
p_spacing = io_spacing / 2.0
h_width = 1 * p_width
h_height = 1.3 * p_height
h_spacing = io_spacing / 2.0
io_corner_roundness = 0.0
module_roundness = 0.0
line_width = 2.0 * fmt.standard_line_width
module_inner_vertical_spacing = 0.1
delta_increment = 0.0

horizontal_module_spacing = 0.2
vertical_module_spacing = 0.2
spacing_between_module_and_hyperp = 0.8
spacing_between_hyperp_and_hyperp = 0.4
arrow_length = vertical_module_spacing

name2color = fmt.google_slides_named_colors()

connect_s_fmt = fmt.combine_tikz_strs(
    [fmt.arrow_heads("end"), fmt.line_width(line_width)])

input_s_fmt = fmt.combine_tikz_strs([
    fmt.line_width(line_width),
])

output_s_fmt = fmt.combine_tikz_strs([
    fmt.line_width(line_width),
])

property_s_fmt = fmt.combine_tikz_strs([
    fmt.line_width(line_width),
])

module_s_fmt = fmt.combine_tikz_strs([
    fmt.line_width(line_width),
])

hyperp_s_fmt = fmt.combine_tikz_strs([
    fmt.line_width(line_width),
])

frame_s_fmt = fmt.combine_tikz_strs([
    fmt.rounded_corners(frame_roundness),
    fmt.line_width(frame_line_width),
])

unassigned_h_s_fmt = fmt.combine_tikz_strs([
    fmt.anchor("left_center"),
])

assigned_h_s_fmt = fmt.combine_tikz_strs([
    fmt.anchor("left_center"),
])


def input(name):
    x1 = io_short_side / 2.0
    x2 = io_long_side / 2.0
    r = stz.closed_path([[-x1, io_height], [x1, io_height], [x2, 0], [-x2, 0]],
                        input_s_fmt)
    l = stz.latex(stz.center_coords(r), name)
    return [r, l]


def output(name):
    x1 = io_long_side / 2.0
    x2 = io_short_side / 2.0
    r = stz.closed_path([[-x1, io_height], [x1, io_height], [x2, 0], [-x2, 0]],
                        output_s_fmt)
    l = stz.latex(stz.center_coords(r), name)
    return [r, l]


def property(name, width_scale=1.0, height_scale=1.0):
    e = stz.ellipse([0, 0], width_scale * p_width / 2.0,
                    height_scale * p_height / 2.0, property_s_fmt)
    l = stz.latex(stz.center_coords(e), name)
    return [e, l]


def module(module_name,
           input_names,
           output_names,
           hyperp_names,
           p_width_scale=1.0):

    i_lst = [input(s) for s in input_names]
    o_lst = [output(s) for s in output_names]
    m = stz.rectangle([0, 0], [module_width, -module_height], module_s_fmt)
    l = stz.latex(stz.center_coords(m), "\\textbf{%s}" % module_name)

    stz.distribute_horizontally_with_spacing(i_lst, io_spacing)
    stz.translate_bbox_top_left_to_coords(
        i_lst, [module_inner_vertical_spacing, -module_inner_vertical_spacing])
    stz.distribute_horizontally_with_spacing(o_lst, io_spacing)
    stz.translate_bbox_bottom_left_to_coords(o_lst, [
        module_inner_vertical_spacing,
        -module_height + module_inner_vertical_spacing
    ])

    if len(hyperp_names) > 0:
        h_lst = [property(s, p_width_scale) for s in hyperp_names]
        stz.distribute_vertically_with_spacing(h_lst, p_spacing)
        stz.translate_bbox_top_right_to_coords(h_lst, [
            module_width - module_inner_vertical_spacing,
            -module_inner_vertical_spacing - delta_increment
        ])
        return [[m, l], i_lst, o_lst, h_lst]
    else:
        return [[m, l], i_lst, o_lst]


def independent_hyperparameter(name, values_expr, value=None):

    e = stz.ellipse([0, 0], h_width / 2.0, h_height / 2.0, hyperp_s_fmt)
    l = stz.latex(stz.center_coords(e), "\\textbf{%s}" % name)
    fn_cs = stz.coords_from_bbox_with_fn(e, stz.right_center_coords)
    if value is None:
        l_vs = stz.latex(fn_cs, "\\textbf{[%s]}" % (values_expr,),
                         unassigned_h_s_fmt)
        return [e, l, l_vs]
    else:
        v_cs = stz.coords_from_bbox_with_fn(e, stz.right_center_coords)
        l_v = stz.latex(v_cs, "\\textbf{%s}" % value, assigned_h_s_fmt)
        return [e, l, l_v]


def dependent_hyperparameter(name, hyperp_names, fn_expr, value=None):
    e = stz.ellipse([0, 0], h_width / 2.0, h_height / 2.0, hyperp_s_fmt)
    if value is None:
        e["horizontal_radius"] *= 2.1 * e["horizontal_radius"]

    l_cs = stz.center_coords(e)
    if value is None:
        l_cs = stz.translate_coords_horizontally(l_cs, 0.1)
    l = stz.latex(l_cs, "\\textbf{%s}" % name)

    if value is None:
        fn_cs = stz.coords_from_bbox_with_fn(e, stz.right_center_coords)
        l_fn = stz.latex(fn_cs, "\\textbf{fn: %s}" % (fn_expr,),
                         unassigned_h_s_fmt)

        p = property("x", 0.25, 0.7)
        p_cs = stz.translate_coords_horizontally(
            stz.coords_from_bbox_with_fn(e, stz.left_center_coords), 0.1)
        stz.translate_bbox_left_center_to_coords(p, p_cs)
        return [e, l, l_fn, p]
    else:
        v_cs = stz.coords_from_bbox_with_fn(e, stz.right_center_coords)
        l_v = stz.latex(v_cs, "\\textbf{%s}" % value, assigned_h_s_fmt)
        return [e, l, l_v]


def dense(idx):
    return module("Dense-%d" % idx, ["in"], ["out"], ["units"])


def conv2d(idx):
    return module("Conv2D-%d" % idx, ["in"], ["out"], ["filters"], 1.1)


def dropout(idx):
    return module("Dropout-%d" % idx, ["in"], ["out"], ["prob"], 0.9)


def optional(idx):
    return module("Optional-%d" % idx, ["in"], ["out"], ["opt"])


def concat(idx):
    return module("Concat-%d" % idx, ["in0", "in1"], ["out"], [])


def repeat(idx):
    return module("Repeat-%d" % idx, ["in"], ["out"], ["k"], 0.5)


def connect_modules(m_from, m_to, output_idx, input_idx):
    return stz.line_segment(
        stz.coords_from_bbox_with_fn(m_from[2][output_idx],
                                     stz.bottom_center_coords),
        stz.coords_from_bbox_with_fn(m_to[1][input_idx], stz.top_center_coords),
        connect_s_fmt)


def connect_hyperp_to_module(h, m, property_idx):
    return stz.line_segment(
        stz.coords_from_bbox_with_fn(h[:2], stz.left_center_coords),
        stz.coords_from_bbox_with_fn(m[3][property_idx],
                                     stz.right_center_coords), connect_s_fmt)


def connect_hyperp_to_hyperp(h_from, h_to):
    return stz.line_segment(
        stz.coords_from_bbox_with_fn(h_from[:2], stz.right_center_coords),
        stz.coords_from_bbox_with_fn(h_to[3], stz.top_center_coords),
        connect_s_fmt)


def frame(frame_idx):
    assert frame_idx >= 0 and frame_idx <= 3
    c1 = conv2d(1)
    o = optional(1)
    r1 = repeat(1)
    r2 = repeat(2)
    cc = concat(1)
    c2 = conv2d(2)
    c3 = conv2d(3)
    c4 = conv2d(4)
    d = dropout(1)

    stz.distribute_horizontally_with_spacing([r1, r2],
                                             horizontal_module_spacing)
    stz.distribute_horizontally_with_spacing([c2, [c3, c4]],
                                             horizontal_module_spacing)

    modules = []
    if frame_idx == 0:
        stz.distribute_vertically_with_spacing([cc, [r1, r2], o, c1][::-1],
                                               vertical_module_spacing)

        stz.align_centers_horizontally([cc, [r1, r2], o, c1], 0)
        modules.extend([c1, o, r1, r2, cc])

    else:
        stz.distribute_vertically_with_spacing([c3, c4],
                                               vertical_module_spacing)
        stz.distribute_horizontally_with_spacing([c2, [c3, c4]],
                                                 horizontal_module_spacing)
        stz.align_centers_vertically([c2, [c3, c4]], 0)

        if frame_idx == 1:
            stz.distribute_vertically_with_spacing(
                [cc, [c2, c3, c4], o, c1][::-1], vertical_module_spacing)
            stz.align_centers_horizontally([cc, [c2, c3, c4], o, c1], 0)
            modules.extend([c1, o, c2, c3, c4, cc])

        else:
            stz.distribute_vertically_with_spacing(
                [cc, [c2, c3, c4], d, c1][::-1], vertical_module_spacing)
            stz.align_centers_horizontally([cc, [c2, c3, c4], d, c1], 0)
            modules.extend([c1, d, c2, c3, c4, cc])

    module_connections = []
    if frame_idx == 0:
        module_connections.extend([
            connect_modules(c1, o, 0, 0),
            connect_modules(o, r1, 0, 0),
            connect_modules(o, r2, 0, 0),
            connect_modules(r1, cc, 0, 0),
            connect_modules(r2, cc, 0, 1),
        ])

    else:
        if frame_idx == 1:
            module_connections.extend([
                connect_modules(c1, o, 0, 0),
                connect_modules(o, c2, 0, 0),
                connect_modules(o, c3, 0, 0),
            ])
        else:
            module_connections.extend([
                connect_modules(c1, d, 0, 0),
                connect_modules(d, c2, 0, 0),
                connect_modules(d, c3, 0, 0),
            ])

        module_connections.extend([
            connect_modules(c3, c4, 0, 0),
            connect_modules(c2, cc, 0, 0),
            connect_modules(c4, cc, 0, 1),
        ])

    # # hyperparameters
    if frame_idx <= 1:
        h_o = independent_hyperparameter("IH-2", "0, 1")
    else:
        h_o = independent_hyperparameter("IH-2", "0, 1", "1")

    if frame_idx <= 0:
        h_r1 = dependent_hyperparameter("DH-1", ["x"], "2*x")
        h_r2 = independent_hyperparameter("IH-3", "1, 2, 4")
    else:
        h_r1 = dependent_hyperparameter("DH-1", ["x"], "2*x", "2")
        h_r2 = independent_hyperparameter("IH-3", "1, 2, 4", "1")

    if frame_idx <= 2:
        h_c1 = independent_hyperparameter("IH-1", "64, 128")
        h_c2 = independent_hyperparameter("IH-4", "64, 128")
        h_c3 = independent_hyperparameter("IH-5", "64, 128")
        h_c4 = independent_hyperparameter("IH-6", "64, 128")
        h_d = independent_hyperparameter("IH-7", "0.25, 0.5")
    else:
        h_c1 = independent_hyperparameter("IH-1", "64, 128", "64")
        h_c2 = independent_hyperparameter("IH-4", "64, 128", "128")
        h_c3 = independent_hyperparameter("IH-5", "64, 128", "128")
        h_c4 = independent_hyperparameter("IH-6", "64, 128", "64")
        h_d = independent_hyperparameter("IH-7", "0.25, 0.5", "0.5")

    def place_hyperp_right_of(h, m):
        y_p = stz.center_coords(m[3])[1]
        stz.align_centers_vertically([h], y_p)
        stz.place_to_the_right(h, m, spacing_between_module_and_hyperp)

    hyperparameters = []
    place_hyperp_right_of(h_c1, c1)
    if frame_idx in [0, 1]:
        place_hyperp_right_of(h_o, o)
        hyperparameters.append(h_o)

    if frame_idx == 0:
        place_hyperp_right_of(h_r1, r2)
        stz.place_above_and_align_to_the_right(h_r2, h_r1, 0.8)
        hyperparameters.extend([h_r1, h_r2, h_c1])
    else:
        place_hyperp_right_of(h_c1, c1)
        place_hyperp_right_of(h_c3, c3)
        place_hyperp_right_of(h_c4, c4)
        stz.place_below(h_c2, h_c1, 3.0)
        hyperparameters.extend([h_c1, h_c2, h_c3, h_c4])

        if frame_idx in [2, 3]:
            place_hyperp_right_of(h_d, d)
            hyperparameters.extend([h_d])

    unreachable_hyperps = []
    if frame_idx == 1:
        stz.distribute_vertically_with_spacing([h_r1, h_r2], 0.2)
        unreachable_hyperps.extend([h_r1, h_r2])
    if frame_idx >= 2:
        stz.distribute_vertically_with_spacing([h_o, h_r1, h_r2], 0.2)
        unreachable_hyperps.extend([h_r1, h_r2, h_o])
    hyperparameters.extend(unreachable_hyperps)

    cs_fn = lambda e: stz.coords_from_bbox_with_fn(e, stz.left_center_coords)
    if frame_idx == 0:

        stz.translate_bbox_left_center_to_coords(h_r2, cs_fn([h_o, h_r1]))
    elif frame_idx == 1:
        stz.translate_bbox_left_center_to_coords(h_c2, cs_fn([h_o, h_c3]))
    else:
        stz.translate_bbox_left_center_to_coords(h_c2, cs_fn([h_d, h_c3]))

    hyperp_connections = [
        connect_hyperp_to_module(h_c1, c1, 0),
    ]
    if frame_idx in [0, 1]:
        hyperp_connections.extend([connect_hyperp_to_module(h_o, o, 0)])
    if frame_idx == 0:
        hyperp_connections.extend([
            connect_hyperp_to_module(h_r1, r2, 0),
            connect_hyperp_to_module(h_r2, r1, 0),
            connect_hyperp_to_hyperp(h_r2, h_r1)
        ])
    else:
        hyperp_connections.extend([
            connect_hyperp_to_module(h_c2, c2, 0),
            connect_hyperp_to_module(h_c3, c3, 0),
            connect_hyperp_to_module(h_c4, c4, 0),
        ])
        if frame_idx in [2, 3]:
            hyperp_connections.append(connect_hyperp_to_module(h_d, d, 0))

    f = stz.rectangle_from_width_and_height([0, 0], frame_height, frame_width,
                                            frame_s_fmt)
    e = [modules, module_connections, hyperparameters, hyperp_connections]
    stz.translate_bbox_center_to_coords(
        f, stz.translate_coords_horizontally(stz.center_coords(e), 0.8))
    if len(unreachable_hyperps) > 0:
        stz.translate_bbox_bottom_right_to_coords(unreachable_hyperps,
                                                  stz.bbox(e)[1])

    # frame id
    s = ["a", "b", "c", "d"][frame_idx]
    label = [stz.latex([0, 0], "\\Huge \\textbf %s" % s)]
    stz.translate_bbox_top_left_to_coords(
        label,
        stz.translate_coords_antidiagonally(
            stz.coords_from_bbox_with_fn(f, stz.top_left_coords), 0.6))

    return e + [f, label]


def search_space_transition():

    e0 = frame(0)
    e1 = frame(1)
    e2 = frame(2)
    e3 = frame(3)
    e = [e0, e1, e2, e3]

    def get_idx(e_frame, indices):
        e = e_frame
        for idx in indices:
            e = e[idx]
        return e

    def highlight(e_frame, indices, idx, color):
        e = get_idx(e_frame, indices)
        s_fmt = fmt.combine_tikz_strs([e["tikz_str"], fmt.fill_color(color)])
        e['tikz_str'] = s_fmt

    # highlight new modules
    highlight(e1, [0, 2, 0, 0], 0, "light_green_2")
    highlight(e1, [0, 3, 0, 0], 0, "light_green_2")
    highlight(e1, [0, 4, 0, 0], 0, "light_green_2")
    highlight(e2, [0, 1, 0, 0], 0, "light_green_2")

    # highlight new hyperparameters
    highlight(e1, [2, 2, 0], 0, "light_green_2")
    highlight(e1, [2, 3, 0], 0, "light_green_2")
    highlight(e1, [2, 4, 0], 0, "light_green_2")
    highlight(e2, [2, 4, 0], 0, "light_green_2")

    # highlight assigned hyperparameters
    highlight(e1, [2, 5, 0], 0, "light_red_2")
    highlight(e1, [2, 6, 0], 0, "light_red_2")
    highlight(e2, [2, 7, 0], 0, "light_red_2")
    highlight(e3, [2, 0, 0], 0, "light_red_2")
    highlight(e3, [2, 1, 0], 0, "light_red_2")
    highlight(e3, [2, 2, 0], 0, "light_red_2")
    highlight(e3, [2, 3, 0], 0, "light_red_2")
    highlight(e3, [2, 4, 0], 0, "light_red_2")

    # arrange the four frames
    stz.align_tops(e, 0.0)
    stz.distribute_horizontally_with_spacing([e0, e1], frame_spacing)
    stz.distribute_horizontally_with_spacing([e2, e3], frame_spacing)
    stz.distribute_vertically_with_spacing([[e0, e1], [e2, e3]], frame_spacing)

    stz.draw_to_tikz_standalone(e, "deep_architect.tex", name2color)


search_space_transition()
