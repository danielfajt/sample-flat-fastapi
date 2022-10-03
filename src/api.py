import typing as t

from fastapi import APIRouter, Query, Response
from fastapi.responses import StreamingResponse

api_router = APIRouter()


@api_router.get("/")
async def api_index():
    """API index"""

    return {"Hello from": "API index"}
