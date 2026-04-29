# app/schemas.py
from __future__ import annotations

from pydantic import BaseModel, Field


class EmployeeIn(BaseModel):
    id: int = Field(alias="pk")
    first_name: str
    last_name: str
    permission_set: str

    class Config:
        populate_by_name = True


class OrderIn(BaseModel):
    id: int
    id2: str
    restaurant: str
    total_cents: int
    tips_cents: int
    surcharge_fee_cents: int
    discount_amount: str
    refund_amount: str


class EmployeeOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    permission_set: str


class OrderOut(BaseModel):
    id: int
    external_id: str
    business_name: str
    total_cents: int
    tips_cents: int
    surcharge_fee_cents: int


class LogResponse(BaseModel):
    action_type: str
    employee_id: int
    order_id: int
    business: str


class PaymentRequest(BaseModel):
    sube_card_id: str
    amount: int


class PaymentResponse(BaseModel):
    status: str
    backend: str
    detail: str
