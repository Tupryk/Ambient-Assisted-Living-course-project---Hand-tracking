// Generated by SolidPython 1.1.3 on 2024-01-15 09:28:27
$fn = 48;


union() {
	difference() {
		difference() {
			scale(v = [1.7000000000, 1.1000000000, 1.2000000000]) {
				cube(center = true, size = [0.9000000000, 1.0000000000, 0.4000000000]);
			}
			translate(v = [0, 0.5500000000, 0.0500000000]) {
				scale(v = [1, 2, 1]) {
					cube(center = true, size = [0.9000000000, 1.0000000000, 0.4000000000]);
				}
			}
		}
		translate(v = [-0.2000000000, 0.0000000000, 0.0500000000]) {
			scale(v = [0.5000000000, 2, 1]) {
				cube(center = true, size = [0.9000000000, 1.0000000000, 0.4000000000]);
			}
		}
	}
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
#! /usr/bin/env python3
import sys
import numpy as np
from solid import *
from solid.objects import cube, translate, union, rotate, color, cylinder

SEGMENTS = 48
SERVO_WIDTH = .9
SERVO_HEIGHT = .4
SERVO_DEPTH = 1.


def eyeGenerator():

    holder = cube([SERVO_WIDTH+1, SERVO_DEPTH, SERVO_HEIGHT], center=True)
    servo = cube([SERVO_WIDTH, SERVO_DEPTH, SERVO_HEIGHT], center=True)
    servoHolder = scale([1.7, 1.1, 1.2])(servo)
    servoDiff = translate([0, .55, .05])(scale([1, 2, 1])(servo))
    neckPiece = difference()(servoHolder, servoDiff)
    servoTopDiff = translate([-.2, .0, .05])(scale([.5, 2, 1])(servo))
    neckPiece = difference()(neckPiece, servoTopDiff)

    return union()(neckPiece)


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
 
 
************************************************/
