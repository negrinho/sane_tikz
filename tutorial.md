

# Overview

`sane_tikz` follows a draw-and-place philosophy.
You draw on the canvas and then use functionality to place the visual elements.
There is no distinction between auxiliary code that you write and the code of `sane_tikz` so always consider creating functions to help you accomplish things when creating your figures.

Every program starts with
```
import sane_tikz as stz
import formatting as fmt
```
which imports the drawing, grouping, alignment, distribution, coordinate computation functionalities of the library.
`formatting` contains functionality to generate the TikZ formatting strings that are used for different purposes (e.g., making lines dashed or dotted, or changing the opacity of a fill).
Eventually, every example ends with a call to `stz.draw_to_tikz_standalone` which generates the code for a TikZ figure to a file.
This draw function unpacks a visual element into its components and draws them individually.

Perhaps the most useful concept in `sane_tikz` is grouping.
If  you have visual elements `e1` and `e2`, you can group them to create a new visual element `e_grouped = [e1, e2]`, i.e., by wrapping the visual elements in a list.
The new element `e_grouped` will be manipulated as a visual element in its own right, meaning that its bounding box is updated accordingly, and therefore all functions that rely on bounding box computations have their behavior updated.
The order that elements are grouped matters when drawing them to the canvas.
A visual element is decomposed into its sub-elements (if any) by going top to bottom and left to right.
Every element can be eventually decomposed down to basic visual elements such as math equations, line segments, circles, rectangles, and so on.
This recursive decomposition can be inspected in the `stz.draw_to_tikz` function which is used by the `stz.draw_to_tikz_standalone`.
This means that we can impose a drawing ordering simply by ordering the elements correctly in the grouping.
In the call to `stz.draw_to_tikz_standalone`, all the elements of the figure are grouped.
Oftentimes for figures, there is no particular ordering that must be imposed because the elements might not have overlaps between visual elements in the figure.

Other important concepts are moving existing elements and computing coordinates of interest such as bounding box computations.

# Simple example

