# -*- coding: utf-8 -*
"""Module for defining option enumerations."""
from enum import Enum, EnumMeta, auto
from typing import Tuple

__all__ = ["Templates", "Direction"]


class StrEnumMeta(EnumMeta):
    """Custom enum implementation."""

    def __contains__(cls, item) -> bool:
        """Provide logic for performing membership test of item in options."""
        return item in cls.__members__.values()

    @property
    def values(cls) -> Tuple[str, ...]:
        """Enum class fields as a list."""
        return tuple(item.value for item in cls)  # type: ignore


class StrEnum(str, Enum, metaclass=StrEnumMeta):
    """Base class for options enumerations."""

    def _generate_next_value_(name, start, count, last_values) -> str:  # type: ignore
        return str(name).lower()


class Templates(StrEnum):
    """Enum for the available templates to render the UML strings in to."""

    SIMPLE = auto()


class Direction(StrEnum):
    """Enum for the diagram direction options."""

    UP = auto()
    DOWN = auto()
