from fastapi import APIRouter
from fastapi.security import HTTPBearer

from .models import Status

router = APIRouter()
security = HTTPBearer()


@router.get("/api-status", response_model=Status)
async def get_api_status() -> Status:
    """
    This is used to test the availability of the API.
    """
    return Status(status="success")
