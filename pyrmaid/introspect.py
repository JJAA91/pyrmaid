# -*- coding: utf-8 -*
"""Module containing logic for object introspection."""
from __future__ import annotations

import builtins
from copy import deepcopy
import logging
from abc import ABC, abstractmethod
from logging import Logger
from typing import List

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

from pyrmaid import constants as const
from pyrmaid import options as opt
from pyrmaid.parents import get_inheritance_tree

log: Logger = logging.getLogger(__file__)
builtin_types: List[type] = [getattr(builtins, d) for d in dir(builtins) if isinstance(getattr(builtins, d), type)]


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

    def build(self) -> str:
        """Method to build a class diagram UML."""
        uml: List[str] = ["classDiagram"]

        ancestry: List[str]
        members: List[str]
        members, ancestry = get_inheritance_tree(self.obj, direction=self.direction)

        for idx, obj in enumerate(ancestry):
            if idx + 1 != len(ancestry):
                uml.append(f" {const.INHERITANCE[self.direction]} ".join([obj, ancestry[idx + 1]]))

        uml.extend(members)

        composed = self._find_composed()

        for comp_obj in composed:
            uml.append(f"{self.obj.__name__} {const.COMPOSITION[self.direction]} {comp_obj}")
            uml.extend(composed[comp_obj]["members"])

        return "\n".join(uml)
    
    def _find_composed(self):
        init_anno: dict = deepcopy(self.obj.__init__.__annotations__)
        init_anno.pop("return")  # __init__ can only ever return None
        composed: dict = {}
        for cls_ in init_anno.values():
            if cls_ in builtin_types:
                # Don't care about builtins
                continue
            # If annotated type is not a built in, then find its lineage
            cls_members, cls_ancestry = get_inheritance_tree(cls_, direction=self.direction)
            composed[cls_.__name__] = {"members": cls_members, "ancestry": cls_ancestry}
        return composed
            

