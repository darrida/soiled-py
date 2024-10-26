from fastapi import Response, status
from fastapi.routing import APIRouter

router = APIRouter()


@router.post("")
def create_location(): ...


@router.get("")
def get_locations(): ...


@router.get("/{id}")
def get_location(): ...


@router.patch("/{id}")
def update_location(): ...