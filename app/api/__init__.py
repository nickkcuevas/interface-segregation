# app/api/__init__.py
from fastapi import APIRouter

from app.api import orders, payments

api_router = APIRouter()
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(payments.router, prefix="/bus-trip", tags=["bus-trip"])