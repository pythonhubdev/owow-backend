from contextlib import asynccontextmanager

from fastapi import FastAPI

from owow_backend.core import OpenTelemetry
from owow_backend.db import MongoConnection
from owow_backend.web.api.user.controller import UserController


@asynccontextmanager  # type: ignore
async def lifespan(app: FastAPI) -> None:  # type: ignore
    app.middleware_stack = None
    OpenTelemetry.setup_opentelemetry(app)
    await MongoConnection().connect()
    await UserController.create_default_user()
    app.middleware_stack = app.build_middleware_stack()
    yield
    OpenTelemetry.stop_opentelemetry(app)
