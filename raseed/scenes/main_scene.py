"""
raseed.scenes.main_scene
========================
Flagship sample post: "morphing geometry + typography".

The scene body is a thin, declarative choreography — every visual token
comes from config, every repeated primitive comes from core helpers.
Adding a new post = adding a new file like this one; nothing else changes.

Render:
    manim -qh --fps 60 raseed/scenes/main_scene.py RaseedMorphPost
"""

from __future__ import annotations

import numpy as np
from manim import DOWN, AnimationGroup, FadeIn, FadeOut, ReplacementTransform, Succession, Transform, UP, Write

from raseed.config import Motion, Palette, Typography
from raseed.core import text_helpers
from raseed.core.geometry_helpers import (
    OrbitRing,
    intro_animation,
    morph_step,
    shape_family,
    spin_animation,
)
from raseed.scenes.base_scene import BaseBrandScene


class RaseedMorphPost(BaseBrandScene):
    """One continuous morph chain (triangle -> ... -> circle) under a headline."""

    # ---- step 1 of the body: the geometry engine --------------------------
    def _build_geometry(self):
        self.shapes = shape_family(radius=1.35)
        self.active = self.shapes[0].copy()          # the ONE visible morphing shape
        self.active.move_to(DOWN * 0.9)
        self.ring = OrbitRing(radius=2.4).move_to(self.active)
        return self.active, self.ring

    # ---- step 2 of the body: the typographic lockup ------------------------
    def _build_typography(self):
        title = text_helpers.headline("الدائرة المعرفة").set_color(Palette.HIGHLIGHT)
        subtitle = text_helpers.subhead("من الزاوية إلى الأفق")
        kicker = text_helpers.caption("RASEED • MOTION SERIES 01")
        block = text_helpers.stack(title, subtitle, kicker, buff=0.28)
        block.move_to(UP * 2.1)
        return block

    # ---- orchestration (the only override the scene author writes) --------
    def build_content(self) -> None:
        shape, ring = self._build_geometry()
        block = self._build_typography()

        # Act I — entrances: shapes draw on, type rises in (parallel tracks)
        self.play(
            AnimationGroup(
                intro_animation(shape, ring),
                Succession(*[Write(t, run_time=Motion.INTRO / 2) for t in block]),
                lag_ratio=0.15,
            )
        )

        # Act II — the morph loop: each family member becomes the next,
        # with a rotational flourish between beats.  Pure interpolation,
        # no per-frame updaters => FFmpeg-friendly and deterministic.
        index = 0
        for _ in range(len(self.shapes)):
            nxt_index = (index + 1) % len(self.shapes)
            target = self.shapes[nxt_index].copy().move_to(shape)
            self.play(
                Transform(shape, target, path_arc=np.pi / 6, run_time=Motion.MORPH),
                spin_animation(ring.satellites, radians=np.pi / 4),
            )
            index = nxt_index

        # Act III — resolve: everything collapses into the brand word once more
        final_circle = self.shapes[-1].copy().move_to(shape).set_color(Palette.GOLD)
        self.play(
            ReplacementTransform(shape, final_circle),
            FadeIn(final_circle),
            run_time=Motion.BEAT,
        )
        self.wait(Motion.HOLD / 2)
