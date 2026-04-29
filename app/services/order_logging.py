# app/services/order_logging.py
from __future__ import annotations

from app.interfaces.logging import OrderLogger
from app.models import (
    Employee,
    EmployeeOrderLog,
    Order,
    ORDER_LOGS,
)


def to_cents(amount_str: str) -> int:
    """
    Very naive conversion "12.34" -> 1234.
    Production code should be more robust.
    """
    try:
        return int(round(float(amount_str) * 100))
    except Exception:
        return 0


class OrderCreatedLogger(OrderLogger):
    def log(self) -> EmployeeOrderLog:
        log = EmployeeOrderLog(
            action_type=self.action(),
            employee_id=self._employee.pk,
            employee_first_name=self._employee.first_name,
            employee_last_name=self._employee.last_name,
            employee_permission_set=self._employee.permission_set,
            order_id=self._order.id,
            business=self._order.restaurant,
            order_total=self._order.total_cents,
            tips_received=self._order.tips_cents,
            surcharge_received=self._order.surcharge_fee_cents,
            discount_applied=to_cents(self._order.discount_amount),
        )
        ORDER_LOGS.append(log)
        return log

    @classmethod
    def action(cls) -> str:
        return "create"


class OrderRefundedLogger(OrderLogger):
    def log(self) -> EmployeeOrderLog:
        log = EmployeeOrderLog(
            action_type=self.action(),
            employee_id=self._employee.pk,
            employee_first_name=self._employee.first_name,
            employee_last_name=self._employee.last_name,
            employee_permission_set=self._employee.permission_set,
            order_id=self._order.id,
            business=self._order.restaurant,
            refund_amount=to_cents(self._order.refund_amount),
        )
        ORDER_LOGS.append(log)
        return log

    @classmethod
    def action(cls) -> str:
        return "refund"


class OrderCancelledLogger(OrderLogger):
    def log(self) -> EmployeeOrderLog:
        log = EmployeeOrderLog(
            action_type=self.action(),
            employee_id=self._employee.pk,
            employee_first_name=self._employee.first_name,
            employee_last_name=self._employee.last_name,
            employee_permission_set=self._employee.permission_set,
            order_id=self._order.id,
            business=self._order.restaurant,
            cancellation_total=self._order.total_cents,
        )
        ORDER_LOGS.append(log)
        return log

    @classmethod
    def action(cls) -> str:
        return "cancel"


def get_all_logs() -> list[EmployeeOrderLog]:
    return list(ORDER_LOGS)