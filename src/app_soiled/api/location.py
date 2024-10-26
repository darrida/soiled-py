from ninja import ModelSchema, Router
from ninja.pagination import paginate

from ..models import Location

router = Router()

class LocationSchema(ModelSchema):
    class Meta:
        model = Location
        fields = ["id", "name", "description", "active", "created_at", "updated_at", "updated_by"]


@router.get("", response={200: list[LocationSchema], 204: None})
@paginate
def get_all(request):
    try:
        return Location.objects.all()
    except Location.DoesNotExist:
        return 204, None


@router.get("/name/{name}", response={200: LocationSchema, 204: None})
def get_by_name(request, name: str):
    try:
        return Location.objects.get(name=name)
    except Location.DoesNotExist:
        return 204, None


@router.get("/id/{id}", response={200: LocationSchema, 204: None})
def get_by_id(request, id: int):
    try:
        return Location.objects.get(id=id)
    except Location.DoesNotExist:
        return 204


# @router.post("")
# def create():
#     pass

# @router.put("")
# def update():
#     pass
