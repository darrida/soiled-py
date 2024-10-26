from django.http import HttpRequest
from ninja import FilterSchema, ModelSchema, PatchDict, Router
from ninja.pagination import paginate

from ..models import Measurement
from .plant import PlantSchema

router = Router()

class MeasurementSchema(ModelSchema):
    # plant: PlantSchema
    class Meta:
        model = Measurement
        fields = ["id", "moisture_percent", "plant", "created_at"]

@router.get("", response={200: list[MeasurementSchema], 204: None})
def get():
    try:
        return Measurement.objects.all()
    except Measurement.DoesNotExist:
        return 204, None

@router.get("/id/{id}", response={200: MeasurementSchema, 204: None})
def get_by_id(request, id: int):
    try:
        return Measurement.objects.get(id=id)
    except Measurement.DoesNotExist:
        return 204, None
    
@router.get("/plant_id/{plant_id}", response={200: MeasurementSchema, 204: None})
def get_by_plant(request, plant_id: int):
    try:
        return Measurement.objects.get(plant__id=plant_id)
    except Measurement.DoesNotExist:
        return 204, None

@router.post("")
def create(request: HttpRequest, payload: MeasurementSchema):
    measurement = Measurement.objects.create(**payload.model_dump())
    measurement.updated_by = request.user.username
    measurement.save()
    return measurement

@router.patch("/{id}")
def update(request: HttpRequest, id: int, payload: PatchDict[MeasurementSchema]):
    obj = Measurement.objects.get(id=id)
    obj.updated_by = request.user.username
    for attr, value in payload.items():
        setattr(obj, attr, value)
    obj.save()