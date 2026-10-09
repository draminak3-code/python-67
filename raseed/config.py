"""
raseed.config
=============
Central design-token registry for the رَصِيْد (Raseed) motion-graphics brand.

Everything a scene needs that is *not* animation logic lives here:
colors, typography, timing constants and render settings.  Scenes import
these tokens instead of hard-coding values (DRY + single source of truth).

To re-brand or A/B-test a palette you edit ONE file — never a scene.
"""

from __future__ import annotations

from manim import BLACK, ManimColor, WHITE


# ---------------------------------------------------------------------------
# 1. Brand palette  — "Deep Sea Editorial"
#    Primary colors carry the identity; accents are reserved for emphasis
#    so every post feels like the same brand even across different scenes.
# ---------------------------------------------------------------------------
class Palette:
    """Immutable brand color tokens (ManimColor instances)."""

    # Core brand
    MIDNIGHT: ManimColor = ManimColor("#0B1D33")   # deep navy — primary background
    INK: ManimColor      = ManimColor("#12294A")   # slightly lighter navy — panels
    GOLD: ManimColor     = ManimColor("#C9A227")   # signature accent — headlines/keys
    TEAL: ManimColor     = ManimColor("#2E9599")   # secondary accent — data shapes
    CORAL: ManimColor    = ManimColor("#E15554")   # alert/emphasis accent (use sparingly)

    # Neutrals
    PAPER: ManimColor    = ManimColor("#F6F1E7")   # warm off-white — body text
    MIST: ManimColor     = ManimColor("#8CA3B8")   # muted blue-grey — captions
    SHADOW: ManimColor   = ManimColor("#06101F")   # deepest tone — vignettes/shadows

    # Semantic aliases (Open/Closed principle: scenes use intent, not hex)
    BACKGROUND: ManimColor = MIDNIGHT
    TEXT_PRIMARY: ManimColor = PAPER
    TEXT_SECONDARY: ManimColor = MIST
    HIGHLIGHT: ManimColor = GOLD

    @classmethod
    def gradient_stop(cls, index: int, total: int) -> ManimColor:
        """Interpolate between GOLD and TEAL for n-step geometric sequences."""
        t = 0.0 if total <= 1 else index / (total - 1)
        return cls.GOLD.interpolate(cls.TEAL, t)


# ---------------------------------------------------------------------------
# 2. Typography
#    Arabic-first: RTL-safe fonts with graceful fallbacks.  If a font is not
#    installed on the render machine, `FALLBACK` keeps renders deterministic.
# ---------------------------------------------------------------------------
class Typography:
    HEADLINE_FONT: str = "Noto Naskh Arabic"   # classical, high-contrast serif feel
    BODY_FONT: str = "Noto Sans Arabic"        # clean UI-grade sans
    LATIN_FONT: str = "Montserrat"             # numerals / latin lockups
    FALLBACK: str = "DejaVu Sans"              # guaranteed-present on Linux CI

    HEADLINE_SIZE: float = 72
    SUBHEAD_SIZE: float = 40
    BODY_SIZE: float = 28
    CAPTION_SIZE: float = 20

    LINE_SPACING: float = 1.4                  # generous for diacritics (التشكيل)


# ---------------------------------------------------------------------------
# 3. Motion language — timing constants
#    A shared "beat" keeps pacing consistent across every produced post.
# ---------------------------------------------------------------------------
class Motion:
    BEAT: float = 0.35            # one rhythmic unit; all timings are multiples
    INTRO: float = 2 * BEAT       # entrances
    HOLD: float = 4 * BEAT        # reading time for static content
    OUTRO: float = 1.5 * BEAT     # exits
    MORPH: float = 3 * BEAT       # geometry transformations
    STAGGER: float = 0.5 * BEAT   # per-element delay in sequence() helpers

    RUN_TIME: float = 12.0        # default loop length for a social post


# ---------------------------------------------------------------------------
# 4. Render defaults — consumed by CLI wrapper / manim.cfg
# ---------------------------------------------------------------------------
class Render:
    QUALITY: str = "production_quality"   # 1080p60 — maps to manim's -qh
    FPS: int = 60
    RESOLUTION: tuple[int, int] = (1920, 1080)
    MEDIA_DIR: str = "media"
    OUTPUT_TEMPLATE: str = "{scene_name}_{date}"
