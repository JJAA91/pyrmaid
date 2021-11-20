# -*- coding: utf-8 -*
# noqa
import logging
from abc import ABC, abstractmethod
from logging import Logger

import pytest

from pyrmaid import constants as const
from pyrmaid import options as opt
from pyrmaid.introspect import ClassDiagram

log: Logger = logging.getLogger(__name__)


"""
Setup objects that follow a template design.

Boilerplate from https://refactoring.guru/design-patterns/template-method/python/example#example-0
"""


class AbstractTemplate(ABC):  # noqa
    def template_method(self) -> None:  # noqa
        self.base_operation1()
        self.required_operation1()
        self.base_operation2()
        self.hook1()
        self.required_operation2()
        self.base_operation3()
        self.hook2()

    def base_operation1(self) -> None:  # noqa
        log.info("AbstractTemplate says: I am doing the bulk of the work")

    def base_operation2(self) -> None:  # noqa
        log.info("AbstractTemplate says: But I let subclasses override some operations")

    def base_operation3(self) -> None:  # noqa
        log.info("AbstractTemplate says: But I am doing the bulk of the work anyway")

    @abstractmethod
    def required_operation1(self) -> None:  # noqa
        pass

    @abstractmethod
    def required_operation2(self) -> None:  # noqa
        pass

    def hook1(self) -> None:  # noqa
        pass

    def hook2(self) -> None:  # noqa
        pass


class ConcreteImplementation1(AbstractTemplate):  # noqa
    def required_operation1(self) -> None:  # noqa
        log.info("ConcreteImplementation1 says: Implemented Operation 1")

    def required_operation2(self) -> None:  # noqa
        log.info("ConcreteImplementation1 says: Implemented Operation 2")


class ConcreteImplementation2(AbstractTemplate):  # noqa
    def required_operation1(self) -> None:  # noqa
        log.info("ConcreteImplementation2 says: Implemented Operation 1")

    def required_operation2(self) -> None:  # noqa
        log.info("ConcreteImplementation2 says: Implemented Operation 2")

    def hook1(self) -> None:  # noqa
        log.info("ConcreteImplementation2 says: Overriden Hook 1")


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
def test_template_implementation_1(direction):
    """Test inheritance is correctly inspected, and represented in the requested direction."""
    uml: ClassDiagram = ClassDiagram(ConcreteImplementation1, direction=direction)
    graph: str = uml.build()
    assert const.INHERITANCE[opt.Direction(direction)] in graph, "The uncorrect connector is arrow to the diagram"
