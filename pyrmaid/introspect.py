# -*- coding: utf-8 -*
"""Module containing logic for object introspection."""
from __future__ import annotations

import inspect
import logging
from abc import ABC, abstractmethod
from functools import singledispatch
from logging import Logger
from types import FunctionType
from typing import Any, List, Tuple, Type, Union

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

from pyrmaid import constants as const
from pyrmaid import options as opt
from pyrmaid import utils

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
                inheriters = [(getattr(self.obj, "__name__"), self._find_members(obj))]

            parent = getattr(obj, "__base__", const.MISSING)

            if parent is object:
                return inheriters

            obj_members = self._find_members(parent)
            inheriters.append((getattr(parent, "__name__", const.MISSING), obj_members))
            return ancestry(parent, inheriters)

        return ancestry(self.obj)

    @staticmethod
    def _find_members(obj: object) -> str:
        """Method to find the methods associated with the object."""

        def order_func(line: str) -> int:
            lut: dict = {const.PUBLIC: 0, const.PROTECTED: 1, const.PRIVATE: 2}
            return lut[line[0]]

        content: List[str] = [f"class {getattr(obj, '__name__')}{{"]

        # Inspect the class for methods and properties
        for key, val in obj.__dict__.items():
            member: Union[List[str], str] = member_string(val, key, obj=obj)
            if member is not const.MISSING:
                if isinstance(member, list):
                    content.extend(member)
                    continue
                content.append(member)
        content = [content[0]] + list(sorted(content[1:], key=order_func))
        content.append("}")
        return "\n".join(content)


@singledispatch
def member_string(member: Any, key: str = "", **kwargs) -> Union[List[str], str]:
    """Generate a mermaid-compatible string for the object member.

    Unsupported members returns const.MISSING
    """
    return const.MISSING


@member_string.register
def _static_method_member(member: staticmethod, key: str = "", **kwargs) -> str:
    if key.startswith("__") and key.endswith("__"):
        # Ignore dunder methods
        return const.MISSING

    sig: inspect.Signature = inspect.signature(member.__func__)
    params: str = f"({', '.join(arg for arg in sig.parameters if arg != 'self')})"
    return_anno: str = str(Type[sig.return_annotation]).split("typing.Type[")[1][:-1]
    return f"{utils.get_visibility(key)}{key}{params}{const.STATIC} {return_anno}"


@member_string.register
def _method_member(member: FunctionType, key: str = "", **kwargs) -> str:
    if key.startswith("__") and key.endswith("__"):
        # Ignore dunder methods
        return const.MISSING

    method_type = const.ABSTRACT if getattr(member, "__isabstractmethod__", False) else ""

    sig: inspect.Signature = inspect.signature(member)
    params: str = f"({', '.join(arg for arg in sig.parameters if arg != 'self')})"
    return_anno: str = str(Type[sig.return_annotation]).split("typing.Type[")[1][:-1]
    return f"{utils.get_visibility(key)}{key}{params}{method_type} {return_anno}"


@member_string.register
def _property_member(member: property, key: str = "", **kwargs) -> str:
    obj = kwargs.get("obj") or const.MISSING

    if obj is const.MISSING:
        return const.MISSING

    return_annotation: str
    src: List[str] = inspect.getsourcelines(obj)[0]
    for line in src:
        if f"def {key}" in line:
            return_annotation = line.split("-> ")[1].split(":")[0]
            return f"{utils.get_visibility(key)}{return_annotation} {key if not key.startswith('_') else key[1:]}"
        # Check for mangled names
        if "__" in key:
            mangled: str = key.split("__")[1]
            if f"def __{mangled}" in line:
                return_annotation = line.split("-> ")[1].split(":")[0]
                return f"{utils.get_visibility(f'__{mangled}')}{return_annotation} {mangled}"
    else:
        return const.MISSING


@member_string.register
def _annotated_fields(member: dict, key: str = "", **kwargs) -> List[str]:
    if key != "__annotations__":
        return const.MISSING

    obj = kwargs.get("obj") or const.MISSING

    if obj is const.MISSING:
        return const.MISSING

    # iterate over the fields
    member_elements: List[str] = []
    field_name: str
    for name, anno in member.items():
        field_name = name
        if obj.__name__ in field_name:  # Check for mangled names
            field_name = name.split(obj.__name__)[1]  # remove the leading dunder
        vis: str = utils.get_visibility(field_name)
        while True:
            field_name = field_name if not field_name.startswith("_") else field_name[1:]
            if not field_name.startswith("_"):
                break
        member_elements.append(f"{vis}{anno.__name__} {field_name}")
    return member_elements
