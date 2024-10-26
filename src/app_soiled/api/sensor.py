from datetime import datetime

from django.http import HttpRequest
from ninja import ModelSchema, PatchDict, Router, Schema
from ninja.pagination import paginate

from ..models import Sensor

router = Router()

class SensorSchema(ModelSchema):
    class Meta:
        model = Sensor
        fields = ["id", "name", "mac_address", "description", "active", "created_at", "updated_at"]


@router.get("", response={200: list[SensorSchema], 204: None})
@paginate
def get():
    try:
        return Sensor.objects.all()
    except Sensor.DoesNotExist:
        return 204, None

@router.get("/name/{name}", response={200: SensorSchema, 204: None})
def get_by_name(request, name: str):
    try:
        return Sensor.objects.get(name=name)
    except Sensor.DoesNotExist:
        return 204, None


@router.get("/id/{id}", response={200: SensorSchema, 204: None})
def get_by_id(request, id: int):
    try:
        return Sensor.objects.get(id=id)
    except Sensor.DoesNotExist:
        return 204

@router.post("", response={200: SensorSchema})
def create(request: HttpRequest, payload: SensorSchema):
    sensor = Sensor.objects.create(**payload.model_dump())
    sensor.updated_by = request.user.username
    sensor.save()
    return sensor

@router.patch("/{id}")
def update(request: HttpRequest, id: int, payload: PatchDict[SensorSchema]):
    obj = Sensor.objects.get(id=id)
    obj.updated_by = request.user.username
    for attr, value in payload.items():
        setattr(obj, attr, value)
    obj.save()