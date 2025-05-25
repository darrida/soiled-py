from django.http import HttpRequest
from ninja import ModelSchema, Router, Schema

from ..models import Sensor

router = Router()


class SensorSchema(ModelSchema):
    class Meta:
        model = Sensor
        fields = ["id", "name", "mac_address", "description", "active", "created_at", "updated_at"]


class SensorIn(Schema):
    name: str | None = None
    mac_address: str
    description: str | None = None
    active: bool = True


@router.get("/mac_address/{mac_address}", response={200: SensorSchema, 204: None})
def get_by_mac_address(request, mac_address: str):
    try:
        return Sensor.objects.get(mac_address=mac_address)
    except Sensor.DoesNotExist:
        return 204
    

@router.get("", response={200: list[SensorSchema], 204: None})
def get_all(request):
    return Sensor.objects.all()


@router.post("", response={200: SensorSchema})
def create(request: HttpRequest, payload: SensorIn):
    sensor = Sensor.objects.create(**payload.model_dump())
    sensor.updated_by = request.user.username
    sensor.save()
    return sensor
