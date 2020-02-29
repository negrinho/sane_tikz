# -*- coding: utf-8 -*-

import math
from copy import deepcopy
from pprint import pprint

#### overview
# - all angles in degrees unless stated otherwise.
# - all dimensions in cm (even for line width).
# cs = [x, y], vec = [start_cs, end_cs]

# nice constants:
golden_ratio = 1.61803398875

#### auxiliary functions for color and dimension conversions


def pt_to_cm(size_in_pt):
    return 0.0352778 * size_in_pt


def cm_to_pt(size_in_cm):
    return size_in_cm / 0.0352778


def degrees_to_radians(angle):
    return angle * ((2.0 * math.pi) / 360.0)


def radians_to_degrees(angle):
    return angle * (360.0 / (2.0 * math.pi))


def normalize_angle_to_standard_interval(angle):
    multiplier = math.floor(angle / 360.0)
    angle = angle - multiplier * 360.0
    return angle


def rgb_to_hex(color_in_rgb):
    raise NotImplementedError


def hex_to_rgb(color_in_hex):
    raise NotImplementedError


#### for coordinates and vectors
def midway_coords(start_cs, end_cs):
    return [
        start_cs[0] / 2.0 + end_cs[0] / 2.0, start_cs[1] / 2.0 + end_cs[1] / 2.0
    ]


def one_third_coords(start_cs, end_cs):
    return [
        2.0 * start_cs[0] / 3.0 + end_cs[0] / 3.0,
        2.0 * start_cs[1] / 3.0 + end_cs[1] / 3.0
    ]


def two_thirds_coords(start_cs, end_cs):
    return [
        start_cs[0] / 3.0 + 2.0 * end_cs[0] / 3.0,
        start_cs[1] / 3.0 + 2.0 * end_cs[1] / 3.0
    ]


def top_left_coords(cs, other_cs):
    return [min(cs[0], other_cs[0]), max(cs[1], other_cs[1])]


def top_right_coords(cs, other_cs):
    return [max(cs[0], other_cs[0]), max(cs[1], other_cs[1])]


def bottom_left_coords(cs, other_cs):
    return [min(cs[0], other_cs[0]), min(cs[1], other_cs[1])]


def bottom_right_coords(cs, other_cs):
    return [max(cs[0], other_cs[0]), min(cs[1], other_cs[1])]


def left_center_coords(cs, other_cs):
    top_left_cs = top_left_coords(cs, other_cs)
    bottom_left_cs = bottom_left_coords(cs, other_cs)
    return midway_coords(top_left_cs, bottom_left_cs)


def right_center_coords(cs, other_cs):
    top_right_cs = top_right_coords(cs, other_cs)
    bottom_right_cs = bottom_right_coords(cs, other_cs)
    return midway_coords(top_right_cs, bottom_right_cs)


def top_center_coords(cs, other_cs):
    top_left_cs = top_left_coords(cs, other_cs)
    top_right_cs = top_right_coords(cs, other_cs)
    return midway_coords(top_left_cs, top_right_cs)


def bottom_center_coords(cs, other_cs):
    bottom_left_cs = bottom_left_coords(cs, other_cs)
    bottom_right_cs = bottom_right_coords(cs, other_cs)
    return midway_coords(bottom_left_cs, bottom_right_cs)


def convex_combination_coords(from_cs, to_cs, alpha):
    return [(1.0 - alpha) * from_cs[0] + alpha * to_cs[0],
            (1.0 - alpha) * from_cs[1] + alpha * to_cs[1]]


def translate_coords(cs, delta_x, delta_y):
    return [cs[0] + delta_x, cs[1] + delta_y]


def translate_coords_horizontally(cs, delta):
    return [cs[0] + delta, cs[1]]


def translate_coords_vertically(cs, delta):
    return [cs[0], cs[1] + delta]


def translate_coords_diagonally(cs, delta):
    return [cs[0] + delta, cs[1] + delta]


def translate_coords_antidiagonally(cs, delta):
    return [cs[0] + delta, cs[1] - delta]


def vector_to_deltax(vec):
    return vec[1][0] - vec[0][0]


def vector_to_deltay(vec):
    return vec[1][1] - vec[0][1]


def vector_to_deltas(vec):
    return [vector_to_deltax(vec), vector_to_deltay(vec)]


def deltas_to_angle(delta_x, delta_y):
    if delta_x == 0.0:
        angle = 90.0 if delta_y > 0.0 else -90.0
    else:
        angle = radians_to_degrees(math.atan(float(delta_y) / delta_x))
    if delta_x < 0.0:
        angle += 180.0
    return angle


def vector_to_angle(vec):
    delta_x, delta_y = vector_to_deltas(vec)
    return deltas_to_angle(delta_x, delta_y)


def rotate_vector(vec, axis_cs, angle):
    start_cs, end_cs = vec
    return [
        rotate_coords(start_cs, axis_cs, angle),
        rotate_coords(end_cs, axis_cs, angle)
    ]


def ortogonal_vector(vec):
    start_cs, end_cs = vec
    return [start_cs, rotate_coords(end_cs, start_cs, 90.0)]


def reflect_coords_horizontally(cs, axis_x):
    return (-(cs[0] - axis_x) + axis_x, cs[1])


def reflect_coords_vertically(cs, axis_y):
    return (cs[0], -(cs[1] - axis_y) + axis_y)


def reflect_vector_horizontally(vec, axis_x):
    start_cs, end_cs = vec
    return [
        reflect_coords_horizontally(start_cs, axis_x),
        reflect_coords_horizontally(end_cs, axis_x)
    ]


def reflect_vector_vertically(vec, axis_y):
    start_cs, end_cs = vec
    return [
        reflect_coords_vertically(start_cs, axis_y),
        reflect_coords_vertically(end_cs, axis_y)
    ]


# def reflect_coords_wrt_vector(cs, vec):
#     start_cs, end_cs = vec

#     delta_x, delta_y = start_cs
#     out_cs = translate_coords(cs, -delta_x, -delta_y)
#     # NOTE: this is unfinished.
#     raise NotImplementedError
#     out_cs = translate(out_cs, delta_x, delta_y)
#     return out_cs

# def reflect_vector_wrt_vector(vec, axis_vec):
#     start_cs, end_cs = vec
#     return [
#         reflect_coords_wrt_vector(start_cs, axis_vec),
#         reflect_coords_wrt_vector(end_cs, axis_vec)
#     ]


def x_difference(vec):
    start_cs, end_cs = vec
    return end_cs[0] - start_cs[0]


def y_difference(vec):
    start_cs, end_cs = vec
    return end_cs[1] - start_cs[1]


def x_length(vec):
    start_cs, end_cs = vec
    return abs(x_difference([start_cs, end_cs]))


def y_length(vec):
    start_cs, end_cs = vec
    return abs(y_difference([start_cs, end_cs]))


