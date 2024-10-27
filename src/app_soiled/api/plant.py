from ninja import ModelSchema, Router

from ..models import Plant

router = Router()

class PlantSchema(ModelSchema):
    class Meta:
        model = Plant
        fields = ["id", "name", "description", "active", "created_at", "updated_at", "updated_by"]


@router.get("/id/{id}", response={200: PlantSchema, 204: None})
def get_by_id(request, id: int):
    try:
        return Plant.objects.get(id=id)
    except Plant.DoesNotExist:
        return 204


# @router.get("", response={200: list[PlantSchema], 204: None})
# @paginate
# def get(request):
#     try:
#         return Plant.objects.all()
#     except Plant.DoesNotExist:
#         return 204, None

# @router.get("/name/{name}", response={200: PlantSchema, 204: None})
# def get_by_name(request, name: str):
#     try:
#         return Plant.objects.get(name=name)
#     except Plant.DoesNotExist:
#         return 204, None

# @router.post("")
# def create():
#     pass

# @router.put("")
# def update():
#     pass
