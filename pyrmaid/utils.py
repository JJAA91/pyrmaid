# -*- coding: utf-8 -*
"""Module containing utility functions."""
from pyrmaid import constants as const


def get_visibility(val: str) -> str:
    """Function to deduce the implied visibility of a string.

    This string should represent a function, attribute, or property name.
    """
    if val.startswith("_") and "__" in val:
        return const.PRIVATE
    if val.startswith("_") and not val.startswith("__"):
        return const.PROTECTED
    return const.PUBLIC


def trim_leading_underscores(name: str) -> str:
    """Function to remove the leading underscores from a string."""
    while True:
        name = name if not name.startswith("_") else name[1:]
        if not name.startswith("_"):
            break
    return name
