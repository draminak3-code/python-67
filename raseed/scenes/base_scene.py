"""
raseed.scenes.base_scene
========================
Template-method base class for every Raseed post.

`BaseBrandScene` owns the *skeleton* of a post (background -> intro ->
content -> outro) while concrete scenes only implement `build_content()`.
This is the Template Method pattern: invariants (brand frame, pacing,
safe margins) can't be forgotten by an authoring scene, and changing the
frame once changes it everywhere (DRY, Open/Closed).
"""

from __future__ import annotations

from manim import DOWN, Rectangle, Scene, Text, UP, FadeIn, FadeOut, VGroup

from raseed.config import Motion, Palette, Render, Typography
from raseed.core import text_helpers


class BaseBrandScene(Scene):
    """Abstract skeleton — subclasses override build_content() only."""

    # Social posts are usually 9:16 or 1:1; keep content inside a safe box.
    SAFE_MARGIN_X: float = 0.85   # fraction of half-width actually used
    SAFE_MARGIN_Y: float = 0.80

    def setup(self) -> None:
        self.camera.background_color = Palette.BACKGROUND
        self.brand_frame = self._make_brand_frame()
        self.add(self.brand_frame)

    # ---- overridable hooks (each tiny, single-responsibility) ------------
    def play_intro(self) -> None:
        """Wordmark sting that opens every رَصِيْد post."""
        mark = text_helpers.headline("رَصِيْد")
        mark.scale(0.5).move_to(self.brand_frame.get_bottom() + DOWN * 0.4)
        self.play(FadeIn(mark, shift=UP * 0.3), run_time=Motion.INTRO)
        self.brand_mark = mark

    def build_content(self) -> None:
        """Concrete scenes implement the actual animation body here."""
        raise NotImplementedError

    def play_outro(self) -> None:
        body = VGroup(*[m for m in self.mobjects if m is not self.brand_frame])
        self.play(FadeOut(body, run_time=Motion.OUTRO))

    # ---- template method --------------------------------------------------
    def construct(self) -> None:
        """Fixed pipeline; no scene logic belongs in this method."""
        self.play_intro()
        self.build_content()
        self.play_outro()

    # ---- shared furniture -------------------------------------------------
    def _make_brand_frame(self) -> Rectangle:
        w = self.camera.frame_width * self.SAFE_MARGIN_X
        h = self.camera.frame_height * self.SAFE_MARGIN_Y
        frame = Rectangle(width=w, height=h)
        frame.set_stroke(Palette.GOLD, width=1.5, opacity=0.35)
        frame.set_fill(opacity=0)
        return frame
