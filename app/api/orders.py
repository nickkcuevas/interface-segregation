# app/api/orders.py
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Path

from app.models import Employee, Order
from app.schemas import EmployeeIn, OrderIn, LogResponse
from app.interfaces.logging import OrderLogger
from app.services import order_logging

router = APIRouter()


@router.post("/log/{action}", response_model=LogResponse)
def log_order_action(
    action: str = Path(..., description="Action type", examples=["create", "refund", "cancel"]),
    employee_in: EmployeeIn = ...,
    order_in: OrderIn = ...,
):
    """Endpoint to exercise the ISP-friendly OrderLogger hierarchy."""
    if action not in {"create", "refund", "cancel"}:
        raise HTTPException(status_code=400, detail="Unsupported action")

    employee = Employee(
        pk=employee_in.id,
        first_name=employee_in.first_name,
        last_name=employee_in.last_name,
        permission_set=employee_in.permission_set,
    )

    order = Order(
        id=order_in.id,
        id2=order_in.id2,
        restaurant=order_in.restaurant,
        total_cents=order_in.total_cents,
        tips_cents=order_in.tips_cents,
        surcharge_fee_cents=order_in.surcharge_fee_cents,
        discount_amount=order_in.discount_amount,
        refund_amount=order_in.refund_amount,
    )

    logger = OrderLogger.new_for(action=action, employee=employee, order=order)
    log = logger.log()

    return LogResponse(
        action_type=log.action_type,
        employee_id=log.employee_id,
        order_id=log.order_id,
        business=log.business,
    )


@router.get("/logs", response_model=list[LogResponse])
def list_logs():
    """Return all in-memory logs (for demo purposes)."""
    logs = order_logging.get_all_logs()
    return [
        LogResponse(
            action_type=log.action_type,
            employee_id=log.employee_id,
            order_id=log.order_id,
            business=log.business,
        )
        for log in logs
    ]