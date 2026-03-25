from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("")
def get_health():
    return {"is_healthy": True}
