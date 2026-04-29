# app/api/payments.py
from __future__ import annotations

from fastapi import APIRouter, Query

from app.models import PAYMENT_EVENTS
from app.schemas import PaymentRequest, PaymentResponse
from app.services.payments import (
    get_sube_bus_trip_service,
    get_modo_bus_trip_service,
)

router = APIRouter()


@router.post("/pay-sube", response_model=PaymentResponse)
def pay_with_sube(request: PaymentRequest):
    """
    Pay a bus trip with a physical SUBE card.
    Backend: SubeTerminal implementing TapToPayInterface + RechargeInterface.
    """
    service = get_sube_bus_trip_service()
    service.pay_trip(sube_card_id=request.sube_card_id, amount=request.amount)

    return PaymentResponse(
        status="ok",
        backend="SUBE",
        detail=f"Paid {request.amount} using SUBE card {request.sube_card_id}",
    )


@router.post("/pay-modo", response_model=PaymentResponse)
def pay_with_modo(request: PaymentRequest):
    """
    Pay a bus trip through MODO using an adapter that implements TapToPayInterface.
    """
    service = get_modo_bus_trip_service()
    service.pay_trip(sube_card_id=request.sube_card_id, amount=request.amount)

    return PaymentResponse(
        status="ok",
        backend="MODO via adapter",
        detail=f"Paid {request.amount} using MODO (adapted as tap) for card {request.sube_card_id}",
    )


@router.get("/events")
def list_payment_events(limit: int = Query(50, ge=1, le=500)):
    """Inspect the in-memory payment events log."""
    return PAYMENT_EVENTS[-limit:]