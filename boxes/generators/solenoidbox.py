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
from boxes.lids import LidSettings

class SolenoidBox(Boxes):
    """A simple Box"""

    description = "This box is kept simple on purpose. If you need more features have a look at the UniversalBox."
    
    ui_group = "Box"

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.addSettingsArgs(LidSettings)
        self.buildArgParser("x", "y", "h", "outside", "bottom_edge")
        self.argparser.add_argument(
            "--holes_offset_x",
            action="store",
            type=float,
            default=6,
            help="offset(x)",
        )
        self.argparser.add_argument(
            "--holes_offset_y",
            action="store",
            type=float,
            default=6,
            help="offset(y)",
        )
        self.argparser.add_argument(
            "--holes_diameter",
            action="store",
            type=float,
            default=4,
            help="mounting hole diameter",
        )
        self.argparser.add_argument(
            "--holes_distance",
            action="store",
            type=float,
            default=14,
            help="distance between holes",
        )
        self.argparser.add_argument(
            "--holes_distance_offset",
            action="store",
            type=float,
            default=25,
            help="distance between pairs of holes",
        )
        self.argparser.add_argument(
            "--holes_angle_between",
            action="store",
            type=float,
            default=15,
            help="distance between pairs of holes",
        )
        self.argparser.add_argument(
            "--holes_space_distance",
            action="store",
            type=float,
            default=8,
            help="distance from start point to start holes",
        )
        self.argparser.add_argument(
            "--holes_count",
            action="store",
            type=int,
            default=6,
            help="number of hole sets",
        )
        self.argparser.add_argument(
            "--rear_solenoid_mounting_holes_width",
            action="store",
            type=float,
            default=12,
            help="Distance between mounting holes(x)",
        )
        self.argparser.add_argument(
            "--rear_solenoid_mounting_holes_height",
            action="store",
            type=float,
            default=15,
            help="Distance between mounting holes(y)",
        )
        self.argparser.add_argument(
            "--rear_solenoid_mounting_holes_diameter",
            action="store",
            type=float,
            default=3,
            help="Diameter of mounting holes",
        )
        self.argparser.add_argument(
            "--rear_solenoid_mounting_holes_center_offset",
            action="store",
            type=float,
            default=13.5+1,
            help="Distance from edge of rear_solenoid body to middle of holes",
        )
        self.argparser.add_argument(
            "--rear_solenoid_center_hole_offset",
            action="store",
            type=float,
            default=12.5,
            help="Distance from edge of rear_solenoid body to middle of actuator",
        )
        self.argparser.add_argument(
            "--rear_solenoid_center_hole_diameter",
            action="store",
            type=float,
            default=10,
            help="diameter of hole for rear_solenoid actuator",
        )
    
    def mountingHolesA(self):
        # self.mountingHolesAngled(30)
        index = 0
        # for a in range(0,91,self.holes_angle_between):
        for a in range(self.holes_count):
            self.mountingHolesAngled(self.holes_angle_between * a, index)
            index += 1

    def mountingHoles(self):
        # self.mountingHolesAngled(30)
        index = 0
        # for a in range(0,91,self.holes_angle_between):
        for a in range(self.holes_count):
            self.mountingHolesAngled(self.holes_angle_between * a, index)
            index += 1

    def mountingHolesAngled(self,angle, index):
         with self.saved_context():
            # self.moveTo(self.holes_offset_x, self.holes_offset_y,  angle)
            # self.moveTo(self.holes_space_distance, 0, 0)
            self.moveTo(self.holes_offset_x, self.holes_offset_y + self.holes_space_distance * index,  angle)

           # if (angle == 0):
            self.hole(0,0,d=self.holes_diameter)
            self.moveTo(self.holes_distance, 0, 0)
            self.hole(0,0,d=self.holes_diameter)
            self.moveTo(self.holes_distance_offset - self.holes_distance, 0, 0)
            self.hole(0,0,d=self.holes_diameter)
            self.moveTo(self.holes_distance, 0, 0)
            self.hole(0,0,d=self.holes_diameter)

    def rear_solenoidMountingHoles(self):
        self.moveTo(self.x/2, self.rear_solenoid_mounting_holes_center_offset)
        self.hole(self.rear_solenoid_mounting_holes_width/2, self.rear_solenoid_mounting_holes_height/2, d=self.rear_solenoid_mounting_holes_diameter)
        self.hole(-self.rear_solenoid_mounting_holes_width/2, self.rear_solenoid_mounting_holes_height/2, d=self.rear_solenoid_mounting_holes_diameter)
        self.hole(self.rear_solenoid_mounting_holes_width/2, -self.rear_solenoid_mounting_holes_height/2, d=self.rear_solenoid_mounting_holes_diameter)
        self.hole(-self.rear_solenoid_mounting_holes_width/2, -self.rear_solenoid_mounting_holes_height/2, d=self.rear_solenoid_mounting_holes_diameter)

    def rear_solenoidActuatorHole(self):
        self.moveTo(self.x/2, self.rear_solenoid_center_hole_offset)
        self.hole(0, 0, d=self.rear_solenoid_center_hole_diameter)

    def render(self):
        x, y, h = self.x, self.y, self.h
        t = self.thickness

        t1, t2, t3, t4 = "eeee"
        b = self.edges.get(self.bottom_edge, self.edges["F"])
        sideedge = "F" # if self.vertical_edges == "finger joints" else "h"

        if self.outside:
            self.x = x = self.adjustSize(x, sideedge, sideedge)
            self.y = y = self.adjustSize(y)
            self.h = h = self.adjustSize(h, b, t1)

        with self.saved_context():
            self.rectangularWall(x, h, [b, sideedge, t1, sideedge],
                                 ignore_widths=[1, 6], move="up")
            self.rectangularWall(x, h, [b, sideedge, t3, sideedge],
                                 ignore_widths=[1, 6], move="up", callback = [self.rear_solenoidActuatorHole, None, None, None])

            if self.bottom_edge != "e":
                self.rectangularWall(x, y, "ffff", move="up", callback = [self.rear_solenoidMountingHoles, None, None, None])
            self.lid(x, y)

        self.rectangularWall(x, h, [b, sideedge, t3, sideedge],
                             ignore_widths=[1, 6], move="right only")
        self.rectangularWall(y, h, [b, "f", t2, "f"],
                             ignore_widths=[1, 6], move="up", callback = [self.mountingHoles, None, None, None])
        self.rectangularWall(y, h, [b, "f", t4, "f"],
                             ignore_widths=[1, 6], move="up", callback = [self.mountingHoles, None, None, None])

