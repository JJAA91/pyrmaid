# -*- coding: utf-8 -*
"""Module containing definitions of constants for diagrams."""
from os import PathLike
from pathlib import Path
from typing import Dict, Final

from pyrmaid import options as opt

"""
Class diagram relationship types
"""

INHERITANCE: Final[Dict[opt.Direction, str]] = {opt.Direction.UP: "<|--", opt.Direction.DOWN: "--|>"}
COMPOSITION: Final[Dict[opt.Direction, str]] = {opt.Direction.UP: "*--", opt.Direction.DOWN: "--*"}
AGGREGATION: Final[Dict[opt.Direction, str]] = {opt.Direction.UP: "o--", opt.Direction.DOWN: "--o"}
ASSOCIATION: Final[Dict[opt.Direction, str]] = {opt.Direction.UP: "<--", opt.Direction.DOWN: "-->"}
DEPENDENCY: Final[Dict[opt.Direction, str]] = {opt.Direction.UP: "<..", opt.Direction.DOWN: "..>"}
REALIZATION: Final[Dict[opt.Direction, str]] = {opt.Direction.UP: "<|..", opt.Direction.DOWN: "..|>"}

"""
Class diagram link types
"""

LINK_SOLID: Final[str] = "--"
LINK_DASHED: Final[str] = ".."

"""
Class Diagram Visibility
"""

PUBLIC: Final[str] = "+"
PRIVATE: Final[str] = "-"
PROTECTED: Final[str] = "#"
PACKAGE: Final[str] = "~"

"""
Class Diagram method classifiers
"""

ABSTRACT: Final[str] = "*"
STATIC: Final[str] = "$"  # Also a compatible field classifier

"""
Locations
"""

TEMPLATES: Final[PathLike] = Path(__file__).parent / "templates"

"""
Sentinal
"""

MISSING: Final = type("MISSING", (), {})()
