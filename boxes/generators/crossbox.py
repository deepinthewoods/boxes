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


class CrossBox(Boxes):
    """A cross shaped Box"""

    description = "This box is kept simple on purpose. If you need more features have a look at the UniversalBox."

    ui_group = "Box"

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.addSettingsArgs(LidSettings)
        self.buildArgParser("x", "y", "h", "outside", "bottom_edge")

        self.argparser.add_argument(
            "--width_x",
            action="store",
            type=float,
            default=40,
            help="width of x section",
        ) 

        self.argparser.add_argument(
            "--width_y",
            action="store",
            type=float,
            default=40,
            help="width of y section",
        ) 
    def hingeHoles(self):
        # self.hole(0, 0, d=3)
        self.hole(7, 6, d=3)
        self.hole(22, 8, d=3)
        self.hole(37, 6, d=3)

    def render(self):
        x, y, h, wx, wy = self.x, self.y, self.h, self.width_x, self.width_y
        t = self.thickness

        t1, t2, t3, t4 = "eeee"
        b = self.edges.get(self.bottom_edge, self.edges["F"])
        sideedge = "F" # if self.vertical_edges == "finger joints" else "h"

        if self.outside:
            self.x = x = self.adjustSize(x, sideedge, sideedge)
            self.y = y = self.adjustSize(y)
            self.h = h = self.adjustSize(h, b, t1)
            self.width_x = wx = self.adjustSize(self.width_x, sideedge, sideedge)
            self.width_y = wy = self.adjustSize(self.width_y, sideedge, sideedge)

        sx = (x - wx)*.5
        sy = (y - wy)*.5

        # with self.saved_context():
        #     self.rectangularWall(x, h, [b, sideedge, t1, sideedge],
        #                          ignore_widths=[1, 6], move="up")
        #     self.rectangularWall(x, h, [b, sideedge, t3, sideedge],
        #                          ignore_widths=[1, 6], move="up")

        #     if self.bottom_edge != "e":
        #         self.rectangularWall(x, y, "ffff", move="up")
        #     self.lid(x, y)

        # self.rectangularWall(x, h, [b, sideedge, t3, sideedge],
        #                      ignore_widths=[1, 6], move="right only")
        # self.rectangularWall(y, h, [b, "f", t2, "f"],
        #                      ignore_widths=[1, 6], move="up")
        # self.rectangularWall(y, h, [b, "f", t4, "f"],
        #                      ignore_widths=[1, 6], move="up")
        
        self.polygonWall(borders=[wx, 90, sx, -90, sy, 90, wy, 90, sy, -90, sx, 90, wx, 90, sx, -90, sy, 90, wy, 90, sy, -90, sx, 90], edge=["f"], move="left", label="top",
                         callback = [None, self.hingeHoles, None, None, self.hingeHoles, None, None, self.hingeHoles, None, None, self.hingeHoles, None])
        self.polygonWall(borders=[wx, 90, sx, -90, sy, 90, wy, 90, sy, -90, sx, 90, wx, 90, sx, -90, sy, 90, wy, 90, sy, -90, sx, 90], edge=[ "E"], move="left", label="inside lid")
        self.polygonWall(borders=[wx, 90, sx, -90, sy, 90, wy, 90, sy, -90, sx, 90, wx, 90, sx, -90, sy, 90, wy, 90, sy, -90, sx, 90], edge=[ "E", "E", "E", "E", "F", "E", "E", "E", "F", "E", "E", "E"], move="left", label="inside lid")

        self.polygonWall(borders=[wx+self.thickness*2, 90, sx, -90, sy, 90, wy+self.thickness*2, 90, sy, -90, sx, 90, wx+self.thickness*2, 90, sx, -90, sy, 90, wy+self.thickness*2, 90, sy, -90, sx, 90], edge=["E"], move="left", label="outside lid")

        # self.rectangularWall(sx - self.thickness, h, ["f", "f", "e", "e"], move="down left")
        # self.rectangularWall(wx, h, ["f", "F", "e", "e"], move="left")
        side = edges.CompoundEdge(self, ["f", "e", "f"], [sx-self.thickness, wx+self.thickness*2, sx-self.thickness])


        self.rectangularWall(x, h-self.thickness*2, [side, "e", "e", "e"], move="left")

        self.rectangularWall(sx, h, ["F", "f", "E", "F"], move="down left")
        self.rectangularWall(sx, h, ["F", "f", "E", "F"], move="left")
        self.rectangularWall(wx, h, ["F", "f", "E", "F"], move="left")

        self.rectangularWall(sy, h, ["F", "f", "E", "F"], move="left")
        self.rectangularWall(sy, h, ["F", "f", "E", "F"], move="left")
        self.rectangularWall(wy, h, ["F", "f", "E", "F"], move="left")

        self.rectangularWall(sx, h, ["F", "f", "E", "F"], move="left")
        self.rectangularWall(sx, h, ["F", "f", "E", "F"], move="left")
        self.rectangularWall(wx, h, ["F", "f", "E", "F"], move="left")

        self.rectangularWall(sy, h, ["F", "f", "E", "F"], move="left")
        self.rectangularWall(sy, h, ["F", "f", "E", "F"], move="left")
        self.rectangularWall(wy, h, ["F", "f", "E", "F"], move="left")
        

        

