import json
from pathlib import Path

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.deps import get_current_user
from app.models import User

router = APIRouter(prefix="/links", tags=["links"])

LINKS_PATH = Path(__file__).resolve().parent.parent / "data" / "links.json"


class LinkOut(BaseModel):
    category: str
    title: str
    url: str
    note: str | None = None


@router.get("")
def list_links(_user: User = Depends(get_current_user)) -> list[LinkOut]:
    data = json.loads(LINKS_PATH.read_text(encoding="utf-8"))
    return [LinkOut(**item) for item in data]