def length(vec):
    start_cs, end_cs = vec
    return math.sqrt(
        x_length([start_cs, end_cs])**2 + y_length([start_cs, end_cs])**2)


def scale_to_length(vec):
    raise NotImplementedError


def rotate_coords(cs, axis_cs, angle):
    x, y = cs
    x_axis, y_axis = axis_cs
    angle_in_rads = math.pi / 180.0 * angle
    c = math.cos(angle_in_rads)
    s = math.sin(angle_in_rads)
    x_recentered = (x - x_axis)
    y_recentered = (y - y_axis)
    x_out = x_axis + c * x_recentered - s * y_recentered
    y_out = y_axis + s * x_recentered + c * y_recentered
    return [x_out, y_out]


#### for composite elements
def bbox(e):
    if isinstance(e, list):
        assert len(e) > 0
        bboxes = [bbox(e_i) for e_i in e]
        # [[[top_x1, top_y1], [bottom_x1, bottom_y1]], ...]
        top_left_xs = [b[0][0] for b in bboxes]
        top_left_ys = [b[0][1] for b in bboxes]
        bottom_right_xs = [b[1][0] for b in bboxes]
        bottom_right_ys = [b[1][1] for b in bboxes]
        b_out = [[min(top_left_xs), max(top_left_ys)],
                 [max(bottom_right_xs),
                  min(bottom_right_ys)]]

    elif e["type"] == 'open_path' or e["type"] == "closed_path":
        xs = [cs[0] for cs in e["cs_lst"]]
        ys = [cs[1] for cs in e["cs_lst"]]
        b_out = [[min(xs), max(ys)], [max(xs), min(ys)]]

    # NOTE: this is not quite correct for circular arcs, but it is a convenient approximation.
    elif e["type"] == "circle" or e["type"] == "circular_arc":
        r = e["radius"]
        cs = e["center_cs"]
        return [[cs[0] - r, cs[1] + r], [cs[0] + r, cs[1] - r]]

    elif e["type"] == 'ellipse':
        rx = e["horizontal_radius"]
        ry = e["vertical_radius"]
        cs = e["center_cs"]
        return [[cs[0] - rx, cs[1] + ry], [cs[0] + rx, cs[1] - ry]]

    ### TODO: this is wrong, but simple for now.
    elif e["type"] == 'bezier':
        return (top_left_coords(e["from_cs"], e["to_cs"]),
                bottom_right_coords(e["from_cs"], e["to_cs"]))

    # NOTE: does not influence the bounding box (for simplicity)
    # TODO: optionally, make it part of text_width explicitly.
    elif e["type"] == "latex":
        return [e["cs"], e["cs"]]

    elif e["type"] == "image":
        return [
            e["top_left_cs"],
            translate_coords(e["top_left_cs"], e["width"], -e["height"])
        ]

    else:
        raise ValueError("bbox not implemented for element: %s." % e["type"])

    return b_out


def center_coords(e):
    return midway_coords(*bbox(e))


def coords_from_bbox_with_fn(e, fn):
    return fn(*bbox(e))


def translate(e, delta_x, delta_y):
    if isinstance(e, list):
        assert len(e) > 0
        for e_i in e:
            translate(e_i, delta_x, delta_y)

    elif e["type"] == 'open_path':
        e["cs_lst"] = [
            translate_coords(cs, delta_x, delta_y) for cs in e["cs_lst"]
        ]

    elif e["type"] == 'closed_path':
        e["cs_lst"] = [
            translate_coords(cs, delta_x, delta_y) for cs in e["cs_lst"]
        ]

    elif e["type"] == "circle":
        e["center_cs"] = translate_coords(e["center_cs"], delta_x, delta_y)

    elif e["type"] == 'ellipse':
        e["center_cs"] = translate_coords(e["center_cs"], delta_x, delta_y)

    elif e["type"] == 'bezier':
        e["from_cs"] = translate_coords(e["from_cs"], delta_x, delta_y)
        e["to_cs"] = translate_coords(e["to_cs"], delta_x, delta_y)
        e["c1_cs"] = translate_coords(e["c1_cs"], delta_x, delta_y)
        e["c2_cs"] = translate_coords(e["c2_cs"], delta_x, delta_y)

    elif e["type"] == "latex":
        e["cs"] = translate_coords(e["cs"], delta_x, delta_y)

    elif e["type"] == "image":
        e["top_left_cs"] = translate_coords(e["top_left_cs"], delta_x, delta_y)
    else:
        raise ValueError("tranlate not implemented for element: %s." %
                         e["type"])


# NOTE: this will move the center of the element. translate to get the appropriate
# center.
# TODO: test this function.
def scale(e, alpha):
    if isinstance(e, list):
        assert len(e) > 0
        for e_i in e:
            scale(e_i, alpha)

    elif e["type"] == 'open_path':
        e["cs_lst"] = [scale_coords(cs, alpha) for cs in e["cs_lst"]]

    elif e["type"] == 'closed_path':
        e["cs_lst"] = [scale_coords(cs, alpha) for cs in e["cs_lst"]]

    elif e["type"] == "circle":
        e["center_cs"] = scale_coords(e["center_cs"], alpha)
        e["radius"] *= alpha

    elif e["type"] == 'ellipse':
        e["center_cs"] = scale_coords(e["center_cs"], alpha)
        e["horizontal_radius"] *= alpha

    elif e["type"] == 'bezier':
        e["from_cs"] = scale_coords(e["from_cs"], alpha)
        e["to_cs"] = scale_coords(e["to_cs"], alpha)
        e["c1_cs"] = scale_coords(e["c1_cs"], alpha)
        e["c2_cs"] = scale_coords(e["c2_cs"], alpha)

    elif e["type"] == "latex":
        e["cs"] = scale_coords(e["cs"], alpha)

    elif e["type"] == "image":
        e["top_left_cs"] = scale_coords(e["top_left_cs"], alpha)
        e["width"] *= alpha
        e["height"] *= alpha
    else:
        raise ValueError("scale not implemented for element: %s." % e["type"])


def scale_coords(cs, alpha):
    return [alpha * x for x in cs]


def translate_horizontally(e, delta):
    translate(e, delta, 0)


def translate_vertically(e, delta):
    translate(e, 0, delta)


def translate_to_coords(e, from_cs, to_cs):
    delta_x, delta_y = vector_to_deltas([from_cs, to_cs])
    translate(e, delta_x, delta_y)


def translate_bbox_center_to_coords(e, cs):
    top_left_cs, bottom_right_cs = bbox(e)
    mid = midway_coords(top_left_cs, bottom_right_cs)
    translate_to_coords(e, mid, cs)


def translate_bbox_top_left_to_coords(e, cs):
    top_left_cs, _ = bbox(e)
    translate_to_coords(e, top_left_cs, cs)


