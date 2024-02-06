#! /usr/bin/env python3
import sys
import numpy as np
from solid import *
from solid.objects import cube, translate, union, rotate, color, cylinder

SEGMENTS = 48


def eyeGenerator():

    cubeShape = cube([2, 1, 1], center=True)
    cornerCylinder = cylinder(h=1, r=1, center=True)
    eyeCup = minkowski()(cubeShape, cornerCylinder)
    eyeCup = scale([1, 1, .1])(eyeCup)
    cubeShape = translate([2, -2, 0])(rotate([0, 0, 45])(cube(3, center=True)))
    eyeCup = difference()(eyeCup, cubeShape)

    

    scaledEyeCup = translate([0, 0, .1])(scale([.9, .9, 1.])(eyeCup))
    outerCorneaCylinder = translate([-.2, 0, 0])(cylinder(h=5, r=1., center=True))
    scaledEyeCup = difference()(scaledEyeCup, outerCorneaCylinder)
    eyeCup = difference()(eyeCup, scaledEyeCup)

    corneaCylinder = translate([-.2, 0, 0])(cylinder(h=5, r=.5, center=True))
    eyeCup = difference()(eyeCup, corneaCylinder)

    return union()(eyeCup)


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
