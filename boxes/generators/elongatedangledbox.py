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

import math

from boxes import *


class ElongatedAngledBox(Boxes):
    """Angled box with a flat section inserted along the short axis (small polygon corners on an elongated body)"""

    ui_group = "Box"

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.buildArgParser("x", "y", "h", "outside", "bottom_edge")
        self.argparser.add_argument(
            "--n",  action="store", type=int, default=3,
            help="number of walls at one side (use odd values to enable ly)")
        self.argparser.add_argument(
            "--ly",  action="store", type=float, default=30.0,
            help="minimum length of the short side (tip edge perpendicular to the long axis); ignored for even n; has no effect when the natural polygon side is already longer")
        self.argparser.add_argument(
            "--top",  action="store", type=str, default="none",
            choices=["none", "angled hole", "angled hole split", "angled lid", "angled lid2"],
            help="style of the top and lid")
        self.argparser.add_argument(
            "--rim_width",  action="store", type=float, default=0.0,
            help="width of the rim around the hole for 'angled hole' and 'angled hole split' tops; 0 uses 2x material thickness. Values below thickness are clamped because finger-joint slots cut that deep into the rim")

    def _elongation(self, y, n, ly):
        """Flat section length needed so the short side is at least ly.

        With apothem (y - E)/2, the polygon side is s = (y - E) * tan(pi/(2n+2)).
        The short (tip) edge length is s + E; solving s + E = ly gives E.
        """
        if not (n % 2) or ly <= 0:
            return 0
        t = math.tan(math.pi / (2 * n + 2))
        s_natural = y * t
        if ly <= s_natural:
            return 0
        return (ly - s_natural) / (1 - t)

    def floor(self, x, y, n, elongation, edge='e', hole=None, move=None, callback=None, label=""):
        r, h, side  = self.regularPolygon(2*n+2, h=(y - elongation)/2.0)
        t = self.thickness

        if n % 2:
            lx = x - 2 * h + side
        else:
            lx = x - 2 * r + side

        tip_edges = [side] * n
        if elongation and n % 2:
            tip_edges[n // 2] = side + elongation
        edges_full = ([lx] + tip_edges) * 2

        edge = self.edges.get(edge, edge)

        tx = x + 2 * edge.spacing()
        ty = y + 2 * edge.spacing()

        if self.move(tx, ty, move, before=True):
            return

        self.moveTo((tx-lx)/2., edge.margin())

        if hole:
            rim_w = self.rim_width if self.rim_width > 0 else 2 * t
            with self.saved_context():
                hr, hh, hside  = self.regularPolygon(2*n+2, h=(y - elongation)/2.0 - rim_w)
                dx = side - hside
                hlx = lx - dx

                htip_edges = [hside] * n
                if elongation and n % 2:
                    htip_edges[n // 2] = hside + elongation
                hedges_full = ([hlx] + htip_edges) * 2

                self.moveTo(dx/2.0, rim_w+edge.spacing())
                for i, l in enumerate(hedges_full):
                    self.edge(l)
                    self.corner(360.0/(2*n + 2))

        for i, l in enumerate(edges_full):
            self.cc(callback, i, 0, edge.startWidth() + self.burn)
            edge(l)
            self.edgeCorner(edge, edge, 360.0/(2*n + 2))

        self.move(tx, ty, move, label=label)

    def _split_geometry(self, x, y, n, elongation):
        rim_w = self.rim_width if self.rim_width > 0 else 2 * self.thickness
        r, hp, side = self.regularPolygon(2*n + 2, h=(y - elongation) / 2.0)
        hr, hh, hside = self.regularPolygon(2*n + 2, h=(y - elongation) / 2.0 - rim_w)
        if n % 2:
            lx = x - 2 * hp + side
        else:
            lx = x - 2 * r + side
        dx = side - hside
        hlx = lx - dx
        diag = math.hypot(dx / 2.0, rim_w)
        alpha = math.degrees(math.atan2(rim_w, dx / 2.0)) if dx > 0 else 90.0
        return r, hp, side, hside, lx, hlx, diag, alpha

    def floor_strip(self, x, y, n, elongation, edge='F', move=None, label=""):
        """Rim strip covering one long straight section.
        Outer long edge mates with the wall (finger joints); the other three
        sides are plain butt edges."""
        edge = self.edges.get(edge, edge)
        rim_w = self.rim_width if self.rim_width > 0 else 2 * self.thickness

        _, _, _, _, lx, hlx, diag, alpha = self._split_geometry(x, y, n, elongation)

        tx = lx + 2 * edge.spacing()
        ty = rim_w + 2 * edge.spacing()

        if self.move(tx, ty, move, before=True):
            return

        # Start at outer F edge's left corner. Plain self.corner() at each
        # corner (no edgeCorner extensions) so the inner edge sits exactly
        # rim_w from the outer F edge, matching the tip pieces.
        self.moveTo(edge.margin(), edge.margin())

        edge(lx)
        self.corner(180.0 - alpha)
        self.edge(diag)
        self.corner(alpha)
        self.edge(hlx)
        self.corner(alpha)
        self.edge(diag)

        self.move(tx, ty, move, label=label)

    def floor_tip(self, x, y, n, elongation, edge='F', move=None, label=""):
        """Rim piece covering one polygon-tip section.
        n outer tip edges mate with walls (finger joints); the n inner edges
        and the two short butt-joint sides are plain."""
        edge = self.edges.get(edge, edge)
        rim_w = self.rim_width if self.rim_width > 0 else 2 * self.thickness

        r, hp, side, hside, _, _, diag, alpha = self._split_geometry(x, y, n, elongation)

        theta = 360.0 / (2 * n + 2)
        extra = elongation if (elongation and n % 2) else 0
        dx_half = (side - hside) / 2.0

        # Max +x extent of outer tip measured from A, by walking the tip edges.
        bump = 0.0
        x_running = 0.0
        for j in range(1, n + 1):
            seg_len = side + elongation if (elongation and n % 2 and (j - 1) == n // 2) else side
            x_running += seg_len * math.cos(math.radians(j * theta))
            bump = max(bump, x_running)

        tx = dx_half + bump + 2 * edge.spacing()
        ty = 2 * hp + extra + 2 * edge.spacing()

        if self.move(tx, ty, move, before=True):
            return

        # Place A at local (spacing + dx_half, spacing). Start mid-bottom-butt heading
        # -alpha toward A. All corners use plain self.corner() (no edgeCorner extensions)
        # so the loop closes exactly and the piece is top/bottom symmetric.
        sx = edge.spacing() + dx_half / 2.0
        sy = edge.spacing() + rim_w / 2.0

        self.moveTo(sx, sy, -alpha)

        self.edge(diag / 2.0)
        self.corner(theta + alpha)

        for i in range(n):
            l = side + elongation if (elongation and n % 2 and i == n // 2) else side
            edge(l)
            if i < n - 1:
                self.corner(theta)

        self.corner(180.0 + alpha - n * theta)
        self.edge(diag)
        self.corner(n * theta - alpha)

        for i in range(n):
            inv_i = n - 1 - i
            hl = hside + elongation if (elongation and n % 2 and inv_i == n // 2) else hside
            self.edge(hl)
            if i < n - 1:
                self.corner(-theta)

        self.corner(180.0 - alpha - theta)
        self.edge(diag / 2.0)

        self.move(tx, ty, move, label=label)

    def inner_lid(self, x, y, n, elongation, edge='E', move=None, label=""):
        """Lid shaped to fit inside the hole of an 'angled hole' / 'angled hole split' rim."""
        edge = self.edges.get(edge, edge)
        rim_w = self.rim_width if self.rim_width > 0 else 2 * self.thickness

        hr, hp_in, hside = self.regularPolygon(2*n + 2, h=(y - elongation) / 2.0 - rim_w)
        _, _, _, _, _, hlx, _, _ = self._split_geometry(x, y, n, elongation)

        htip_edges = [hside] * n
        if elongation and n % 2:
            htip_edges[n // 2] = hside + elongation
        hedges_full = ([hlx] + htip_edges) * 2

        if n % 2:
            inner_x = hlx + 2 * hp_in - hside
        else:
            inner_x = hlx + 2 * hr - hside
        inner_y = y - 2 * rim_w

        tx = inner_x + 2 * edge.spacing()
        ty = inner_y + 2 * edge.spacing()

        if self.move(tx, ty, move, before=True):
            return

        self.moveTo((tx - hlx) / 2., edge.margin())

        for i, l in enumerate(hedges_full):
            edge(l)
            self.edgeCorner(edge, edge, 360.0 / (2*n + 2))

        self.move(tx, ty, move, label=label)

    def render(self):

        x, y, h, n = self.x, self.y, self.h, self.n
        ly = self.ly
        b = self.bottom_edge

        if n < 1:
            n = self.n = 1

        if n % 2 == 0:
            ly = 0

        if x < y:
            x, y = y, x

        if self.outside:
            x = self.adjustSize(x)
            y = self.adjustSize(y)
            if self.top == "none":
                h = self.adjustSize(h, False)
            elif "lid" in self.top and self.top != "angled lid":
                h = self.adjustSize(h) - self.thickness
            else:
                h = self.adjustSize(h)

        if ly >= y:
            raise ValueError(f"ly ({ly}) must be smaller than y ({y})")

        t = self.thickness

        elongation = self._elongation(y, n, ly)

        r, hp, side  = self.regularPolygon(2*n+2, h=(y - elongation)/2.0)

        if n % 2:
            lx = x - 2 * hp + side
        else:
            lx = x - 2 * r + side

        fingerJointSettings = copy.deepcopy(self.edges["f"].settings)
        fingerJointSettings.setValues(self.thickness, angle=360./(2 * (n+1)))
        fingerJointSettings.edgeObjects(self, chars="gGH")

        with self.saved_context():
            if b != "e":
                self.floor(x, y, n, elongation, edge='f', move="right", label="Bottom")
            if self.top == "angled lid":
                self.floor(x, y, n, elongation, edge='e', move="right", label="Lower Lid")
                self.floor(x, y, n, elongation, edge='E', move="right", label="Upper Lid")
            elif self.top in ("angled hole", "angled lid2"):
                self.floor(x, y, n, elongation, edge='F', move="right", hole=True, label="Top Rim and Lid")
                if self.top == "angled lid2":
                    self.floor(x, y, n, elongation, edge='E', move="right", label="Upper Lid")
            elif self.top == "angled hole split":
                self.floor_strip(x, y, n, elongation, edge='F', move="right", label="Top Rim Strip 1")
                self.floor_strip(x, y, n, elongation, edge='F', move="right", label="Top Rim Strip 2")
                self.floor_tip(x, y, n, elongation, edge='F', move="right", label="Top Rim Tip 1")
                self.floor_tip(x, y, n, elongation, edge='F', move="right", label="Top Rim Tip 2")
                self.floor(x, y, n, elongation, edge='E', move="right", label="Outer Lid")
                self.inner_lid(x, y, n, elongation, edge='E', move="right", label="Inner Lid")
        self.floor(x, y, n, elongation, edge='F', move="up only")

        fingers = self.top in ("angled lid2", "angled hole", "angled hole split")

        cnt = 0
        for j in range(2):
            cnt += 1
            if j == 0 or n % 2:
                self.rectangularWall(lx, h, move="right",
                                 edges=b+"GfG" if fingers else b+"GeG",
                                 label=f"wall {cnt}")
            else:
                self.rectangularWall(lx, h, move="right",
                                 edges=b+"gfg" if fingers else b+"geg",
                                 label=f"wall {cnt}")
            for i in range(n):
                cnt += 1
                wall_length = side + elongation if (elongation and n % 2 and i == n // 2) else side
                if (i+j*((n+1)%2)) % 2: # reverse for second half if even n
                    self.rectangularWall(wall_length, h, move="right",
                                         edges=b+"GfG" if fingers else b+"GeG",
                                         label=f"wall {cnt}")
                else:
                    self.rectangularWall(wall_length, h, move="right",
                                         edges=b+"gfg" if fingers else b+"geg",
                                         label=f"wall {cnt}")