def translate_bbox_bottom_left_to_coords(e, cs):
    top_left_cs, bottom_right_cs = bbox(e)
    bottom_left_cs = bottom_left_coords(top_left_cs, bottom_right_cs)
    translate_to_coords(e, bottom_left_cs, cs)


def translate_bbox_bottom_right_to_coords(e, cs):
    _, bottom_right_cs = bbox(e)
    translate_to_coords(e, bottom_right_cs, cs)


def translate_bbox_top_right_to_coords(e, cs):
    top_left_cs, bottom_right_cs = bbox(e)
    top_right_cs = top_right_coords(top_left_cs, bottom_right_cs)
    translate_to_coords(e, top_right_cs, cs)


def translate_bbox_top_center_to_coords(e, cs):
    top_left_cs, right_bottom_cs = bbox(e)
    top_center_cs = top_center_coords(top_left_cs, right_bottom_cs)
    translate_to_coords(e, top_center_cs, cs)


def translate_bbox_bottom_center_to_coords(e, cs):
    top_left_cs, right_bottom_cs = bbox(e)
    bottom_center_cs = bottom_center_coords(top_left_cs, right_bottom_cs)
    translate_to_coords(e, bottom_center_cs, cs)


def translate_bbox_left_center_to_coords(e, cs):
    top_left_cs, right_bottom_cs = bbox(e)
    left_center_cs = left_center_coords(top_left_cs, right_bottom_cs)
    translate_to_coords(e, left_center_cs, cs)


def translate_bbox_right_center_to_coords(e, cs):
    top_left_cs, bottom_right_cs = bbox(e)
    top_center_cs = right_center_coords(top_left_cs, bottom_right_cs)
    translate_to_coords(e, top_center_cs, cs)


def place_above(e, e_ref, spacing):
    y_ref = bbox(e_ref)[0][1]
    y = bbox(e)[1][1]
    delta = (y_ref - y) + spacing
    translate_vertically(e, delta)


def place_below(e, e_ref, spacing):
    y_ref = bbox(e_ref)[1][1]
    y = bbox(e)[0][1]
    delta = (y_ref - y) - spacing
    translate_vertically(e, delta)


def place_to_the_left(e, e_ref, spacing):
    x_ref = bbox(e_ref)[0][0]
    x = bbox(e)[1][0]
    delta = (x_ref - x) - spacing
    translate_horizontally(e, delta)


def place_to_the_right(e, e_ref, spacing):
    x_ref = bbox(e_ref)[1][0]
    x = bbox(e)[0][0]
    delta = (x_ref - x) + spacing
    translate_horizontally(e, delta)


# place with functions (flexible!)
def place_relative_to_at_angle_with_fns(e, e_ref, fn, fn_ref, out_angle,
                                        spacing):
    cs_ref = fn_ref(*bbox(e_ref))
    cs_to = coords_on_circle(cs_ref, spacing, out_angle)
    cs_from = fn(*bbox(e))
    translate_to_coords(e, cs_from, cs_to)


# place above
def place_above_and_align_to_the_left(e, e_ref, spacing):
    ref_cs = coords_from_bbox_with_fn(e_ref, top_left_coords)
    cs = translate_coords_vertically(ref_cs, spacing)
    translate_bbox_bottom_left_to_coords(e, cs)


def place_above_and_align_to_the_center(e, e_ref, spacing):
    ref_cs = coords_from_bbox_with_fn(e_ref, top_center_coords)
    cs = translate_coords_vertically(ref_cs, spacing)
    translate_bbox_bottom_center_to_coords(e, cs)


def place_above_and_align_to_the_right(e, e_ref, spacing):
    ref_cs = coords_from_bbox_with_fn(e_ref, top_right_coords)
    cs = translate_coords_vertically(ref_cs, spacing)
    translate_bbox_bottom_right_to_coords(e, cs)


# place below
def place_below_and_align_to_the_left(e, e_ref, spacing):
    ref_cs = coords_from_bbox_with_fn(e_ref, bottom_left_coords)
    cs = translate_coords_vertically(ref_cs, -spacing)
    translate_bbox_top_left_to_coords(e, cs)


def place_below_and_align_to_the_center(e, e_ref, spacing):
    ref_cs = coords_from_bbox_with_fn(e_ref, bottom_center_coords)
    cs = translate_coords_vertically(ref_cs, -spacing)
    translate_bbox_top_center_to_coords(e, cs)


def place_below_and_align_to_the_right(e, e_ref, spacing):
    ref_cs = coords_from_bbox_with_fn(e_ref, bottom_right_coords)
    cs = translate_coords_vertically(ref_cs, -spacing)
    translate_bbox_top_right_to_coords(e, cs)


# place to the left
def place_to_the_left_and_align_to_the_top(e, e_ref, spacing):
    ref_cs = coords_from_bbox_with_fn(e_ref, top_left_coords)
    cs = translate_coords_horizontally(ref_cs, -spacing)
    translate_bbox_top_right_to_coords(e, cs)


def place_to_the_left_and_align_to_the_center(e, e_ref, spacing):
    ref_cs = coords_from_bbox_with_fn(e_ref, left_center_coords)
    cs = translate_coords_horizontally(ref_cs, -spacing)
    translate_bbox_right_center_to_coords(e, cs)


def place_to_the_left_and_align_to_the_bottom(e, e_ref, spacing):
    ref_cs = coords_from_bbox_with_fn(e_ref, bottom_left_coords)
    cs = translate_coords_horizontally(ref_cs, -spacing)
    translate_bbox_bottom_right_to_coords(e, cs)


# place to the right
def place_to_the_right_and_align_to_the_top(e, e_ref, spacing):
    ref_cs = coords_from_bbox_with_fn(e_ref, top_right_coords)
    cs = translate_coords_horizontally(ref_cs, spacing)
    translate_bbox_top_left_to_coords(e, cs)


def place_to_the_right_and_align_to_the_center(e, e_ref, spacing):
    ref_cs = coords_from_bbox_with_fn(e_ref, right_center_coords)
    cs = translate_coords_horizontally(ref_cs, spacing)
    translate_bbox_left_center_to_coords(e, cs)


def place_to_the_right_and_align_to_the_bottom(e, e_ref, spacing):
    ref_cs = coords_from_bbox_with_fn(e_ref, bottom_right_coords)
    cs = translate_coords_horizontally(ref_cs, spacing)
    translate_bbox_bottom_left_to_coords(e, cs)


# left to right
def distribute_horizontally_with_spacing(e_lst, spacing):
    for i in range(1, len(e_lst)):
        e = e_lst[i]
        e_prev = e_lst[i - 1]
        cs = bbox(e)[0]
        cs_prev = bbox(e_prev)[1]
        delta_x = cs_prev[0] - cs[0] + spacing
        translate(e, delta_x, 0)


