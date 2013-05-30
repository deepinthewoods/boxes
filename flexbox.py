#!/usr/bin/python

import boxes
import math

class FlexBox(boxes.Boxes):
    def __init__(self, x, y, z, r=None, thickness=3.0):
        c4 = math.pi * r * 0.5
        self.x = x
        self.y = y
        self.z = z
        self.r = r or min(x, y)/2.0
        width = 2*x + 2*y - 8*r + 4*c4 + 4*thickness
        height = y + z + 40
        boxes.Boxes.__init__(self, width, height, thickness=thickness)
        
    @boxes.restore
    def flexBoxSide(self, x, y, r, callback=None):
        space, finger = self.fingerJointSettings
        lock = 2.1*space + finger

        self.moveTo(r, 0)
        for i, l in zip(range(2), (x, y)):
            self.cc(callback, i)
            self.fingerJoint(l-2*r)
            self.corner(90, r)
        self.cc(callback, 2)
        self.edge(x-2*r)
        self.corner(90, r)
        self.cc(callback, 3)
        self.fingerJoint(lock)
        self.cc(callback, 4)
        self.fingerJoint(y-2*r-lock)
        self.corner(90, r)

    def surroundingWall(self):
        x, y, z, r = self.x, self.y, self.z, self.r
        
        c4 = math.pi * r * 0.5

        space, finger = self.fingerJointSettings
        lock = 2.1*space + finger

        self.fingerJoint(y-2*r-lock, False)
        self.flex(c4, z+2*self.thickness)
        self.fingerJoint(x-2*r, False)
        self.flex(c4, z+2*self.thickness)
        self.fingerJoint(y-2*r, False)
        self.flex(c4, z+2*self.thickness)
        self.edge(x-2*r)
        self.flex(c4, z+2*self.thickness)
        self.fingerJoint(lock, False)
        self.corner(90)
        self.edge(z+2*self.thickness)
        self.corner(90)
        self.fingerJoint(lock, False)
        self.edge(c4)
        self.edge(x-2*r)
        self.edge(c4)
        self.fingerJoint(y-2*r, False)
        self.edge(c4)
        self.fingerJoint(x-2*r, False)
        self.edge(c4)
        self.fingerJoint(y-2*r-lock, False)
        self.corner(90)
        self.edge(z+2*self.thickness)
        self.corner(90)

    def render(self):
        self.moveTo(self.thickness, self.thickness)
        self.surroundingWall()
        self.moveTo(self.thickness, self.z+4*self.thickness)
        self.flexBoxSide(self.x, self.y, self.r)
        self.moveTo(2*self.x+3*self.thickness, 0)
        self.ctx.scale(-1, 1)
        self.flexBoxSide(self.x, self.y, self.r)
        self.ctx.stroke()
        self.surface.flush()


if __name__=="__main__":
    b = FlexBox(200, 200, 200, r=50)
    b.render()