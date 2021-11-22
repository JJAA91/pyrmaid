# -*- coding: utf-8 -*
import abc
import logging
from logging import Logger

import pytest

from pyrmaid import constants as const
from pyrmaid import options as opt
from pyrmaid.introspect import ClassDiagram, Graph

log: Logger = logging.getLogger(__name__)


class ComposedElement:

    def __init__(self) -> None:
        self.name: str = "Giovanni Giorgio, but everybody calls me Giorgio"

    def log_name(self) -> None:
        log.info(f"My name is {self.name}")


class Implementation:

    def __init__(self, element: ComposedElement, element2: str) -> None:
        self.element: ComposedElement = element
        self.element2: str = element2
    
    def do_something(self) -> None:
        self.element.log_name()
    
    def get_name(self) -> str:
        return self.element.name


@pytest.mark.analyzer
@pytest.mark.parametrize(
    "direction",
    [
        pytest.param("up", id="UpDirection"),
        pytest.param("down", id="DownDirection"),
        pytest.param(
            "insideout",
            id="InvalidDirection",
            marks=pytest.mark.xfail(raises=ValueError, reason="Not a valid direction option", strict=True),
        ),
    ],
)
def test_composite(direction):
    uml: ClassDiagram = ClassDiagram(Implementation, direction=direction)
    graph: str = uml.build()
    log.info(graph)
    assert const.COMPOSITION[opt.Direction(direction)] in graph, "The uncorrect connector is arrow to the diagram"