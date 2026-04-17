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

class DoubleSolenoidBox(Boxes):
    """Box with top and front open"""

    ui_group = "Box"

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.buildArgParser("outside", x=60, y=40, h=30)
        # self.argparser.add_argument(
        #     "--edgetype", action="store",
        #     type=ArgparseEdgeType("Fh"), choices=list("Fh"),
        #     default="F",
        #     help="edge type")
        self.addSettingsArgs(edges.FingerJointSettings)

        self.argparser.add_argument(
            "--solenoid_mounting_holes_length",
            action="store",
            type=float,
            default=14.5,
            help="Distance between mounting holes(along length of solenoid actuator)",
        )
        self.argparser.add_argument(
            "--solenoid_mounting_holes_width",
            action="store",
            type=float,
            default=12,
            help="Distance between mounting holes",
        )
        self.argparser.add_argument(
            "--solenoid_mounting_holes_diameter",
            action="store",
            type=float,
            default=3,
            help="Diameter of mounting holes",
        )

        self.argparser.add_argument(
            "--solenoid_mounting_holes_centre_from_edge",
            action="store",
            type=float,
            default=20,
            help="distance from centre of solenoid holes to edge of box",
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
            default=3,
            help="",
        )
        self.argparser.add_argument(
            "--axle_hole_distance_from_centre",
            action="store",
            type=float,
            default=24,
            help="centre of mounting holes to axle hole distance",
        )

        self.argparser.add_argument(
            "--back_hole_distance",
            action="store",
            type=float,
            default=12.5,
            help="",
        )

        self.argparser.add_argument(
            "--back_hole_diameter",
            action="store",
            type=float,
            default=10,
            help="",
        )
        
        self.argparser.add_argument(
            "--extra_height",
            action="store",
            type=float,
            default=25,
            help="",
        )
       
        self.argparser.add_argument(
            "--slit_length",
            action="store",
            type=float,
            default=12,
            help="",
        )
        self.argparser.add_argument(
            "--slit_width",
            action="store",
            type=float,
            default=5,
            help="",
        )

        self.argparser.set_defaults(x=60)
            
    def baseOuterHoles(self):
        #  self.hole(-self.thickness+self.x/2 + self.solenoid_mounting_holes_width/2, -self.thickness+self.space_at_front + self.solenoid_mounting_holes_height/2, d=self.solenoid_mounting_holes_diameter)
        #  self.hole(-self.thickness+self.x/2 + self.solenoid_mounting_holes_width/2, -self.thickness+self.space_at_front - self.solenoid_mounting_holes_height/2, d=self.solenoid_mounting_holes_diameter)
        #  self.hole(-self.thickness+self.x/2 - self.solenoid_mounting_holes_width/2, -self.thickness+self.space_at_front + self.solenoid_mounting_holes_height/2, d=self.solenoid_mounting_holes_diameter)
        #  self.hole(-self.thickness+self.x/2 - self.solenoid_mounting_holes_width/2, -self.thickness+self.space_at_front - self.solenoid_mounting_holes_height/2, d=self.solenoid_mounting_holes_diameter)
        # self.hole(self.extra_height,-self.thickness,d=self.solenoid_mounting_holes_diameter)
        # self.hole(self.h + self.extra_height - self.thickness, -self.thickness, d=self.solenoid_mounting_holes_diameter)

        # self.hole(self.extra_height + self.h/2 - self.thickness/2,-self.thickness + self.solenoid_mounting_holes_centre_from_edge, d=self.solenoid_mounting_holes_diameter)
        self.hole(self.extra_height + self.h/2 - self.thickness/2 - self.solenoid_mounting_holes_width/2,-self.thickness + self.solenoid_mounting_holes_centre_from_edge + self.solenoid_mounting_holes_length/2, d=self.solenoid_mounting_holes_diameter)
        self.hole(self.extra_height + self.h/2 - self.thickness/2 + self.solenoid_mounting_holes_width/2,-self.thickness + self.solenoid_mounting_holes_centre_from_edge + self.solenoid_mounting_holes_length/2, d=self.solenoid_mounting_holes_diameter)
        self.hole(self.extra_height + self.h/2 - self.thickness/2 - self.solenoid_mounting_holes_width/2,-self.thickness + self.solenoid_mounting_holes_centre_from_edge - self.solenoid_mounting_holes_length/2, d=self.solenoid_mounting_holes_diameter)
        self.hole(self.extra_height + self.h/2 - self.thickness/2 + self.solenoid_mounting_holes_width/2,-self.thickness + self.solenoid_mounting_holes_centre_from_edge - self.solenoid_mounting_holes_length/2, d=self.solenoid_mounting_holes_diameter)


    def hingeHoles(self):
        # self.hole(0, 0, d=3)
        self.hole(7, 6, d=3)
        self.hole(22, 8, d=3)
        self.hole(37, 6, d=3)

    def sideCallbacks(self):
        self.baseOuterHoles()
        self.fingerHolesAt(-self.thickness*.5+self.extra_height, -self.thickness*.5, self.y)
        self.hole(-self.thickness*.5 + self.extra_height*.5, -self.thickness + self.solenoid_mounting_holes_centre_from_edge - self.axle_hole_distance_from_centre, d=self.axle_hole_diameter)
        self.rectangularHole(-self.thickness*.5 + self.extra_height*.5, -self.thickness + self.solenoid_mounting_holes_centre_from_edge - self.axle_hole_distance_from_centre, r=self.axle_hole_diameter*2
                             , dx=self.extra_height+self.thickness, dy = self.extra_height+self.thickness)

        

    def backCallback(self):
        self.hole(self.back_hole_distance, self.h*.5 - self.thickness*.5, d=self.back_hole_diameter)
                # self.hole(-self.thickness*.5, 0, d=self.back_hole_diameter)

    def topCallback(self):
        self.rectangularHole(self.back_hole_distance, -self.thickness + self.slit_length*.5, self.slit_width, self.slit_length)
        self.rectangularHole(self.x - self.thickness*2 - self.back_hole_distance, -self.thickness + self.slit_length*.5, self.slit_width, self.slit_length)

    def bottomExtensions(self):
        self.hole(self.x*.5-self.thickness, -10, d=3)
        self.rectangularHole(self.x*.5-self.thickness, -8, r=self.axle_hole_diameter
                             , dx=25, dy = 16)

    
    def render(self):
        x, y, h = self.x, self.y, self.h
        t = self.thickness

        if self.outside:
            x = self.adjustSize(x)
            y = self.adjustSize(y, False)
            h = self.adjustSize(h, False)

        backEdge = edges.CompoundEdge(
            self,
            types=["f", "E"], 
            lengths=[h, self.extra_height]
        )
        self.edges['a'] = backEdge

        # compensateEdge = edges.CompoundEdge(
        #     self,
        #     types=["F", "e"], 
        #     lengths=[self.extra_height, h-self.extra_height]
        # )
        # self.edges['b'] = compensateEdge
        # compensateEdge2 = edges.CompoundEdge(
        #     self,
        #     types=["e", "F"], 
        #     lengths=[h-self.extra_height, self.extra_height]
        # )
        # self.edges['B'] = compensateEdge2

        # self.rectangularWall(x, h, "FFFF", move="right", label="Wall 1")
        self.rectangularWall(h+self.extra_height, y, "EfaE", move="right", label="Wall 2", callback = [self.sideCallbacks, None, None, None])
        self.rectangularWall(h+self.extra_height, y, "EfaE", move="right", label="Wall 2", callback = [self.sideCallbacks, None, None, None])

        # self.rectangularWall(h, y, "EFfF", move="right", label="Wall 4")
        self.rectangularWall(x, h, "fFfF", move="right", label="Wall s3", callback = [self.backCallback, None, self.backCallback, None])
        # self.rectangularWall(x, h, "fbfB", move="right", label="Wall 3", callback = [self.backCallback, None, self.backCallback, None])

        self.rectangularWall(x, y, "EfFf", move="right", label="Top", callback = [self.topCallback, None, None, None])
        self.rectangularWall(x, y, "EFhF", label="Bottom", move="right",callback = [self.bottomExtensions, None, self.bottomExtensions, None])

        # self.rectangularWall(x, y, "Ehhh", move="right", label="Bottom Plate" )
        # self.rectangularWall(x, y, "Ehhh", move="right", label="Bottom Plate" )
        
       

       
