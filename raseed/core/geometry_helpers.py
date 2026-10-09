"""
raseed.core.geometry_helpers
============================
Brand-grade shape factory + animation recipes.

Encapsulates the "morphing geometry" language of رَصِيْد posts:
polygons that share vertex counts so `Transform` interpolates cleanly
(no popping), plus a rotating orbit ring built with efficient
numpy-based placement rather than per-frame updaters where possible.
"""

from __future__ import annotations

import numpy as np
from manim import (
    Circle,
    FadeIn,
    FadeOut,
    Group,
    RegularPolygon,
    Rotate,
    Succession,
    Transform,
    VMobject,
    VGroup,
    Write,
)

from raseed.config import Motion, Palette


class MorphShape(VMobject):
    """A single regular polygon rendered at HIGH vertex resolution.

    Why? Manim's `Transform` between two VMobjects interpolates matching
    sub-paths point-by-point.  If source and target have different vertex
    counts you get ugly "popping".  By building every member of the shape
    family (triangle -> square -> pentagon -> hexagon -> circle) with the
    same number of anchor points, any-to-any morph becomes pure coordinate
    interpolation: cheap to compute, buttery to render through FFmpeg.
    """

    def __init__(self, n_sides: int, radius: float = 1.4) -> None:
        super().__init__()
        self.radius = radius
        # Build the polygon geometry ourselves (numpy): guarantees every
        # family member has an identical point count for clean morphs and
        # avoids fragile VMobject subclassing.
        verts = np.array(
            [
                radius * np.array([np.cos(a), np.sin(a), 0.0])
                for a in np.linspace(np.pi / 2, np.pi / 2 + 2 * np.pi, n_sides, endpoint=False)
            ]
        )
        self.set_points_as_corners(self._resample(verts))
        self.set_stroke(width=3)
        self.set_fill(opacity=0.12)

    @staticmethod
    def _resample(vertices, samples_per_edge: int = 15):
        """Linearly resample polygon edges into a fixed-size point list."""
        verts = np.append(vertices, [vertices[0]], axis=0)
        pts = []
        for a, b in zip(verts[:-1], verts[1:]):
            ts = np.linspace(0, 1, samples_per_edge, endpoint=False)
            pts.extend(a + (b - a) * t for t in ts)
        pts.append(verts[-1])
        return np.array(pts)


def shape_family(radius: float = 1.4) -> list[MorphShape]:
    """Ordered morph chain: triangle, square, pentagon, hexagon, circle."""
    family = [MorphShape(n, radius) for n in (3, 4, 5, 6)]
    circle = Circle(radius=radius).set_stroke(width=3).set_fill(opacity=0.12)
    family.append(circle)
    for i, shape in enumerate(family):
        shape.set_color(Palette.gradient_stop(i, len(family)))
    return family


class OrbitRing(Group):
    """Decorative satellite dots on a guide circle — brand 'system' motif."""

    def __init__(self, radius: float = 2.6, dots: int = 8, dot_r: float = 0.07) -> None:
        angles = np.linspace(0, 2 * np.pi, dots, endpoint=False)
        satellites = VGroup(
            *[
                Circle(radius=dot_r)
                .set_color(Palette.gradient_stop(i, dots))
                .move_to(radius * np.array([np.cos(a), np.sin(a), 0.0]))
                for i, a in enumerate(angles)
            ]
        )
        guide = Circle(radius=radius, stroke_width=1.5).set_stroke(
            Palette.MIST, opacity=0.35
        )
        super().__init__(guide, satellites)
        self.satellites = satellites


# ---------------------------------------------------------------------------
# Composite animation recipes (each returns ONE Animation object — scenes
# stay declarative; pacing is centralized in config.Motion).
# ---------------------------------------------------------------------------
def intro_animation(first_shape: VMobject, ring: OrbitRing) -> Succession:
    """Write the first shape, then fade the orbit ring in behind it."""
    return Succession(
        Write(first_shape, run_time=Motion.INTRO),
        FadeIn(ring, lag_ratio=0.05, run_time=Motion.INTRO / 2),
    )


def morph_step(shapes: list[VMobject], current_index: int) -> tuple[Transform, int]:
    """Return (animation, new_index) for the next step of the morph loop."""
    nxt = (current_index + 1) % len(shapes)
    anim = Transform(
        shapes[current_index],
        shapes[nxt],
        path_arc=np.pi / 6,          # slight arc = organic feel, still O(1) math
        run_time=Motion.MORPH,
    )
    return anim, nxt


def outro_animation(*mobjects) -> FadeOut:
    """Single unified exit — every post ends the same way (brand consistency)."""
    return FadeOut(Group(*mobjects), run_time=Motion.OUTRO)


def spin_animation(mobj, radians: float = np.pi / 3) -> Rotate:
    """Small rotational flourish used between morph beats."""
    return Rotate(mobj, angle=radians, about_point=mobj.get_center(), run_time=Motion.BEAT)
