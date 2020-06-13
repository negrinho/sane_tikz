import sane_tikz as stz
import formatting as fmt

horizontal_node_spacing = 2.0
vertical_node_spacing = 0.8
node_radius = 0.36
filled_node_radius = 0.08
rectangle_roundness = 0.1
rectangle_width = 1.4
vertical_rectangle_distance = 0.8
horizontal_rectangle_distance = 1.4
triangle_angle_delta = 40
triangle_radius = node_radius
vd = vertical_rectangle_distance
hd = horizontal_rectangle_distance


def node(label):
    return [stz.circle([0, 0], node_radius), stz.latex([0, 0], label)]


def small_node(cs):
    s_fmt = fmt.fill_color('black')
    return stz.circle(cs, filled_node_radius, s_fmt)


def small_node_relative(e_from, e_to, alpha=0.5):
    from_cs = stz.center_coords(e_from)
    to_cs = stz.center_coords(e_to)
    cs = stz.convex_combination_coords(from_cs, to_cs, alpha)
    return small_node(cs)


def connect_nodes(e_from, e_to):
    cs_from = stz.center_coords(e_from)
    cs_to = stz.center_coords(e_to)
    angle = stz.vector_to_angle([cs_from, cs_to])
    return stz.line_segment_between_circles(cs_from, node_radius, angle, cs_to,
                                            node_radius, angle + 180.0)


def connect_small_node_to_node(e_small_from, e_to):
    cs_from = stz.center_coords(e_small_from)
    cs_to = stz.center_coords(e_to)
    angle = stz.vector_to_angle([cs_from, cs_to])
    return stz.line_segment_between_circles(cs_from, filled_node_radius, angle,
                                            cs_to, node_radius, angle + 180.0)


def label_small_node(label, e_small, angle, distance, label_width):
    s_fmt = fmt.combine_tikz_strs([
        fmt.rounded_corners(rectangle_roundness),
        fmt.fill_color_with_no_line('gray!20')
    ])
    s_fmt_t = fmt.fill_color_with_no_line('gray!20')
    r = stz.rectangle_from_width_and_height([0, 0], 1.8 * node_radius,
                                            label_width, s_fmt)
    cs = stz.center_coords(e_small)
    cs_label = stz.coords_on_circle(cs, distance, angle)
    stz.translate_bbox_center_to_coords(r, cs_label)
    l = stz.latex(cs_label, label)
    t = stz.closed_path([
        stz.coords_on_circle(cs, filled_node_radius, angle), cs_label,
        stz.coords_on_circle(cs_label, triangle_radius,
                             angle + 180.0 + triangle_angle_delta)
    ], s_fmt_t)
    return [r, t, l]


def figure_a():
    x1 = node("$x_1$")
    x2 = node("$x_2$")
    x3 = node("$x_3$")
    stz.distribute_horizontally_with_spacing([x1, x2, x3],
                                             horizontal_node_spacing)
    nodes = [x1, x2, x3]

    c1 = small_node_relative(x1, x2)
    c2 = small_node_relative(x2, x3)
    c3 = small_node([0, 0])
    stz.place_to_the_left_and_align_to_the_center(
        c3, x1, horizontal_node_spacing / 2.0 - filled_node_radius)
    small_nodes = [c1, c2, c3]
    small_nodes.extend([small_node([0, 0]) for _ in range(3)])
    stz.distribute_centers_horizontally_with_spacing(
        small_nodes[-3:], horizontal_node_spacing + 2.0 * node_radius)
    stz.place_below_and_align_to_the_center(small_nodes[-3:], nodes,
                                            vertical_node_spacing)

    x1_x2 = connect_nodes(x1, x2)
    x2_x3 = connect_nodes(x2, x3)
    x1_c3 = connect_small_node_to_node(c3, x1)
    connections = [x1_x2, x2_x3, x1_c3]
    connections.extend([
        connect_small_node_to_node(small_nodes[-3 + i], nodes[i])
        for i in range(3)
    ])

    labels = [
        label_small_node("$p(x_1)$", c3, 90.0, vd, rectangle_width),
        label_small_node("$l(x_1; z_1)$", small_nodes[3], 0.0, hd,
                         rectangle_width),
        label_small_node("$p(x_3 | x_2)$", c2, 90.0, vd, rectangle_width)
    ]

    return [nodes, small_nodes, connections, labels]


