from fastapi import Response, status
from fastapi.routing import APIRouter

router = APIRouter()


@router.get("/")
async def test_status():
    return Response("The server is running properly", status.HTTP_200_OK)