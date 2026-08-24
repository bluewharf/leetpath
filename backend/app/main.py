from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import db as dbmod
from app.db import Base, configure_db
from app.deps import get_current_user
from app.config import get_settings
from app.rate_limit import request_limiter
from app.routers import admin, auth, drafts, invites, jobs, links, problems, submissions


@asynccontextmanager
async def lifespan(_app: FastAPI):
    get_settings()
    request_limiter.clear()
    configure_db()
    from app import models as _models  # noqa: F401

    assert dbmod.engine is not None
    Base.metadata.create_all(bind=dbmod.engine)
    yield
    if dbmod.engine is not None:
        dbmod.engine.dispose()
        dbmod.engine = None
        dbmod.SessionLocal = None


_settings = get_settings()
app = FastAPI(
    title="leetpath",
    lifespan=lifespan,
    docs_url=None if _settings.APP_ENV == "production" else "/docs",
    redoc_url=None if _settings.APP_ENV == "production" else "/redoc",
    openapi_url=None if _settings.APP_ENV == "production" else "/openapi.json",
)
if _settings.APP_ENV != "production":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[_settings.PUBLIC_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def validate_origin(request: Request, call_next):
    settings = get_settings()
    if settings.APP_ENV == "production" and request.method not in {"GET", "HEAD", "OPTIONS"}:
        if request.headers.get("origin", "").rstrip("/") != settings.PUBLIC_ORIGIN.rstrip("/"):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "请求来源不受信任"},
            )
    return await call_next(request)

app.include_router(auth.router, prefix="/api")
_protected = [Depends(get_current_user)]
app.include_router(problems.router, prefix="/api", dependencies=_protected)
app.include_router(submissions.router, prefix="/api", dependencies=_protected)
app.include_router(drafts.router, prefix="/api", dependencies=_protected)
app.include_router(jobs.router, prefix="/api", dependencies=_protected)
app.include_router(links.router, prefix="/api", dependencies=_protected)
app.include_router(admin.router, prefix="/api", dependencies=_protected)
app.include_router(invites.router, prefix="/api", dependencies=_protected)