# bottom to top
def distribute_vertically_with_spacing(e_lst, spacing):
    for i in range(1, len(e_lst)):
        e = e_lst[i]
        e_prev = e_lst[i - 1]
        cs = bbox(e)[1]
        cs_prev = bbox(e_prev)[0]
        delta_y = cs_prev[1] - cs[1] + spacing
        translate(e, 0, delta_y)


def distribute_centers_horizontally_with_spacing(e_lst, spacing):
    for i in range(1, len(e_lst)):
        e = e_lst[i]
        e_prev = e_lst[i - 1]
        cs = midway_coords(*bbox(e))
        cs_prev = midway_coords(*bbox(e_prev))
        delta_x = cs_prev[0] - cs[0] + spacing
        translate(e, delta_x, 0)


def distribute_centers_vertically_with_spacing(e_lst, spacing):
    for i in range(1, len(e_lst)):
        e = e_lst[i]
        e_prev = e_lst[i - 1]
        cs = midway_coords(*bbox(e))
        cs_prev = midway_coords(*bbox(e_prev))
        delta_y = cs_prev[1] - cs[1] + spacing
        translate(e, 0, delta_y)


def align_centers_horizontally(e_lst, x):
    for e in e_lst:
        center_cs = center_coords(e)
        translate_horizontally(e, x - center_cs[0])


def align_centers_vertically(e_lst, y):
    for e in e_lst:
        center_cs = center_coords(e)
        translate_vertically(e, y - center_cs[1])


def align_centers_both(e_lst, x, y):
    align_centers_horizontally(e_lst, x)
    align_centers_vertically(e_lst, y)


def align_lefts(e_lst, x):
    for e in e_lst:
        top_left_cs, _ = bbox(e)
        translate_horizontally(e, x - top_left_cs[0])


def align_rights(e_lst, x):
    for e in e_lst:
        _, bottom_right_cs = bbox(e)
        translate_horizontally(e, x - bottom_right_cs[0])


def align_tops(e_lst, y):
    for e in e_lst:
        top_left_cs, _ = bbox(e)
        translate_vertically(e, y - top_left_cs[1])


def align_bottoms(e_lst, y):
    for e in e_lst:
        _, bottom_right_cs = bbox(e)
        translate_vertically(e, y - bottom_right_cs[1])


def copy(e):
    return deepcopy(e)


#### these are some of the graphical primitives used for drawing.
def line_segment(start_cs, end_cs, tikz_str=""):
    return open_path([start_cs, end_cs], tikz_str)


def horizontal_line_segment(start_cs, delta, tikz_str=""):
    end_cs = translate_coords_horizontally(start_cs, delta)
    return line_segment(start_cs, end_cs, tikz_str)


def vertical_line_segment(start_cs, delta, tikz_str=""):
    end_cs = translate_coords_vertically(start_cs, delta)
    return line_segment(start_cs, end_cs, tikz_str)


def centered_horizontal_line_segment(center_cs, length, tikz_str=""):
    delta = length / 2.0
    start_cs = translate_coords_horizontally(center_cs, delta)
    end_cs = translate_coords_horizontally(center_cs, -delta)
    return line_segment(start_cs, end_cs, tikz_str)


def centered_vertical_line_segment(center_cs, length, tikz_str=""):
    delta = length / 2.0
    start_cs = translate_coords_vertically(center_cs, delta)
    end_cs = translate_coords_vertically(center_cs, -delta)
    return line_segment(start_cs, end_cs, tikz_str)


def line_segment_from_angle_and_length(start_cs, angle, length, tikz_str=""):
    end_cs = coords_on_circle(start_cs, length, angle)
    return line_segment(start_cs, end_cs, tikz_str)


def line_segment_between_circles(from_center_cs,
                                 from_radius,
                                 from_angle,
                                 to_center_cs,
                                 to_radius,
                                 to_angle,
                                 tikz_str=""):
    from_cs = coords_on_circle(from_center_cs, from_radius, from_angle)
    to_cs = coords_on_circle(to_center_cs, to_radius, to_angle)
    return line_segment(from_cs, to_cs, tikz_str)


def centered_line_segment_from_angle_and_length(center_cs,
                                                angle,
                                                length,
                                                tikz_str=""):
    radius = length / 2.0
    start_cs = coords_on_circle(center_cs, radius, angle)
    end_cs = coords_on_circle(center_cs, radius, angle + 180.0)
    return line_segment(start_cs, end_cs, tikz_str)


def orthogonal_connector_with_horizontal_switch(from_cs,
                                                to_cs,
                                                alpha,
                                                tikz_str=""):
    from_x, from_y = from_cs
    to_x, to_y = to_cs
    switch_x = (1.0 - alpha) * from_x + alpha * to_x
    return open_path([from_cs, [switch_x, from_y], [switch_x, to_y], to_cs],
                     tikz_str)


def orthogonal_connector_with_vertical_switch(from_cs,
                                              to_cs,
                                              alpha,
                                              tikz_str=""):
    from_x, from_y = from_cs
    to_x, to_y = to_cs
    switch_y = (1.0 - alpha) * from_y + alpha * to_y
    return open_path([from_cs, [from_x, switch_y], [to_x, switch_y], to_cs],
                     tikz_str)


def orthogonal_connector_with_midway_horizontal_switch(from_cs,
                                                       to_cs,
                                                       tikz_str=""):
    return orthogonal_connector_with_horizontal_switch(from_cs, to_cs, 0.5,
                                                       tikz_str)


def orthogonal_connector_with_midway_vertical_switch(from_cs,
                                                     to_cs,
                                                     tikz_str=""):
    return orthogonal_connector_with_vertical_switch(from_cs, to_cs, 0.5,
                                                     tikz_str)


def rectangle(top_left_cs, bottom_right_cs, tikz_str=""):
    return closed_path([
        top_left_cs,
        top_right_coords(top_left_cs, bottom_right_cs), bottom_right_cs,
        bottom_left_coords(top_left_cs, bottom_right_cs)
    ], tikz_str)


def square(top_left_cs, side_length, tikz_str=""):
    x, y = top_left_cs
    return rectangle(top_left_cs, [x + side_length, y - side_length], tikz_str)


def open_path(cs_lst, tikz_str=""):
    return {"type": "open_path", "cs_lst": cs_lst, "tikz_str": tikz_str}


def closed_path(cs_lst, tikz_str=""):
    return {"type": "closed_path", "cs_lst": cs_lst, "tikz_str": tikz_str}


def circle(center_cs, radius, tikz_str=""):
    return {
        "type": "circle",
        "center_cs": center_cs,
        "radius": radius,
        "tikz_str": tikz_str
    }


def ellipse(center_cs, horizontal_radius, vertical_radius, tikz_str=""):
    return {
        "type": "ellipse",
        "center_cs": center_cs,
        "horizontal_radius": horizontal_radius,
        "vertical_radius": vertical_radius,
        "tikz_str": tikz_str
    }


