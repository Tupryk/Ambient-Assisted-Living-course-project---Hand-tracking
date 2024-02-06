#! /usr/bin/env python3
import sys
import numpy as np
from solid import *
from solid.objects import cube, translate, union, rotate, color, cylinder

SEGMENTS = 48
TEETH = 16
GEAR_RADIOUS = 3.


def rotated_vec(vec, angle):
    new_vec = np.copy(vec)
    new_vec[0] = vec[0] * np.cos(angle) - vec[1] * np.sin(angle)
    new_vec[1] = vec[0] * np.sin(angle) + vec[1] * np.cos(angle)
    return new_vec

def truncated_pyramid(top_size, bottom_size, height):
    trapezoid_points = [
        [bottom_size / 2, -height / 2],
        [-bottom_size / 2, -height / 2],
        [-top_size / 2, height / 2],
        [top_size / 2, height / 2]
    ]
    trapezoid_shape = linear_extrude(height)(polygon(trapezoid_points))
    return trapezoid_shape

def eyeGenerator():

    gear = cylinder(r=GEAR_RADIOUS, h=1)
    hole = translate([0, 0, -.1])(cylinder(r=.7, h=2))
    gear = difference()(gear, hole)

    pyrams = []
    step = 2*np.pi/TEETH
    vec = np.array([0., 1.])
    for i in range(TEETH):
        angle = step*i
        new_vec = rotated_vec(vec, angle) * GEAR_RADIOUS

        pyramid = truncated_pyramid(top_size=0.2, bottom_size=1.5, height=1.5)
        pyramid = translate([new_vec[0], new_vec[1], -.1])(rotate([0, 0, np.rad2deg(angle)+180])(pyramid))

        pyrams.append(pyramid)

        gear = difference()(gear, pyramid)

    return union()(gear)


if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else None

    a = eyeGenerator()

    # Adding the file_header argument as shown allows you to change
    # the detail of arcs by changing the SEGMENTS variable.  This can
    # be expensive when making lots of small curves, but is otherwise
    # useful.
    file_out = scad_render_to_file(
        a, out_dir=out_dir, file_header=f'$fn = {SEGMENTS};')
    print(f"{__file__}: SCAD file written to: \n{file_out}")
