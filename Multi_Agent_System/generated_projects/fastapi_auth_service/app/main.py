import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.health import router as health_router
from app.core.settings import get_settings
from app.middleware.ratelimit_middleware import RateLimitMiddleware
from app.middleware.auth_middleware import AuthMiddleware
from app.db import engine
from app.models import Base

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="FastAPI Authentication Service",
        description="Authentication API with JWT, email verification, password reset, and role‑based access control.",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS configuration (allow all origins by default, can be restricted via env)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS.split(",") if settings.ALLOWED_HOSTS else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate limiting middleware
    app.add_middleware(RateLimitMiddleware)

    # Authentication middleware (adds `request.state.user` when a valid access token is present)
    app.add_middleware(AuthMiddleware)

    # Router registration
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(users_router, prefix="/users", tags=["users"])
    app.include_router(health_router, prefix="/health", tags=["health"])

    @app.on_event("startup")
    async def on_startup() -> None:
        """
        Create database tables on startup if they do not exist.
        In production migrations are handled by Alembic; this is a safety net for dev environments.
        """
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables ensured on startup.")

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        """
        Properly close the async engine on application shutdown.
        """
        await engine.dispose()
        logger.info("Database engine disposed on shutdown.")

    return app


app = create_app()