def ellipse_from_width_over_height(center_cs,
                                   vertical_radius,
                                   ratio,
                                   tikz_str=""):
    horizontal_radius = vertical_radius * ratio
    return ellipse(center_cs, horizontal_radius, vertical_radius, tikz_str)


# the control points pull the curve towards them.
def bezier(from_cs, to_cs, c1_cs, c2_cs, tikz_str=""):
    return {
        "type": "bezier",
        "from_cs": from_cs,
        "to_cs": to_cs,
        "c1_cs": c1_cs,
        "c2_cs": c2_cs,
        "tikz_str": tikz_str
    }


def bezier_with_relative_angle_length_controls(from_cs,
                                               to_cs,
                                               c1_angle,
                                               c1_length,
                                               c2_angle,
                                               c2_length,
                                               tikz_str=""):

    ref_angle = vector_to_angle([from_cs, to_cs])
    c1_cs = coords_on_circle(from_cs, c1_length, ref_angle + c1_angle)
    c2_cs = coords_on_circle(to_cs, c2_length, ref_angle + c2_angle)
    return bezier(from_cs, to_cs, c1_cs, c2_cs, tikz_str)


def bezier_with_symmetric_relative_angle_length_controls(
        from_cs, to_cs, control_angle, control_length, tikz_str=""):

    ref_angle = vector_to_angle([from_cs, to_cs])
    c1_cs = coords_on_circle(from_cs, control_length, ref_angle + control_angle)
    c2_cs = coords_on_circle(to_cs, control_length,
                             ref_angle + 180.0 - control_angle)
    return bezier(from_cs, to_cs, c1_cs, c2_cs, tikz_str)


# TODO: do the analog of this, but with the angles not tied.
def bezier_with_symmetric_relative_angle_relative_length_controls(
        from_cs, to_cs, control_angle, control_length_multiplier, tikz_str=""):

    ref_angle = vector_to_angle([from_cs, to_cs])
    control_length = control_length_multiplier * length([from_cs, to_cs])
    c1_cs = coords_on_circle(from_cs, control_length, ref_angle + control_angle)
    c2_cs = coords_on_circle(to_cs, control_length,
                             ref_angle + 180.0 - control_angle)
    return bezier(from_cs, to_cs, c1_cs, c2_cs, tikz_str)


def bezier_with_symmetric_relative_angle_midway_controls(
        from_cs, to_cs, control_angle, tikz_str=""):
    angle = normalize_angle_to_standard_interval(control_angle)
    assert angle < 90.0 or angle > 270.0
    x = length([from_cs, to_cs]) / 2.0
    control_length = x / math.cos(degrees_to_radians(control_angle))
    ref_angle = vector_to_angle([from_cs, to_cs])
    control_cs = coords_on_circle(from_cs, control_length,
                                  ref_angle + control_angle)
    return bezier(from_cs, to_cs, control_cs, control_cs, tikz_str)


# NOTE: these are still not very nice.
def bezier_with_midwayx_controls(from_cs, to_cs, tikz_str=""):
    cs = midway_coords(from_cs, to_cs)
    delta_x = vector_to_deltax([cs, to_cs])
    c1_cs = translate_coords_horizontally(cs, delta_x)
    c2_cs = translate_coords_horizontally(cs, -delta_x)
    return bezier(from_cs, to_cs, c1_cs, c2_cs, tikz_str)


def bezier_with_midwayy_controls(from_cs, to_cs, tikz_str=""):
    cs = midway_coords(from_cs, to_cs)
    delta_y = vector_to_deltay([cs, to_cs])
    c1_cs = translate_coords_vertically(cs, delta_y)
    c2_cs = translate_coords_vertically(cs, -delta_y)
    return bezier(from_cs, to_cs, c1_cs, c2_cs, tikz_str)


def bezier_with_top_left_controls(from_cs, to_cs, tikz_str=""):
    cs = top_left_coords(from_cs, to_cs)
    return bezier(from_cs, to_cs, cs, cs, tikz_str)


def bezier_with_bottom_right_controls(from_cs, to_cs, tikz_str=""):
    cs = bottom_right_coords(from_cs, to_cs)
    return bezier(from_cs, to_cs, cs, cs, tikz_str)


def rectangle_from_width_over_height(top_left_cs, height, ratio, tikz_str=""):
    width = ratio * height
    bottom_right_cs = translate_coords(top_left_cs, width, -height)
    return rectangle(top_left_cs, bottom_right_cs, tikz_str)


def rectangle_from_width_and_height(top_left_cs, height, width, tikz_str=""):
    bottom_right_cs = translate_coords(top_left_cs, width, -height)
    return rectangle(top_left_cs, bottom_right_cs, tikz_str)


def rectangle_with_golden_ratio(top_left_cs, height, tikz_str=""):
    return rectangle_from_width_over_height(top_left_cs, height, golden_ratio,
                                            tikz_str)


def rectangle_from_additive_resizing(top_left_cs,
                                     bottom_right_cs,
                                     delta_x,
                                     delta_y,
                                     tikz_str=""):
    tcs = translate_coords(top_left_cs, -delta_x / 2.0, delta_y / 2.0)
    bcs = translate_coords(bottom_right_cs, delta_x / 2.0, -delta_y / 2.0)
    return rectangle(tcs, bcs, tikz_str)


def rectangle_from_multiplicative_resizing(top_left_cs,
                                           bottom_right_cs,
                                           alpha_x,
                                           alpha_y,
                                           tikz_str=""):
    ccs = midway_coords(top_left_cs, bottom_right_cs)
    tcs = [
        ccs[0] + alpha_x * (top_left_cs[0] - ccs[0]),
        ccs[1] + alpha_y * (top_left_cs[1] - ccs[1])
    ]
    bcs = [
        ccs[0] + alpha_x * (bottom_right_cs[0] - ccs[0]),
        ccs[1] + alpha_y * (bottom_right_cs[1] - ccs[1])
    ]
    return rectangle(tcs, bcs, tikz_str)


def circular_arc(center_cs, radius, start_angle, end_angle, tikz_str=""):
    return {
        "type": "circular_arc",
        "center_cs": center_cs,
        "radius": radius,
        "start_angle": start_angle,
        "end_angle": end_angle,
        "tikz_str": tikz_str
    }


def equilateral_triangle(center_cs, radius, starting_angle, tikz_str=""):
    cs_lst = equispaced_coords_on_circle(center_cs, radius, 3)
    cs_lst = [rotate_coords(cs, center_cs, starting_angle) for cs in cs_lst]
    return closed_path(cs_lst, tikz_str)


def polygon(center_cs, radius, num_sides, tikz_str=""):
    delta = 360.0 / num_sides

    return closed_path([
        coords_on_circle(center_cs, radius, delta * i) for i in range(num_sides)
    ], tikz_str)


