# -*- coding: utf-8 -*
"""Module containing logic for object introspection."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from logging import Logger
from typing import Any, List, Tuple

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

from pyrmaid import constants as const
from pyrmaid import options as opt
from pyrmaid.members import find_members

log: Logger = logging.getLogger(__file__)


class Graph:
    """Interface class for creating the UML."""

    def __init__(self, strategy: GraphStrategy) -> None:
        self.strategy: GraphStrategy = strategy

    @property
    def strategy(self) -> GraphStrategy:
        """The diagram strategy to implement."""
        return self._strategy

    @strategy.setter
    def strategy(self, val) -> None:
        self._strategy = val

    def generate(self) -> str:
        """Method for implementing the UML string generator strategy."""
        graph: str = self.strategy.build()
        env: Environment = Environment(  # type: ignore
            loader=FileSystemLoader(const.TEMPLATES), autoescape=select_autoescape()
        )
        template: Template = env.get_template(f"{opt.Templates.SIMPLE}.html.jinja")  # type: ignore
        return template.render(uml_string=graph)


class GraphStrategy(ABC):
    """Abstract base class for implementing a graphing strategy."""

    @abstractmethod
    def build(self) -> str:
        """Abstract method to implement the UML diagram build logic."""
        pass


class ClassDiagram(GraphStrategy):
    """Concrete implementation of the GraphStrategy."""

    def __init__(self, obj: object, direction: str = "down") -> None:
        self.obj: object = obj
        self.direction: opt.Direction = opt.Direction(direction)
        self.ancestry: List[str]

        _ancestry: List[Tuple[str, str]] = self._find_parents()
        _parents: Tuple[Any, ...]
        _members: Tuple[Any, ...]
        _parents, _members = list(zip(*_ancestry))
        if self.direction == opt.Direction.DOWN:
            self.ancestry = list(_parents)[::-1]
        if self.direction == opt.Direction.UP:
            self.ancestry = list(_parents)
        self.members: List[str] = list(_members)

    def build(self) -> str:
        """Method to build a class diagram UML."""
        uml: List[str] = ["classDiagram"]

        for idx, obj in enumerate(self.ancestry):
            if idx + 1 != len(self.ancestry):
                uml.append(f" {const.INHERITANCE[self.direction]} ".join([obj, self.ancestry[idx + 1]]))

        uml.extend(self.members)

        return "\n".join(uml)

    def _find_parents(self) -> List[Tuple[str, str]]:
        """Method to determine the parent classes of the object."""

        def ancestry(obj: object, inheriters: List[Tuple[str, str]] = None) -> List[Tuple[str, str]]:
            if inheriters is None:
                inheriters = [(getattr(self.obj, "__name__"), find_members(obj))]

            parent = getattr(obj, "__base__", const.MISSING)

            if parent is object:
                return inheriters

            obj_members = find_members(parent)
            inheriters.append((getattr(parent, "__name__", const.MISSING), obj_members))
            return ancestry(parent, inheriters)

        return ancestry(self.obj)
