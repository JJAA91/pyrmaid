# -*- coding: utf-8 -*
"""Module containing definitions of constants for diagrams."""
from pathlib import Path
from typing import Final

from pyrmaid import options as opt

"""
Class diagram relationship types
"""

INHERITANCE: Final = {opt.Direction.UP: "<|--", opt.Direction.DOWN: "--|>"}
COMPOSITION: Final = ("*--", "--*")
AGGREGATION: Final = ("o--", "--o")
ASSOCIATION: Final = ("<--", "-->")
DEPENDENCY: Final = ("<..", "..>")
REALIZATION: Final = ("<|..", "..|>")

"""
Class diagram link types
"""

LINK_SOLID: Final = "--"
LINK_DASHED: Final = ".."

"""
Class Diagram Visibility
"""

PUBLIC: Final = "+"
PRIVATE: Final = "-"
PROTECTED: Final = "#"
PACKAGE: Final = "~"

"""
Class Diagram method classifiers
"""

ABSTRACT: Final = "*"
STATIC: Final = "$"  # Also a compatible field classifier

"""
Locations
"""

TEMPLATES: Final = Path(__file__).parent / "templates"

"""
Sentinal
"""

MISSING: Final = type("MISSING", (), {})()