def figure_b():
    x1 = node("$x_1$")
    x2 = node("$x_2$")
    x3 = node("$x_3$")
    stz.distribute_horizontally_with_spacing([x1, x2, x3],
                                             horizontal_node_spacing)
    nodes = [x1, x2, x3]

    c1 = small_node_relative(x1, x2)
    c2 = small_node_relative(x2, x3)
    c3 = small_node([0, 0])
    stz.place_to_the_left_and_align_to_the_center(
        c3, x1, horizontal_node_spacing / 2.0 - filled_node_radius)
    small_nodes = [c1, c2, c3]
    small_nodes.extend([small_node([0, 0]) for _ in range(3)])
    stz.distribute_centers_horizontally_with_spacing(
        small_nodes[-3:], horizontal_node_spacing + 2.0 * node_radius)
    stz.place_below_and_align_to_the_center(small_nodes[-3:], nodes,
                                            vertical_node_spacing)

    x1_x2 = connect_nodes(x1, x2)
    x2_x3 = connect_nodes(x2, x3)
    x1_c3 = connect_small_node_to_node(c3, x1)
    connections = [x1_x2, x2_x3, x1_c3]
    connections.extend([
        connect_small_node_to_node(small_nodes[-3 + i], nodes[i])
        for i in range(3)
    ])

    # for qs
    q1 = node("$q_1$")
    q2 = node("$q_2$")
    q3 = node("$q_3$")
    stz.distribute_horizontally_with_spacing([q1, q2, q3],
                                             horizontal_node_spacing)
    nodes.extend([q1, q2, q3])
    stz.place_above_and_align_to_the_center([q1, q2, q3], [x1, x2, x3],
                                            vertical_node_spacing)

    qc1 = small_node_relative(q1, q2)
    qc2 = small_node_relative(q2, q3)
    qc3 = small_node([0, 0])
    stz.place_to_the_left_and_align_to_the_center(
        qc3, q1, horizontal_node_spacing / 2.0 - filled_node_radius)
    small_nodes.extend([qc1, qc2, qc3])

    q1_q2 = connect_nodes(q1, q2)
    q2_q3 = connect_nodes(q2, q3)
    q1_qc3 = connect_small_node_to_node(qc3, q1)
    connections.extend([q1_q2, q2_q3, q1_qc3])
    connections.extend(
        [connect_nodes(e1, e2) for e1, e2 in zip([x1, x2, x3], [q1, q2, q3])])

    labels = [
        label_small_node("$p(q_1)$", qc3, -90.0, vd, rectangle_width),
        label_small_node("$p(q_2| q_3)$", qc2, -90.0, vd, rectangle_width),
    ]

    return [nodes, small_nodes, connections, labels]


def figure_c():
    x1 = node("$x_1$")
    x2 = node("$x_2$")
    x3 = node("$x_3$")
    stz.distribute_horizontally_with_spacing([x1, x2, x3],
                                             horizontal_node_spacing)
    nodes = [x1, x2, x3]

    c1 = small_node_relative(x1, x2)
    c2 = small_node_relative(x2, x3)
    small_nodes = [c1, c2]
    small_nodes.extend([small_node([0, 0]) for _ in range(3)])
    stz.distribute_centers_horizontally_with_spacing(
        small_nodes[-3:], horizontal_node_spacing + 2.0 * node_radius)
    stz.place_below_and_align_to_the_center(small_nodes[-3:], nodes,
                                            vertical_node_spacing)

    x1_x2 = connect_nodes(x1, x2)
    x2_x3 = connect_nodes(x2, x3)
    connections = [x1_x2, x2_x3]
    connections.extend([
        connect_small_node_to_node(small_nodes[-3 + i], nodes[i])
        for i in range(3)
    ])

    u1 = node("$u_1$")
    u2 = node("$u_2$")
    nodes.extend([u1, u2])
    for u, c in zip([u1, u2], [c1, c2]):
        cx = small_node([0, 0])
        stz.place_above_and_align_to_the_center(
            u, c, vertical_node_spacing - node_radius)
        stz.place_above_and_align_to_the_center(
            cx, u, vertical_node_spacing - node_radius)
        connections.extend([
            connect_small_node_to_node(c, u),
            connect_small_node_to_node(cx, u)
        ])
        small_nodes.append(cx)

    labels = [
        label_small_node("$J_x(x_1)$", small_nodes[2], 0.0, hd,
                         rectangle_width),
        label_small_node("$J_u(u_1)$", small_nodes[5], 0.0, hd,
                         rectangle_width),
        label_small_node("$p(x_3| x_2, u_2)$", small_nodes[1], -90.0, vd,
                         1.4 * rectangle_width)
    ]

    return [nodes, small_nodes, connections, labels]


