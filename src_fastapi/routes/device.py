from fastapi import Response, status
from fastapi.routing import APIRouter

router = APIRouter()


@router.post("")
def create_device(): ...


@router.get("")
def get_devices(): ...


@router.get("/{id}")
def get_device(): ...


@router.patch("/{id}")
def update_device(): ...