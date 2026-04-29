# app/services/payments.py
from __future__ import annotations

from dataclasses import dataclass

from app.interfaces.payments import (
    TapToPayInterface,
    RechargeInterface,
    QRPaymentInterface,
    TokenizedCardPaymentInterface,
)
from app.models import PAYMENT_EVENTS


class SubeTerminal(TapToPayInterface, RechargeInterface):
    """Physical SUBE terminal: tap + recharge only."""

    def tap_to_pay(self, card_id: str, amount: int) -> None:
        PAYMENT_EVENTS.append(f"SUBE tap: card={card_id}, amount={amount}")

    def recharge(self, card_id: str, amount: int) -> None:
        PAYMENT_EVENTS.append(f"SUBE recharge: card={card_id}, amount={amount}")


class ModoApp(QRPaymentInterface):
    """MODO app: QR payments only."""

    def pay_with_qr(self, qr_data: str, amount: int) -> None:
        PAYMENT_EVENTS.append(f"MODO QR: data={qr_data}, amount={amount}")


class MastercardGateway(TokenizedCardPaymentInterface):
    """Mastercard/Visa style gateway using tokenized cards."""

    def pay_with_token(self, token: str, amount: int) -> None:
        PAYMENT_EVENTS.append(f"MASTERCARD token: token={token}, amount={amount}")


@dataclass
class FakeQRGenerator:
    """Dummy QR generator for demo purposes."""

    prefix: str = "QR-SUBE"

    def generate_for(self, card_id: str, amount: int) -> str:
        return f"{self.prefix}:{card_id}:{amount}"


class ModoAsTapAdapter(TapToPayInterface):
    """
    Adapter that exposes tap_to_pay but internally uses QR via MODO.
    Demonstrates ISP + Adapter pattern.
    """

    def __init__(self, modo: QRPaymentInterface, qr_generator: FakeQRGenerator):
        self._modo = modo
        self._qr_generator = qr_generator

    def tap_to_pay(self, card_id: str, amount: int) -> None:
        qr_data = self._qr_generator.generate_for(card_id, amount)
        self._modo.pay_with_qr(qr_data, amount)


class BusTripService:
    """
    Service that depends only on TapToPayInterface.
    It doesn't know if backend is SUBE, MODO, Mastercard, etc.
    """

    def __init__(self, tap_backend: TapToPayInterface):
        self._tap_backend = tap_backend

    def pay_trip(self, sube_card_id: str, amount: int) -> None:
        self._tap_backend.tap_to_pay(sube_card_id, amount)


def get_sube_bus_trip_service() -> BusTripService:
    """Bus trips paid directly with physical SUBE card."""
    backend = SubeTerminal()
    return BusTripService(tap_backend=backend)


def get_modo_bus_trip_service() -> BusTripService:
    """
    Bus trips paid with MODO:
    we adapt MODO (QR) to TapToPayInterface via ModoAsTapAdapter.
    """
    modo = ModoApp()
    adapter = ModoAsTapAdapter(modo=modo, qr_generator=FakeQRGenerator())
    return BusTripService(tap_backend=adapter)