def latex(cs, expr, tikz_str=""):
    return {"type": "latex", "cs": cs, "expr": expr, "tikz_str": tikz_str}


def image(filepath, top_left_cs, height, width, tikz_str=""):
    return {
        "type": "image",
        "filepath": filepath,
        "top_left_cs": top_left_cs,
        "height": height,
        "width": width,
        "tikz_str": tikz_str
    }


def horizontal_guidelines(top_left_cs, bottom_right_cs, spacing, tikz_str=""):
    width = x_length([top_left_cs, bottom_right_cs])
    height = y_length([top_left_cs, bottom_right_cs])
    n = int(math.ceil(height / float(spacing))) + 1
    return [
        horizontal_line_segment(
            translate_coords_vertically(top_left_cs, -i * spacing), width,
            tikz_str) for i in range(n)
    ]


def vertical_guidelines(top_left_cs, bottom_right_cs, spacing, tikz_str=""):
    width = x_length([top_left_cs, bottom_right_cs])
    height = y_length([top_left_cs, bottom_right_cs])
    n = int(math.ceil(width / float(spacing))) + 1
    return [
        vertical_line_segment(
            translate_coords_horizontally(top_left_cs, i * spacing), -height,
            tikz_str) for i in range(n)
    ]


def guidelines(top_left_cs, bottom_right_cs, spacing, tikz_str=""):
    return [
        horizontal_guidelines(top_left_cs, bottom_right_cs, spacing, tikz_str),
        vertical_guidelines(top_left_cs, bottom_right_cs, spacing, tikz_str)
    ]


def horizontal_ticks(start_cs, num_ticks, tick_spacing, tick_delta,
                     tikz_str=""):
    x, y = start_cs
    return [
        vertical_line_segment([x + i * tick_spacing, y], tick_delta, tikz_str)
        for i in range(num_ticks)
    ]


def vertical_ticks(start_cs, num_ticks, tick_spacing, tick_delta, tikz_str=""):
    x, y = start_cs
    return [
        vertical_line_segment([x, y + i * tick_spacing], tick_delta, tikz_str)
        for i in range(num_ticks)
    ]


def arrow(shaft_width, shaft_height, head_width, head_height, tikz_str=""):
    return closed_path([
        [0.0, shaft_height / 2.0],
        [shaft_width, shaft_height / 2.0],
        [shaft_width, head_height / 2.0],
        [shaft_width + head_width, 0.0],
        [shaft_width, -head_height / 2.0],
        [shaft_width, -shaft_height / 2.0],
        [0.0, -shaft_height / 2.0],
    ], tikz_str)


### helper functions for placing coords
def coords_on_circle(center_cs, radius, angle):
    cs = translate_coords_horizontally(center_cs, radius)
    return rotate_coords(cs, center_cs, angle)


def antipodal_coords(cs, radius, angle):
    return [
        coords_on_circle(cs, radius, angle),
        coords_on_circle(cs, radius, angle + 180.0)
    ]


def equispaced_coords_on_circle(center_cs, radius, n):
    delta = 360.0 / n
    return [coords_on_circle(center_cs, radius, i * delta) for i in range(n)]


def coords_on_ellipse(center_cs, horizontal_radius, vertical_radius, angle):
    raise NotImplementedError


def are_coords_inside_rectangle(cs, top_left_cs, bottom_right_cs):
    return (top_left_cs[0] <= cs[0] and cs[0] <= bottom_right_cs[0] and
            bottom_right_cs[1] <= cs[1] and cs[1] <= top_left_cs[1])


def coords_on_rectangle(top_left_cs, bottom_right_cs, angle):
    center_cs = midway_coords(top_left_cs, bottom_right_cs)
    end_cs = coords_on_circle(center_cs, 1.0, angle)
    top_right_cs = top_right_coords(top_left_cs, bottom_right_cs)
    delta_angle = vector_to_angle([center_cs, top_right_cs])

    # return coords depending on the side it falls in.
    if (angle >= 0 and angle <= delta_angle) or (angle >= 360.0 - delta_angle):
        cs = coords_on_line_with_x_value(center_cs, end_cs, bottom_right_cs[0])
    elif angle > delta_angle and angle <= 180.0 - delta_angle:
        cs = coords_on_line_with_y_value(center_cs, end_cs, top_left_cs[1])
    elif angle > 180.0 - delta_angle and angle <= 180 + delta_angle:
        cs = coords_on_line_with_x_value(center_cs, end_cs, top_left_cs[0])
    elif angle > 180.0 + delta_angle and angle <= 360.0 - delta_angle:
        cs = coords_on_line_with_y_value(center_cs, end_cs, bottom_right_cs[1])
    return cs


def coords_on_top_edge(top_left_cs, bottom_right_cs, alpha):
    top_right_cs = top_right_coords(top_left_cs, bottom_right_cs)
    cs = convex_combination_coords(top_left_cs, top_right_cs, alpha)
    return cs


def coords_on_bottom_edge(top_left_cs, bottom_right_cs, alpha):
    bottom_left_cs = bottom_left_coords(top_left_cs, bottom_right_cs)
    cs = convex_combination_coords(bottom_left_cs, bottom_right_cs, alpha)
    return cs


def coords_on_left_edge(top_left_cs, bottom_right_cs, alpha):
    bottom_left_cs = bottom_left_coords(top_left_cs, bottom_right_cs)
    cs = convex_combination_coords(bottom_left_cs, top_left_cs, alpha)
    return cs


def coords_on_right_edge(top_left_cs, bottom_right_cs, alpha):
    top_right_cs = top_right_coords(top_left_cs, bottom_right_cs)
    cs = convex_combination_coords(bottom_right_cs, top_right_cs, alpha)
    return cs


# t in [0, 1]. for symmetric curves, it should be 0.5 for the middle
def coords_on_bezier(from_cs, to_cs, c1_cs, c2_cs, t):
    raise NotImplementedError


def coords_on_line_segment(start_cs, end_cs, t):
    return [(1.0 - t) * start_cs[0] + t * end_cs[0],
            (1.0 - t) * start_cs[1] + t * end_cs[1]]


def coords_on_line_with_x_value(start_cs, end_cs, x):
    # y = mx + b
    # y1 = mx1 + b
    # y2 = mx2 + b
    # b = y - mx
    # y1 - y2 = m(x1 - x2)
    x1, y1 = start_cs
    x2, y2 = end_cs
    if abs(x1 - x2) < 1.0e-6:
        # vertical line.
        raise ValueError
    else:
        m = (y1 - y2) / float(x1 - x2)
        b = y1 - m * x1
        y = m * x + b
    return [x, y]


def coords_on_line_with_y_value(start_cs, end_cs, y):
    x1, y1 = start_cs
    x2, y2 = end_cs
    if abs(y1 - y2) < 1.0e-6:
        # horizontal line.
        raise ValueError
    else:
        m = (x1 - x2) / float(y1 - y2)
        b = x1 - m * y1
        x = m * y + b
    return [x, y]


