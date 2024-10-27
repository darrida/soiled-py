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
