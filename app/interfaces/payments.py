# app/interfaces/payments.py
from __future__ import annotations

from abc import ABC, abstractmethod


class TapToPayInterface(ABC):
    @abstractmethod
    def tap_to_pay(self, card_id: str, amount: int) -> None:
        raise NotImplementedError


class RechargeInterface(ABC):
    @abstractmethod
    def recharge(self, card_id: str, amount: int) -> None:
        raise NotImplementedError


class QRPaymentInterface(ABC):
    @abstractmethod
    def pay_with_qr(self, qr_data: str, amount: int) -> None:
        raise NotImplementedError


class TokenizedCardPaymentInterface(ABC):
    @abstractmethod
    def pay_with_token(self, token: str, amount: int) -> None:
        raise NotImplementedError
