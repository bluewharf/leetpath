from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import db as dbmod
from app.db import Base, configure_db
from app.deps import get_current_user
from app.routers import admin, auth, drafts, jobs, links, problems, submissions


@asynccontextmanager
async def lifespan(_app: FastAPI):
    configure_db()
    from app import models as _models  # noqa: F401

    assert dbmod.engine is not None
    Base.metadata.create_all(bind=dbmod.engine)
    yield
    if dbmod.engine is not None:
        dbmod.engine.dispose()
        dbmod.engine = None
        dbmod.SessionLocal = None


app = FastAPI(title="leetpath", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
_protected = [Depends(get_current_user)]
app.include_router(problems.router, prefix="/api", dependencies=_protected)
app.include_router(submissions.router, prefix="/api", dependencies=_protected)
app.include_router(drafts.router, prefix="/api", dependencies=_protected)
app.include_router(jobs.router, prefix="/api", dependencies=_protected)
app.include_router(links.router, prefix="/api", dependencies=_protected)
app.include_router(admin.router, prefix="/api", dependencies=_protected)