The following example is drawn by the code below, which will be broken down into pieces for explaining its purpose.
This code corresponds to [this](https://github.com/negrinho/sane_tikz/blob/master/examples/pentagon.pdf) figure.

Importing the library and defining some basic values for specifying the figure.
In the examples, we often use this format which allows us to change some high-level characteristics of the figure and regenerate the output.
This is great compared to what you would need to do in a WYSIWYG editor to change high-level aspects of the figure (e.g., spacing or line width).

```
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
```

This defines the coordinates of the vertices of the pentagon and finally generates the representation for the pentagon through the call to `stz.closed_path`.
```
cs = [
   stz.coords_on_circle([0, 0], pentagon_radius, 90.0 + i * (360.0 / 5))
   for i in range(5)
]
e = stz.closed_path(cs)
```

This is the computation of the coordinates for placing various labels in the figure.
Note that the computation of these coordinates is done with respect to the vertices of the pentagon by translating them in appropriate directions.
```
origin_cs = stz.translate_coords_horizontally(cs[2], -1.0)
x_end_cs = stz.translate_coords_horizontally(origin_cs, x_axis_length)
y_end_cs = stz.translate_coords_vertically(origin_cs, y_axis_length)
x_start_cs = stz.translate_coords_horizontally(origin_cs, -extra_length)
y_start_cs = stz.translate_coords_vertically(origin_cs, -extra_length)
x_label_cs = stz.translate_coords_vertically(x_end_cs, -label_spacing)
y_label_cs = stz.translate_coords_horizontally(y_end_cs, -label_spacing)
origin_label_cs = stz.translate_coords_diagonally(origin_cs, -label_spacing)
```

Create the representation of the axes.
Note that they are grouped together.
A formatting string is used to create a line segment with an arrowhead.
See `formatting` for other possible options.
```
axes = [
   stz.line_segment(x_start_cs, x_end_cs, s_fmt),
   stz.line_segment(y_start_cs, y_end_cs, s_fmt)
]
```

Creates the representations of the labels in the figure along with a filled circle on point A.
```
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
```

Finally, all the elements in the figure are grouped into a single one (i.e., `[e, axes, labels]`, which represents the pentagon, the axes, and the labels, respectively).
The compilation of this figure into TikZ code is done by `stz.draw_to_tikz_standalone`.
The resulting tex file can then be compiled by a Latex compiler (e.g., pdflatex) to generate the visual output (see [here](https://github.com/negrinho/sane_tikz/blob/master/examples/pentagon.tex) for the result for this figure).
All figures are drawn in a lazy fashion, where first define the representation of the figure in terms of basic visual elements and finally compile them to TikZ code.
This allows us to define visual elements and move them around before generating the final visual representation.
Grouping is a very powerful feature.
For example, in the call below, we could have omitted all labels by simply passing `[e, axes]` instead of `[e, axes, labels]`.
We are also free to keep adding elements and generating new figures with them, even after the call to `stz.draw_to_tikz_standalone`.
This makes it easy to generate many related figures.
```
stz.draw_to_tikz_standalone([e, labels, axes], "pentagon.tex")
```

# Design overview

## Naming

We often prefix or suffix variable names with `cs` when they refer to coordinates, which are simply a list with a pair of numbers, which is a coordinate of a point in the canvas.
Functions that return coordinates often contain the substring `coords` in its name, e.g., `stz.translate_coords_horizontally` and `stz.coords_on_circle`.
These functions are often useful for computing coordinates of interest, such as coordinates on a circle, on a line segment, or on a rectangle.
For example, if you wanted the coordinates that are 45 degrees outside the origin at a distance of 5cm, you would call `stz.coords_on_circle([0, 0], 5.0, 45.0)`, which would output the desired values.
These functions mimic some of the hand drawing procedures that you do with a ruler, compass, and protractor.

For graphical elements, we often use the variable `e` (or `e_lst`) to denote them.
These are elements that can eventually be converted to a TikZ representation.
Contrary to coordinates, there isn't a single substring that appears in a function name when it produces elements to be drawn.
Examples of this are `stz.circle` and `stz.line_segment`.
These do not draw directly an element, simply they return a representation of the element to be drawn (i.e., a representation from which the TikZ string representing the object can be drawn).
The representation of an element to draw is, if we are talking about the most basic elements, a dictionary from strings to values that contains enough information to generate the TikZ representation for that element, and if more complex, a list of nested lists containing many visual elements (i.e., these are created through grouping).


## Grouping

Grouping is one of the most important functionalities of the language, and in my opinion, one of the most powerful when combined with the placement and alignment functionalities that use bounding box computations.
Grouping corresponds to lumping various elements into a new element.
This is done easily by wrapping the elements into a list and passing this list around.
This new element will function as an element in its own right with respect to bounding box computations.

## Translation and alignment

Given various elements, often regular such as multiple circles of the same size, there is often the need of aligning them (horizontally or vertically) or distributing them (horizontally or vertically).
These needs are met by functions that take graphical elements (grouped or not) and translate them around to implement the desired transformation.
Note that these functions have side-effects, meaning that the state of the visual elements passed to the functions will change to implement the desired transformations.
Translation and alignment functions operate on visual elements (grouped or not) and usually have movement-related terms in their function name (e.g., `translate`, `place`, `align`, and `distribute`).
The fact that they take elements can often be determined by the names of arguments of the functions, e.g., `e` or `e_lst`.
Some functions take reference elements that are used to compute quantities that are then used to specify a placement, e.g., `place_above_and_align_to_the_center` takes `e`, `e_ref`, and `spacing`; `e` is the element to be placed above `e_ref` such that the bounding boxes of `e` and `e_ref` are at a distance `spacing` from each other and their centers are aligned; only `e` is moved with respect to `e_ref`.
A variety of functions of this type exist such as `place_below_and_align_to_the_center`, `distribute_vertically_with_spacing`, any many more.
I recommend reading the source for these functions which often short and rely on high level functionality of the language (see immediately below for one example).

```
def distribute_vertically_with_spacing(e_lst, spacing):
   for i in range(1, len(e_lst)):
       e = e_lst[i]
       e_prev = e_lst[i - 1]
       cs = bbox(e)[1]
       cs_prev = bbox(e_prev)[0]
       delta_y = cs_prev[1] - cs[1] + spacing
       translate(e, 0, delta_y)
```

There exist also functions of this type that work over coordinates rather than elements (i.e., they take coordinates).
These functions usually have `cs` in the name of the arguments and `coords` in the name of the function (e.g., `translate_coords_horizontally`).

## Bounding boxes

Bounding boxes are convenient summaries when working with figures.
They are used widely in translation and alignment functionality.
The figures are summarized into a pair of coordinates of the top left corner and the bottom right corner of the bounding box.
The computation of the bounding box for an element is done by ungrouping recursively an element until it is expressed into basic elements for which we can compute the bounding box and then put back together through logic on how to combine multiple bounding boxes into a single bounding box (see `stz.bbox`).
This function is widely used, both in functionality within sane_tikz (e.g., `place_to_the_right`, `distribute_vertically_with_spacing`, and many others) and in drawing specific figures.
Bounding box computation may fail in cases where the grouped element contains basic elements which don’t yet have functionality to compute a bounding box.

## Coordinates


Coordinates are the starting point for much of what is done in this library.
Coordinates are used in specifying different graphical elements, for example rectangles (i.e., `stz.rectangle` which is specified through the coordinates of the top left corner and the bottom corner and an optional formatting string (e.g., for changing the colors of the line or the fill). Some examples of functions in this category are:
`coords_on_circle`, antipodal_`coords`, `coords_on_ellipse`, `coords_on_rectangle`, `coords_on_line_segment`, `coords_on_line_segment`, `coords_on_line_with_x_value`, `coords_on_line_with_y_value`, `coords_from_deltas`, and `coords_on_grid`.
Coordinate computation is also important for moving elements to specific places.

Sometime coordinates are computed with respect to other elements or coordinates, e.g., `center_coords` and `coords_from_bbox_fn` compute the coordinates of the center of the bounding box of an element and compute coordinates that are derived using some function of the coordinates of the bounding box.

## Latex support

Latex support is done through `stz.latex` which takes both a string (in math mode or otherwise) and the coordinates of where that string is to be placed.
Formatting options using `anchor` and `alignment` are often useful for specifying the placement of the string relative to the coordinates specified.
This allows to write latex code in a fairly transparent way, e.g., any string that would be possible to write in math mode (between $ or $$) is valid and so are environments (although additional trial and error may be necessary here in case errors are thrown).
The conversion of the latex string to the tikz code is fairly transparent as it is done through a node placed at the coordinates specified.

## Formatting

Most formatting is delegated to the `formatting` library.
The functionality of this library was designed to help generate the corresponding formatting strings given a set of options.
These can be options for fill, line width, line style, opacity, defining new colors, using color maps, and so on.
Multiple formatting strings can be combined into a single one using `fmt.combine_tikz_strs`.
This string is then passed as an argument in specific functions of the library to define the appropriate options (e.g., in `stz.rectangle`).
There is little enforcement of the correctness of the string; the functions there serve mostly as a way of making clear what are the most common options available and providing some guidance in assigning values to them.
`formatting` is not comprehensive; any valid formatting string that you would use in TikZ is valid and can be plugged in, rather than going through functions in `formatting`.
See the figures in the example folder for more information about their usage.

# A more complex example

Here is an explanation for [tree.py](https://github.com/negrinho/sane_tikz/blob/master/examples/tree.py) which produces [tree.pdf](https://github.com/negrinho/sane_tikz/blob/master/examples/tree.pdf).
This example shows the use of many of the functionalities discussed in this tutorial such as grouping, placement, and coordinate computation.

```
# reproduction of https://en.wikipedia.org/wiki/Binary_search_algorithm#/media/File:Binary_search_tree_search_4.svg

import sane_tikz as stz
import formatting as fmt
```

Basic formatting options for the figure.
Changes to the figure can be accomplished by changing the values for these parameters and regenerating the TikZ code.
```
node_radius = 0.30
vertical_node_spacing = 1.4 * node_radius
first_level_horizontal_node_spacing = 1.8
arrow_angle = 30.0
bbox_spacing = 0.1
label_spacing = 0.4
line_width = 1.2 * fmt.standard_line_width

s_lw = fmt.line_width(line_width)
```

Auxiliary function to draw a circle with Latex annotation at (0, 0).
```
fn = lambda expr: [
   stz.circle([0, 0], node_radius, s_lw),
   stz.latex([0, 0], expr)
]
```

Auxiliary function to place the node horizontally in its place.
```
def place(e, lst):
   delta = 0.0
   for i, sign in enumerate(lst):
       delta += sign * (node_radius + first_level_horizontal_node_spacing /
                           (2 * (i + 1.0)))
   stz.translate_horizontally(e, delta)
```

Auxiliary function to connect two nodes (with optional color for line). `line_segment_between_circles` returns a line segment that you can draw.
```
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
```

Auxiliary function to compute the bounding box of `e_lst` and expand it additivively to draw the dashed bounding box.
```
def dashed_bbox(e_lst):
   s_fmt = fmt.combine_tikz_strs([fmt.line_style("dashed"), s_lw])
   top_left_cs, bottom_right_cs = stz.bbox(e_lst)
   return stz.rectangle_from_additive_resizing(top_left_cs, bottom_right_cs,
                                               2.0 * bbox_spacing,
                                               2.0 * bbox_spacing, s_fmt)
```

Auxiliary function to label a node to the left and the right at some spacing from it.
```
def label_right(e, expr):
   cs = stz.coords_from_bbox_with_fn(e, stz.right_center_coords)
   cs = stz.translate_coords(cs, label_spacing, 0.1)
   return stz.latex(cs, "\\scriptsize{%s}" % expr)

def label_left(e, expr):
   cs = stz.coords_from_bbox_with_fn(e, stz.left_center_coords)
   cs = stz.translate_coords(cs, -label_spacing, 0.1)
   return stz.latex(cs, "\\scriptsize{%s}" % expr)
```

Creates all the nodes.
They aren't yet in the right positions.
```
nodes = []
for i in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
   if i == 4:
       s = "\\textbf{%s}" % str(i)
   else:
       s = str(i)
   nodes.append(fn(s))
```

Distributes them vertically.
Note that the nodes are grouped by level.
```
stz.distribute_vertically_with_spacing(
   [nodes[0:1], nodes[1:3], nodes[3:6], nodes[6:9]][::-1], vertical_node_spacing)
```

Fixes the horizontal spacing between the nodes of the tree at each level.
```
place(nodes[1], [-1])
place(nodes[2], [1])
place(nodes[3], [-1, -1])
place(nodes[4], [-1, 1])
place(nodes[5], [1, 1])
place(nodes[6], [-1, 1, -1])
place(nodes[7], [-1, 1, 1])
place(nodes[8], [1, 1, -1])
```

Draws all the connections.
```
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
```

Highlight the node that you care about by changing the TikZ formatting string for it.
(Kind of low-level, but can be done).
```
nodes[-3][0]["tikz_str"] = fmt.combine_tikz_strs(
   [nodes[-3][0]["tikz_str"],
       fmt.line_and_fill_colors("mygreen", "mygreen")])
nodes[-3][1]["tikz_str"] = fmt.combine_tikz_strs(
   [nodes[-3][0]["tikz_str"], "text=white"])
```

Draw the dashed boxes, which will be in the right places.
```
bb1 = dashed_bbox([nodes[6]])
bb2 = dashed_bbox([bb1, nodes[4], nodes[7]])
bb3 = dashed_bbox([bb2, nodes[1], nodes[3]])
bboxes = [bb1, bb2, bb3]
```

Draw the labels.
```
labels = [
   label_left(nodes[0], "4 < 8"),
   label_left(nodes[1], "4 > 3"),
   label_left(nodes[4], "4 < 6"),
]
```

Define the colors that you going to use in the figure in RGB.
These are then passed in `draw_to_tikz_standalone` to specify the user-defined colors used in the figure.
```
name2color = {"mygreen": (2, 129, 0)}
```

Grouping all the graphical elements of the figure.
This is really powerful in general, e.g., you can compute the coordinates of the group by simply doing `stz.bbox([nodes, connections, bboxes, labels])`.
```
e = [nodes, connections, bboxes, labels]
```

Finally, compile to TikZ, i.e., generate the TikZ code.
If any user-defined colors are needed for the figure, they need to be defined through a string to rgb tuple dictionary passed to the function (i.e., `name2color`).
```
stz.draw_to_tikz_standalone(e, "tree.tex", name2color)
```

Two recurring patterns we have observed above is the creation of auxiliary functions that take arguments corresponding to some parametrization of a visual element and then return the visual element in the right place (e.g., `dashed_bbox` and `connect`) and functions that take existing visual elements and place them in the right place (often as a function of some parametrization, e.g., `place`.
These functions could be very well present in the main library `sane_tikz`.
The main deciding factor in developing a function in a user file or in a library file is its expected widespread use.
If we expect a function to be useful in a wide variety of figures, then we include it in the main library.
Otherwise, it is kept in the local file corresponding to the figure.

Additional examples are available in the [examples](https://github.com/negrinho/sane_tikz/tree/master/examples) folder.
Inspecting some of the intermediate state of the figures should also give insight about what each function accomplishes, both in terms of creating new visual elements and of moving existing elements to the right place.
