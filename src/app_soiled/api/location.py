from datetime import datetime

from ninja import Router, Schema
from ninja.pagination import paginate

from ..models import Location

router = Router()

class LocationOut(Schema):
    pk: int
    name: str
    description: str | None = None
    active: bool
    created_at: datetime
    updated_at: datetime
    updated_by: str | None = None


@router.get("", response={200: list[LocationOut], 204: None})
@paginate
def get_all(request):
    try:
        return Location.objects.all()
    except Location.DoesNotExist:
        return 204, None


@router.get("/name/{name}", response={200: LocationOut, 204: None})
def get_by_name(request, name: str):
    try:
        location = Location.objects.get(name=name)
        return location
    except Location.DoesNotExist:
        return 204, None


@router.get("/pk/{pk}", response={200: LocationOut, 204: None})
def get_by_pk(request, pk: int):
    try:
        location = Location.objects.get(pk=pk)
        return location
    except Location.DoesNotExist:
        return 204


# @router.post("")
# def create():
#     pass

# @router.put("")
# def update():
#     pass