def figure_d():
    x1 = node("$T_1$")
    x2 = node("$T_2$")
    x3 = node("$T_3$")
    stz.distribute_horizontally_with_spacing([x1, x2, x3],
                                             horizontal_node_spacing)
    nodes = [x1, x2, x3]

    c1 = small_node_relative(x1, x2)
    c2 = small_node_relative(x2, x3)
    c3 = small_node([0, 0])
    stz.place_to_the_left_and_align_to_the_center(
        c3, x1, horizontal_node_spacing / 2.0 - filled_node_radius)
    small_nodes = [c1, c2, c3]

    connections = [
        connect_nodes(x1, x2),
        connect_nodes(x2, x3),
        connect_small_node_to_node(c3, x1),
    ]

    x4 = node("$T_4$")
    x5 = node("$T_5$")
    stz.distribute_horizontally_with_spacing([x5, x4], horizontal_node_spacing)
    stz.place_above_and_align_to_the_center([x5, x4], [x2, x3],
                                            vertical_node_spacing)
    nodes.extend([x4, x5])

    connections.extend([
        connect_nodes(x2, x5),
        connect_nodes(x3, x4),
        connect_nodes(x4, x5),
    ])

    small_nodes.extend([
        small_node_relative(x2, x5),
        small_node_relative(x3, x4),
        small_node_relative(x4, x5)
    ])

    labels = [
        label_small_node("$f_p(T_1)$", c3, 90.0, vd, rectangle_width),
        label_small_node("$f_l(T_5, T_2)$", small_nodes[-3], 180.0, hd,
                         1.25 * rectangle_width),
        label_small_node("$f_b(T_4, T_5)$", small_nodes[-1], -90.0, vd,
                         1.25 * rectangle_width)
    ]

    return [nodes, small_nodes, connections, labels]


def figure_e():
    x1 = node("$T_1$")
    x2 = node("$T_2$")
    x3 = node("$T_3$")
    stz.distribute_horizontally_with_spacing([x1, x2, x3],
                                             horizontal_node_spacing)
    nodes = [x1, x2, x3]

    c1 = small_node_relative(x1, x2)
    c2 = small_node_relative(x2, x3)
    c3 = small_node([0, 0])
    stz.place_to_the_left_and_align_to_the_center(
        c3, x1, horizontal_node_spacing / 2.0 - filled_node_radius)
    small_nodes = [c1, c2, c3]

    connections = [
        connect_nodes(x1, x2),
        connect_nodes(x2, x3),
        connect_small_node_to_node(c3, x1),
    ]

    x4 = node("$l_4$")
    x5 = node("$l_5$")
    stz.distribute_horizontally_with_spacing([x5, x4], horizontal_node_spacing)
    stz.place_above_and_align_to_the_center([x5, x4], [x2],
                                            vertical_node_spacing)
    nodes.extend([x4, x5])

    connections.extend([
        connect_nodes(x1, x5),
        connect_nodes(x2, x5),
        connect_nodes(x2, x4),
        connect_nodes(x3, x4),
        connect_nodes(x1, x4),
    ])

    small_nodes.extend([
        small_node_relative(x1, x5, 0.6),
        small_node_relative(x2, x5, 0.6),
        small_node_relative(x2, x4, 0.6),
        small_node_relative(x3, x4, 0.6),
        small_node_relative(x1, x4, 0.6),
    ])

    labels = [
        label_small_node("$f_{br}(T_1, l_5)$", small_nodes[-5], 135.0, hd,
                         1.4 * rectangle_width)
    ]

    return [nodes, small_nodes, connections, labels]


def figure_f():
    x1 = node("$C_1$")
    x2 = node("$C_2$")
    x3 = node("$C_3$")
    stz.distribute_horizontally_with_spacing([x1, x2, x3],
                                             horizontal_node_spacing)
    nodes = [x1, x2, x3]

    small_nodes = []
    connections = []

    x4 = node("$p_4$")
    x5 = node("$p_5$")
    stz.distribute_horizontally_with_spacing([x5, x4], horizontal_node_spacing)
    stz.place_above_and_align_to_the_center([x5, x4], [x2],
                                            vertical_node_spacing)
    nodes.extend([x4, x5])

    connections.extend([
        connect_nodes(x1, x5),
        connect_nodes(x2, x5),
        connect_nodes(x2, x4),
        connect_nodes(x3, x4),
        connect_nodes(x1, x4),
    ])

    small_nodes.extend([
        small_node_relative(x1, x5, 0.6),
        small_node_relative(x2, x5, 0.6),
        small_node_relative(x2, x4, 0.6),
        small_node_relative(x3, x4, 0.6),
        small_node_relative(x1, x4, 0.6),
    ])

    labels = [
        label_small_node("$f_{rp}(C_1, p_5)$", small_nodes[-5], 135.0, hd,
                         1.4 * rectangle_width)
    ]

    return [nodes, small_nodes, connections, labels]


e = [
    figure_a(),
    figure_b(),
    figure_c(),
    figure_d(),
    figure_e(),
    figure_f(),
]
stz.distribute_vertically_with_spacing(e[:3][::-1], 2.0)
stz.distribute_vertically_with_spacing(e[3:][::-1], 2.0)
stz.distribute_horizontally_with_spacing([e[:3], e[3:]], 2.0)

stz.draw_to_tikz_standalone(e, "factor_graphs.tex")
