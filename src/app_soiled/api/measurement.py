from datetime import datetime

from django.http import HttpRequest
from ninja import ModelSchema, Router, Schema

from ..models import Measurement, Plant, Sensor

router = Router()


class PlantOut(ModelSchema):
    class Meta:
        model = Plant
        fields = ["id", "name"]


class MeasurementOut(ModelSchema):
    plant: PlantOut

    class Meta:
        model = Measurement
        fields = ["id", "moisture_percent", "created_at"]

    
class MeasurementIn(Schema):
    mac_address: str
    moisture_percent: int
    created_at: datetime
    

@router.get("/latest/{mac_address}", response={200: MeasurementOut, 204: None})
def get_most_recent_by_mac_address(request, mac_address: str):
    try:
        plant = Plant.objects.get(sensor__mac_address=mac_address)
    except Sensor.DoesNotExist:
        return 204, None
    try:
        return Measurement.objects.filter(plant__pk=plant.pk).latest()
    except Measurement.DoesNotExist:
        return 204, None


@router.post("", response={200: MeasurementOut})
def create(request: HttpRequest, payload: MeasurementIn):
    try:
        sensor = Sensor.objects.get(mac_address=payload.mac_address)
    except Sensor.DoesNotExist:
        return 204, None
    plant = Plant.objects.get(sensor__pk=sensor.pk)
    measurement = Measurement.objects.create(
        moisture_percent=payload.moisture_percent,
        plant=plant,
        updated_by=request.user.username
    )
    return measurement
