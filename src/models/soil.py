from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class IOTDevice(BaseModel):
    mac_address: str
    active: bool
    name: str
    description: str
    created_by: str
    created_at: datetime = datetime.now()
    updated_by: str
    updated_at: datetime = datetime.now()


class Plant(BaseModel):
    name: str
    location_id: int
    location: Location
    device_id: int
    device: IOTDevice
    description: str
    active: bool


class Location(BaseModel):
    name: str
    description: str
    active: bool


class SoilMeasurement(BaseModel):
    percent: int
    iot_device_id: int
    iot_device: IOTDevice
    plant_id: int
    plant: Plant
    location_id: int
    location: Location