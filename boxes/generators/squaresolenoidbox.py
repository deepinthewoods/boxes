#!/usr/bin/env python3
# Copyright (C) 2013-2014 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *

class SquareSolenoidBox(Boxes):
    """Box with top and front open"""

    ui_group = "Box"

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.buildArgParser("x", "y", "h", "outside")
        # self.argparser.add_argument(
        #     "--edgetype", action="store",
        #     type=ArgparseEdgeType("Fh"), choices=list("Fh"),
        #     default="F",
        #     help="edge type")
        self.addSettingsArgs(edges.FingerJointSettings)

        self.argparser.add_argument(
            "--solenoid_mounting_holes_width",
            action="store",
            type=float,
            default=22,
            help="Distance between mounting holes(x)",
        )
        self.argparser.add_argument(
            "--solenoid_mounting_holes_height",
            action="store",
            type=float,
            default=30,
            help="Distance between mounting holes(y)",
        )
        self.argparser.add_argument(
            "--solenoid_mounting_holes_diameter",
            action="store",
            type=float,
            default=3,
            help="Diameter of mounting holes",
        )
        self.argparser.add_argument(
            "--solenoid_actuator_distance",
            action="store",
            type=float,
            default=52,
            help="Distance from center of holes to solenoid actuator hole",
        )
        self.argparser.add_argument(
            "--solenoid_actuator_height",
            action="store",
            type=float,
            default=20.5,
            help="Distance from edge of solenoid to actuator hole",
        )
        self.argparser.add_argument(
            "--solenoid_actuator_hole_diameter",
            action="store",
            type=float,
            default=3,
            help="Diameter of actuator hole",
        )
        self.argparser.add_argument(
            "--lever_actuator_hole_length",
            action="store",
            type=float,
            default=15,
            help="length of actuator hole on lever",
        )
        self.argparser.add_argument(
            "--lever_width",
            action="store",
            type=float,
            default=10,
            help="Width of lever",
        )
        self.argparser.add_argument(
            "--lever_angle",
            action="store",
            type=float,
            default=25,
            help="angle of lever",
        )
        self.argparser.add_argument(
            "--lever_top_length",
            action="store",
            type=float,
            default=30,
            help="length of top part of lever",
        )
        self.argparser.add_argument(
            "--space_at_front",
            action="store",
            type=float,
            default=5.0,
            help="Extra space at the front",
        )
        self.argparser.add_argument(
            "--axle_hole_diameter",
            action="store",
            type=float,
            default=4,
            help="",
        )
        self.argparser.add_argument(
            "--axle_length",
            action="store",
            type=float,
            default=12,
            help="length from edge of solenoid to axle centre",
        )
        self.argparser.add_argument(
            "--extra_height",
            action="store",
            type=float,
            default=25,
            help="",
        )
       


    
            
    def baseOuterHoles(self):
         self.hole(-self.thickness+self.x/2 + self.solenoid_mounting_holes_width/2, -self.thickness+self.offset_y+self.space_at_front + self.solenoid_mounting_holes_height/2, d=self.solenoid_mounting_holes_diameter)
         self.hole(-self.thickness+self.x/2 + self.solenoid_mounting_holes_width/2, -self.thickness+self.offset_y+self.space_at_front - self.solenoid_mounting_holes_height/2, d=self.solenoid_mounting_holes_diameter)
         self.hole(-self.thickness+self.x/2 - self.solenoid_mounting_holes_width/2, -self.thickness+self.offset_y+self.space_at_front + self.solenoid_mounting_holes_height/2, d=self.solenoid_mounting_holes_diameter)
         self.hole(-self.thickness+self.x/2 - self.solenoid_mounting_holes_width/2, -self.thickness+self.offset_y+self.space_at_front - self.solenoid_mounting_holes_height/2, d=self.solenoid_mounting_holes_diameter)
        
    def baseLeverHole(self):
        lever_hole_length = self.lever_width*2
        self.rectangularHole(-self.thickness+self.x/2, -self.thickness + lever_hole_length * 0.5+self.space_at_front, self.thickness+2, lever_hole_length)

    def sideAxleHole(self):
        self.hole(self.extra_height - self.axle_length, -self.thickness + self.lever_width * 0.5+self.space_at_front, self.axle_hole_diameter * .5)

    def sideCallbacks(self):
        self.sideAxleHole()
        self.fingerHolesAt(-self.thickness*.5+self.extra_height, -self.thickness*.5, self.y)



    def baseInsideCallbacks(self):
        self.baseOuterHoles()
        self.baseLeverHole()

    def leverAxleHole(self):
        self.hole(self.lever_width  * .5, self.lever_width * .5, self.axle_hole_diameter * .5)
        self.hole(self.lever_width  * .5 , self.lever_width * .5 + 15, 1)
    
    def leverBottomHole(self):
        self.rectangularHole(self.lever_width  * .5, self.lever_width * .5 + self.lever_actuator_hole_length*.5 - 2, self.solenoid_actuator_hole_diameter, self.lever_actuator_hole_length)

    def render(self):
        x, y, h = self.x, self.y, self.h
        t = self.thickness

        if self.outside:
            x = self.adjustSize(x)
            y = self.adjustSize(y, False)
            h = self.adjustSize(h, False)

        self.offset_y = self.solenoid_actuator_distance

        self.rectangularWall(x, h, "FFFF", move="right", label="Wall 1")
        self.rectangularWall(h+self.extra_height, y, "EFfE", move="right", label="Wall 2", callback = [self.sideCallbacks, None, None, None])
        self.rectangularWall(h+self.extra_height, y, "EFfE", move="right", label="Wall 2", callback = [self.sideCallbacks, None, None, None])

        # self.rectangularWall(h, y, "EFfF", move="right", label="Wall 4")
        self.rectangularWall(x, h, "FFFF", move="right", label="Wall 3")

        self.rectangularWall(x, y, "Efff", move="right", label="Top", callback = [self.baseInsideCallbacks, None, None, None])
        self.rectangularWall(x, y, "Efff", label="Bottom", move="right",)
        
        adj = self.lever_top_length + self.lever_width
        extra_height = adj*math.tan(math.radians(self.lever_angle))

        self.polygonWall([self.solenoid_actuator_height + self.axle_length + self.lever_width*2, 90, self.lever_width, 90,  self.solenoid_actuator_height + self.axle_length + self.lever_width,
                            -90, self.lever_top_length, 90, self.lever_width + extra_height,  90+self.lever_angle, 10, 90, 3, -90, 3, -90, 3, None], "eeeeee", move="right", label="lever", 
                            callback = [self.leverAxleHole, self.leverBottomHole, None, None, None, None])
