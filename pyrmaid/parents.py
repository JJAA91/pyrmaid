# -*- coding: utf-8 -*
"""Module containing logic for finding the object inheritance."""
from typing import Any, List, Tuple

from pyrmaid import constants as const
from pyrmaid import options as opt
from pyrmaid.members import find_members


def find_parents(obj) -> List[Tuple[str, str]]:
    """Method to determine the parent classes of the object."""

    def ancestry(obj_: object, inheriters: List[Tuple[str, str]] = None) -> List[Tuple[str, str]]:
        if inheriters is None:
            inheriters = [(getattr(obj_, "__name__"), find_members(obj_))]

        parent = getattr(obj_, "__base__", const.MISSING)

        if parent is object:
            return inheriters

        obj_members = find_members(parent)
        inheriters.append((getattr(parent, "__name__", const.MISSING), obj_members))
        return ancestry(parent, inheriters)

    return ancestry(obj)


def get_inheritance_tree(obj: object, direction: opt.Direction) -> Tuple[List[str], List[str]]:
    _parents: Tuple[Any, ...]
    _members: Tuple[Any, ...]
    _parents, _members = list(zip(*find_parents(obj)))
    if direction == opt.Direction.DOWN:
        ancestry = list(_parents)[::-1]
    if direction == opt.Direction.UP:
        ancestry = list(_parents)
    members: List[str] = list(_members)
    return members, ancestry
