# app/models.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Employee:
    pk: int
    first_name: str
    last_name: str
    permission_set: str


@dataclass
class Order:
    id: int
    id2: str
    restaurant: str
    total_cents: int
    tips_cents: int
    surcharge_fee_cents: int
    discount_amount: str
    refund_amount: str


@dataclass
class EmployeeOrderLog:
    action_type: str
    employee_id: int
    employee_first_name: str
    employee_last_name: str
    employee_permission_set: str
    order_id: int
    business: str
    order_total: Optional[int] = None
    tips_received: Optional[int] = None
    surcharge_received: Optional[int] = None
    discount_applied: Optional[int] = None
    refund_amount: Optional[int] = None
    cancellation_total: Optional[int] = None


# In-memory "database" just to make the example playable
ORDER_LOGS: List[EmployeeOrderLog] = []
PAYMENT_EVENTS: List[str] = []
