# app/main.py
from __future__ import annotations

from fastapi import FastAPI

from app.api import api_router


def create_app() -> FastAPI:
    app = FastAPI(title="SOLID ISP Demo (FastAPI + SUBE/MODO/OrderLogger)")
    app.include_router(api_router)
    return app


app = create_app()