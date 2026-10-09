"""
raseed.core.text_helpers
========================
Reusable typography factory + animation recipes (DRY).

Every scene that needs brand text calls these instead of re-writing
Text() kwargs and fade logic.  Font resolution is defensive: if the
brand font is missing on the render box it silently falls back, so CI
renders never crash.
"""

from __future__ import annotations

from manim import DOWN, Text, VGroup

from raseed.config import Palette, Typography


def _resolve_font(preferred: str) -> str:
    """Return *preferred* if installed, else the deterministic fallback."""
    try:
        from manimpango import PangoFontInfo  # bundled with manim

        if preferred in {f for f in PangoFontInfo().get_all_pango_fonts()}:
            return preferred
    except Exception:  # pragma: no cover - environment dependent
        pass
    return Typography.FALLBACK


def headline(text: str, color: "Palette" = Palette.HIGHLIGHT) -> Text:
    """Brand display type — used for the main word of a post."""
    return Text(
        text,
        font=_resolve_font(Typography.HEADLINE_FONT),
        font_size=Typography.HEADLINE_SIZE,
        weight="BOLD",
        line_spacing=Typography.LINE_SPACING,
        color=color,
    )


def subhead(text: str) -> Text:
    return Text(
        text,
        font=_resolve_font(Typography.BODY_FONT),
        font_size=Typography.SUBHEAD_SIZE,
        color=Palette.TEXT_PRIMARY,
        line_spacing=Typography.LINE_SPACING,
    )


def caption(text: str) -> Text:
    return Text(
        text,
        font=_resolve_font(Typography.BODY_FONT),
        font_size=Typography.CAPTION_SIZE,
        color=Palette.TEXT_SECONDARY,
        slant="ITALIC",
        line_spacing=Typography.LINE_SPACING,
    )


def stack(*mobjects, buff: float = 0.35) -> VGroup:
    """Vertically stack brand text with consistent rhythm."""
    group = VGroup(*mobjects).arrange(DOWN, buff=buff, aligned_edge="CENTER")
    return group