def coords_from_deltas(start_cs, deltas_lst):
    cs_lst = [start_cs]
    cs = start_cs
    for (delta_x, delta_y) in deltas_lst:
        cs = translate_coords(cs, delta_x, delta_y)
        cs_lst.append(cs)
    return cs_lst


def coords_from_horizontal_deltas(start_cs, delta_lst):
    cs_lst = [start_cs]
    cs = start_cs
    for delta in delta_lst:
        cs = translate_coords_horizontally(cs, delta)
        cs_lst.append(cs)
    return cs_lst


def coords_from_vertical_deltas(start_cs, delta_lst):
    cs_lst = [start_cs]
    cs = start_cs
    for delta in delta_lst:
        cs = translate_coords_vertically(cs, delta)
        cs_lst.append(cs)
    return cs_lst


def coords_on_grid(top_left_cs, num_rows, num_columns, cell_width, cell_height):
    grid_cs = []
    for i in range(num_rows + 1):
        row_cs = []
        for j in range(num_columns + 1):
            cs = translate_coords(top_left_cs, j * cell_width, -i * cell_height)
            row_cs.append(cs)
        grid_cs.append(row_cs)
    return grid_cs


def coords_on_irregular_grid(top_left_cs, column_width_lst, row_height_lst):

    cs = top_left_cs
    grid_cs = [coords_from_horizontal_deltas(cs, column_width_lst)]
    for x in row_height_lst:
        cs = translate_coords_vertically(cs, -x)
        row_cs = coords_from_horizontal_deltas(cs, column_width_lst)
        grid_cs.append(row_cs)
    return grid_cs


# for canvas aligned axis; transform the data first with log if log coords necessary.
def axis_value_to_canvas_value(canvas_v, axis_v, other_canvas_v, other_axis_v,
                               queried_axis_v):
    m = (other_canvas_v - canvas_v) / float(other_axis_v - axis_v)
    b = canvas_v - m * axis_v
    return m * queried_axis_v + b


def canvas_value_to_axis_value(canvas_v, axis_v, other_canvas_v, other_axis_v,
                               queried_canvas_v):
    m = float(other_axis_v - axis_v) / (other_canvas_v - canvas_v)
    b = axis_v - m * canvas_v
    return m * queried_canvas_v + b


def draw_to_tikz(e):
    cmd_lst = []
    if isinstance(e, list):
        assert len(e) > 0
        for e_i in e:
            cmd_lst.extend(draw_to_tikz(e_i))

    elif e["type"] == 'open_path':
        cmd_lst.append(
            "\\draw[%s] " % e["tikz_str"] +
            " -- ".join(["(%f, %f)" % tuple(cs) for cs in e["cs_lst"]]) + ";")

    elif e["type"] == 'closed_path':
        # print e
        cmd_lst.append(
            "\\draw[%s] " % e["tikz_str"] +
            " -- ".join(["(%f, %f)" % (cs[0], cs[1]) for cs in e["cs_lst"]]) +
            " -- cycle;")

    elif e["type"] == "circle":
        cmd_lst.append(
            "\\draw[%s] (%f, %f) circle (%f);" %
            (e["tikz_str"], e["center_cs"][0], e["center_cs"][1], e["radius"]))

    elif e["type"] == 'ellipse':
        cmd_lst.append("\\draw[%s] (%f, %f) ellipse (%f and %f);" %
                       (e["tikz_str"], e["center_cs"][0], e["center_cs"][1],
                        e["horizontal_radius"], e["vertical_radius"]))

    elif e["type"] == "bezier":
        cmd_lst.append(
            "\\draw[%s] (%f, %f) .. controls (%f, %f) and (%f, %f) .. (%f, %f);"
            % tuple([e["tikz_str"]] + e["from_cs"] + e["c1_cs"] + e["c2_cs"] +
                    e["to_cs"]))

    elif e["type"] == "circular_arc":
        cmd_lst.append("\\draw[%s] (%f,%f) arc (%f:%f:%f);" %
                       (e["tikz_str"], e["center_cs"][0], e["center_cs"][1],
                        e["start_angle"], e["end_angle"], e["radius"]))

    elif e["type"] == "elliptical_arc":
        cmd_lst.append("\\draw[%s] (%f,%f) arc (%f:%f:%f and %f);" %
                       (e["tikz_str"], e["center_cs"][0], e["center_cs"][1],
                        e["start_angle"], e["end_angle"],
                        e["horizontal_radius"], e["vertical_radius"]))

    elif e["type"] == "latex":
        cmd_lst.append("\\node[%s] at (%f,%f) {%s};" %
                       (e["tikz_str"], e["cs"][0], e["cs"][1], e["expr"]))

    elif e["type"] == "image":
        center_cs = translate_coords(e["top_left_cs"], e["width"] / 2.0,
                                     -e["height"] / 2.0)
        cmd_lst.append(
            "\\node[inner sep=0pt, %s] at (%f,%f) {\\includegraphics[height=%f, width=%f]{%s}};"
            % (e["tikz_str"], center_cs[0], center_cs[1], e["height"],
               e["width"], e["filepath"]))
    else:
        raise ValueError("draw not implemented for element: %s" % e["type"])

    return cmd_lst


def write_textfile(filepath, lines):
    with open(filepath, 'w') as f:
        for line in lines:
            f.write(line + "\n")


# TODO: have to define colors by hand.
def draw_to_tikz_standalone(e, filepath, name2color_in_rgb=None):
    tikz_lines = []
    tikz_lines.extend([
        '\\documentclass{standalone}',
        "\\usepackage[T1]{fontenc}"
        '\\usepackage{tikz}',
        '\\usepackage{amsmath, amsfonts}',
        '\\usetikzlibrary{arrows.meta}',
        '\\begin{document}',
        '\\begin{tikzpicture}',
    ])

    # define the colors used.
    if name2color_in_rgb is not None:
        tikz_lines.extend([
            '\\definecolor{%s}{RGB}{%d,%d,%d}' % (name, rgb[0], rgb[1], rgb[2])
            for (name, rgb) in name2color_in_rgb.items()
        ])

    tikz_lines.extend(draw_to_tikz(e))
    tikz_lines.extend([
        '\\end{tikzpicture}',
        '\\end{document}',
    ])
    write_textfile(filepath, tikz_lines)


#### tikz reference

#===> linewidth

# \tikzset{
#     ultra thin/.style= {line width=0.1pt},
#     very thin/.style=  {line width=0.2pt},
#     thin/.style=       {line width=0.4pt},% (*** DEFAULT ***; close to 1/64cm)
#     semithick/.style=  {line width=0.6pt},
#     thick/.style=      {line width=0.8pt},
#     very thick/.style= {line width=1.2pt},
#     ultra thick/.style={line width=1.6pt}
# }

