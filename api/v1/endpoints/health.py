from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "ok"})
