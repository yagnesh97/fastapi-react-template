from fastapi import APIRouter
from fastapi.security import HTTPBearer

from .models import APIStatus

router = APIRouter()
security = HTTPBearer()


@router.get("/api-status", response_model=APIStatus)
async def get_api_status() -> APIStatus:
    """
    This is used to test the availability of the API.
    """
    return APIStatus(status="success")
