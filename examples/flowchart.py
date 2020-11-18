import sane_tikz.core as stz
import sane_tikz.formatting as fmt

box_height = 1.0
box_width = 1.6
box_spacing = 1.1
box_roundness = 0.1
shaft_width = 0.5
shaft_height = 0.4
head_width = 0.35
head_height = 0.8

lst = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
]


def box_with_text(s):
    s_fmt = fmt.rounded_corners(box_roundness)
    return [
        stz.rectangle([0, 0], [box_width, -box_height], s_fmt),
        stz.latex([box_width / 2.0, -box_height / 2.0], s)
    ]


def arrow():
    s_fmt = fmt.fill_color_with_no_line("lightgray")
    a = stz.arrow(shaft_width, shaft_height, head_width, head_height, -90.0,
                  s_fmt)
    return a


boxes = [box_with_text(s) for s in lst]
stz.distribute_vertically_with_spacing(boxes[::-1], box_spacing)

arrows = [arrow() for _ in range(len(lst) - 1)]
for i in range(len(boxes) - 1):
    to_cs = stz.center_coords(boxes[i:i + 2])
    from_cs = stz.center_coords(arrows[i])
    stz.translate_to_coords(arrows[i], from_cs, to_cs)

stz.draw_to_tikz_standalone([boxes, arrows], "flowchart.tex")