#===> linestyle

# \tikzstyle{solid}=                   [dash pattern=]
# \tikzstyle{dotted}=                  [dash pattern=on \pgflinewidth off 2pt]
# \tikzstyle{densely dotted}=          [dash pattern=on \pgflinewidth off 1pt]
# \tikzstyle{loosely dotted}=          [dash pattern=on \pgflinewidth off 4pt]
# \tikzstyle{dashed}=                  [dash pattern=on 3pt off 3pt]
# \tikzstyle{densely dashed}=          [dash pattern=on 3pt off 2pt]
# \tikzstyle{loosely dashed}=          [dash pattern=on 3pt off 6pt]
# \tikzstyle{dashdotted}=              [dash pattern=on 3pt off 2pt on \the\pgflinewidth off 2pt]
# \tikzstyle{densely dashdotted}=      [dash pattern=on 3pt off 1pt on \the\pgflinewidth off 1pt]
# \tikzstyle{loosely dashdotted}=      [dash pattern=on 3pt off 4pt on \the\pgflinewidth off 4pt]

#===> fontsize (TODO: add the size in pts)

# \tiny
# \scriptsize
# \footnotesize
# \small
# \normalsize
# \large
# \Large
# \LARGE
# \huge
# \Huge

#===> font type

# https://www.overleaf.com/learn/latex/Font_typefaces
# https://tug.org/FontCatalogue/
# https://fonts.google.com/
# http://mirror.las.iastate.edu/tex-archive/fonts/
# https://tex.stackexchange.com/questions/84533/font-installation-woes-texshop-on-a-mac?rq=1

#===> external links

# https://tex.stackexchange.com/questions/45275/tikz-get-values-for-predefined-dash-patterns
# https://tex.stackexchange.com/questions/255234/how-does-one-pick-control-points-to-control-b%C3%A9zier-curves-in-tikz
# https://tex.stackexchange.com/questions/20885/draw-curly-braces-in-tikz
# https://cremeronline.com/LaTeX/minimaltikz.pdf
# https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833 ; for tips on scientific figures.

#===> colors

# https://www.kennethmoreland.com/color-advice/

#### TODO

# - continuous compilation with file changes (useful for finding the right dimensions).
# - additional print options for generating tikz code.
# - easier handling of tikz styling options
# - easier handling of sizing options.
# - better defaults for colors.
# - better defaults for sizes. (powers (both positive and negative) of 2)
# - better default aspect ratios.
# - ability to draw auxiliary controls for bezier curves.
# - better interactivity (e.g., multiple drawings with binary search)
# - computation of the convex hull of a set of points.
# - computation of contour sets given a function.
# - basic scaling options
# - few basic default styles.
# - antipodal points for reference.
# - dealing with text appropriately (currently it is somewhat of a 2nd class citizen)
# - dealing with styling options appropriately  (these are not made super easy; require styling strings).
# --> maybe manage the creation of these strings.
# - support for simple plotting.
# - good default groups in the creation of figures
# - higher order functions to draw and then label specific places (?)
# - additional figures (triangle?)
# - animation functionality (should be fun)
# - FIX the drawing commands to make them simpler and less verbose
# - proper handling of images
# - bezier curve with symmetric controls and other nicer options.
# - write more functionality to work with angles.
# - fix the headers for the library.
# - think of a better name.
# - define a few styles. erase style.
# - draw complex closed paths involving different commands.
# - coloring text can be done, but I haven't thought much about it.
# - effective use of higher order functions for saving effort.
# - help with drawing highly symmetric figures, i.e., just draw a single plane.
# - functionality to tile a figure.
# - to address inconsistencies in how tikz handles nodes, always use a minipage.
# - make all the strings verbatin, i.e., the latex strings.
# - it would be convenient to have a function that distributes with a certain bounding box size that might be different than the one we want.
# - compute the spacing automatically from the sizes and the space that we want to occupy.
# - more relative positioning functionality as it is very useful (some spacing to the right of it)
# - translate_bottom_right_to_bottom_right(e, reference_e, delta_x, delta_y) and all the other combinations (there are sixteen of these functions, or even 64 such functions.)
# TODO: add guidelines that should be useful to get coordinates manually for this and to measure relative coordinates.
# TODO: add anchoring.
# - reduce the number of very common two steps.
# - add popular colors.
# - https://en.wikipedia.org/wiki/3D_projection ; add 3D projections.
# - draw patterns by copying a figure and putting it into multiple places or by calling a function.
# or by distributing a set of existing figures on a grid.
# - TODO: write the commit id that generated the figure in the file.
# - TODO: potentially move formatting to a single file.
# TODO: have a few more reference latex and tikz dimensions. (like linewidths)
# - TODO: rename to place_relative_to_top_and_align_center; place_relative_to_top
# - https://www.overleaf.com/learn/latex/Page_size_and_margins ; likely useful for slides.
# TODO: using other fonts. make it easy to add fonts in the package.
# https://tug.org/FontCatalogue/
# http://www.sascha-frank.com/latex-font-size.html
# https://tug.org/TUGboat/tb33-3/tb105thurnherr.pdf
# TODO: do GIFs.
# TODO: do pseudo interactivity (grid of multiple frames).
# TODO: add a way of dealing with node names.
# TODO: easy wall of using sane-tikz for presentations.
# work with maps and coloring maps (this might be interesting.)
# - basic functionality to read simple svg files.
# - package fonts with sane tikz
# overleaf.com/learn/latex/Questions/I_have_a_custom_font_I%27d_like_to_load_to_my_document._How_can_I_do_this%3F

# - ask for donations (*)

# define a grid for a plot.
# TODO: draw a bar plot with no lines.
# TODO: discrete ...
# TODO: think about the model.

# http://iamvdo.me/en/blog/css-font-metrics-line-height-and-vertical-align#lets-talk-about-font-size-first
# TODO: check about font size.

# TODO: add a tile option. this needs to deal with alignments:
# tons of different ones. how to angle the ones that have different sizes.

# Show a GIF of local first and second order approximations to various functions.

# Low pass filter; this would be nice.

# file:///Users/negrinho/Downloads/world.svg
# add world maps.

# https://simplemaps.com/

# https://distill.pub/

# TODO: make a discovery

# convex hull with some sequence of points.
# change this to use numpy at some point and to handle directly
# matrices (n points x dimension.)
# do these like matlab.

# https://tex.stackexchange.com/questions/25249/how-do-i-use-a-particular-font-for-a-small-section-of-text-in-my-document

# TODO: make it possible to compile to svg (not sure if it can have data.)
# this would be useful to embed it in a webpage. (alternatives.)

# TODO: learning html

# how to surround an equation with a text bounding box. see that I can do it consistently.
# can I compile animations to manim.
# can I set properties easily, e.g., color.