from fastapi import Response, status
from fastapi.routing import APIRouter

router = APIRouter()


@router.post("")
def create_plant(): ...


@router.get("")
def get_plants(): ...


@router.get("/{id}")
def get_plant(): ...


@router.patch("/{id}")
def update_planet(): ...