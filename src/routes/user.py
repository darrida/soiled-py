from fastapi import Response, status
from fastapi.routing import APIRouter

router = APIRouter()


@router.post("")
def create_user(): ...


@router.get("")
def get_users(): ...


@router.get("/{id}")
def get_user(): ...


@router.patch("/{id}")
def update_user(): ...