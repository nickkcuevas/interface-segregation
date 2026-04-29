# app/interfaces/logging.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type

from app.models import Employee, Order


class OrderLogger(ABC):
    """Base logger enforcing a small, focused interface (ISP)."""

    def __init__(self, order: Order, employee: Employee):
        self._order = order
        self._employee = employee

    @classmethod
    def new_for(cls: Type["OrderLogger"], action: str, employee: Employee, order: Order) -> "OrderLogger":
        for subclass in cls.__subclasses__():
            if subclass.action() == action:
                return subclass(order=order, employee=employee)
        raise ValueError(f"No logger for action={action!r}")

    @abstractmethod
    def log(self):
        """Perform the logging action."""
        ...

    @classmethod
    @abstractmethod
    def action(cls) -> str:
        """Action type this logger handles."""
        ...