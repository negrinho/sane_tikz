# reproduction of https://en.wikipedia.org/wiki/Binary_search_algorithm#/media/File:Binary_search_tree_search_4.svg

import sane_tikz.core as stz
import sane_tikz.formatting as fmt

node_radius = 0.30
vertical_node_spacing = 1.4 * node_radius
first_level_horizontal_node_spacing = 1.8
arrow_angle = 30.0
bbox_spacing = 0.1
label_spacing = 0.4
line_width = 1.2 * fmt.standard_line_width

s_lw = fmt.line_width(line_width)

fn = lambda expr: [
    stz.circle([0, 0], node_radius, s_lw),
    stz.latex([0, 0], expr)
]


def place(e, lst):
    delta = 0.0
    for i, sign in enumerate(lst):
        delta += sign * (node_radius + first_level_horizontal_node_spacing /
                         (2 * (i + 1.0)))
    stz.translate_horizontally(e, delta)


def connect(e_from, e_to, color_name="black"):
    s_fmt = fmt.combine_tikz_strs(
        [fmt.arrow_heads("end"),
         fmt.line_color(color_name), s_lw])
    from_cs = stz.center_coords(e_from)
    to_cs = stz.center_coords(e_to)
    out_angle = stz.vector_to_angle([from_cs, to_cs])
    in_angle = out_angle + 180.0
    return stz.line_segment_between_circles(from_cs, node_radius, out_angle,
                                            to_cs, node_radius, in_angle, s_fmt)


def dashed_bbox(e_lst):
    s_fmt = fmt.combine_tikz_strs([fmt.line_style("dashed"), s_lw])
    top_left_cs, bottom_right_cs = stz.bbox(e_lst)
    return stz.rectangle_from_additive_resizing(top_left_cs, bottom_right_cs,
                                                2.0 * bbox_spacing,
                                                2.0 * bbox_spacing, s_fmt)


def label_right(e, expr):
    cs = stz.coords_from_bbox_with_fn(e, stz.right_center_coords)
    cs = stz.translate_coords(cs, label_spacing, 0.1)
    return stz.latex(cs, "\\scriptsize{%s}" % expr)


def label_left(e, expr):
    cs = stz.coords_from_bbox_with_fn(e, stz.left_center_coords)
    cs = stz.translate_coords(cs, -label_spacing, 0.1)
    return stz.latex(cs, "\\scriptsize{%s}" % expr)


nodes = []
for i in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    if i == 4:
        s = "\\textbf{%s}" % str(i)
    else:
        s = str(i)
    nodes.append(fn(s))
stz.distribute_vertically_with_spacing(
    [nodes[0:1], nodes[1:3], nodes[3:6],
     nodes[6:9]][::-1], vertical_node_spacing)

place(nodes[1], [-1])
place(nodes[2], [1])
place(nodes[3], [-1, -1])
place(nodes[4], [-1, 1])
place(nodes[5], [1, 1])
place(nodes[6], [-1, 1, -1])
place(nodes[7], [-1, 1, 1])
place(nodes[8], [1, 1, -1])

connections = [
    connect(nodes[0], nodes[1], "blue"),
    connect(nodes[0], nodes[2]),
    connect(nodes[1], nodes[3]),
    connect(nodes[1], nodes[4], "blue"),
    connect(nodes[2], nodes[5]),
    connect(nodes[4], nodes[6], "blue"),
    connect(nodes[4], nodes[7]),
    connect(nodes[5], nodes[8]),
]

nodes[-3][0]["tikz_str"] = fmt.combine_tikz_strs(
    [nodes[-3][0]["tikz_str"],
     fmt.line_and_fill_colors("mygreen", "mygreen")])
nodes[-3][1]["tikz_str"] = fmt.combine_tikz_strs(
    [nodes[-3][0]["tikz_str"], "text=white"])

bb1 = dashed_bbox([nodes[6]])
bb2 = dashed_bbox([bb1, nodes[4], nodes[7]])
bb3 = dashed_bbox([bb2, nodes[1], nodes[3]])
bboxes = [bb1, bb2, bb3]

labels = [
    label_left(nodes[0], "4 < 8"),
    label_left(nodes[1], "4 > 3"),
    label_left(nodes[4], "4 < 6"),
]

name2color = {"mygreen": (2, 129, 0)}

e = [nodes, connections, bboxes, labels]
stz.draw_to_tikz_standalone(e, "tree.tex", name2color)