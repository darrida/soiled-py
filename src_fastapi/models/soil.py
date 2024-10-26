from __future__ import annotations

import shelve
from datetime import datetime
from hashlib import sha256
from os import stat_result
from typing import Any

from pydantic import BaseModel, Field


class storage:
    @staticmethod
    def get_all(db_name: str) -> dict:
        with shelve.open(db_name) as db:
            return db
        
    @staticmethod
    def get_one(db_name: str, key: str | int) -> Any:
        with shelve.open(db_name) as db:
            return db[key]
        
    @staticmethod
    def update(db_name: str, key: str | int, obj: Any):
        with shelve.open(db_name) as db:
            db[key] = obj



class IOTDevice(BaseModel):
    mac_address: str
    active: bool
    name: str
    description: str
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_by: str
    updated_at: datetime = Field(default_factory=datetime.now)

    def create(self):
        storage.update("users.db", self.name, self)
        
    def update(self):
        user: IOTDevice = storage.get_one("users.db", self.name)
        user.updated_at = datetime.now()
        user.updated_by = "admin"
        storage.update(("users.db", self.name, user))
    
    @staticmethod
    def get(mac_address: str) -> "IOTDevice":
        with shelve("device.db") as db:
            user: IOTDevice = db[mac_address]
        return user
    
    @staticmethod
    def get_all() -> list["IOTDevice"]:
        with shelve("device.db") as db:
            return db    


class Plant(BaseModel):
    name: str
    location_id: int
    location: Location
    device_id: int
    device: IOTDevice
    description: str
    active: bool
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_by: str
    updated_at: datetime = Field(default_factory=datetime.now)

    def create(self):
        with shelve("plants.db") as db:
            self.created_by = "admin"
            self.updated_by = "admin"
            db[self.name] = self

    def update(self):
        with shelve("plants.db") as db:
            user: IOTDevice = db[self.name]
            user.updated_at = datetime.now()
            user.updated_by = "admin"
            db[self.name] = user
    
    @staticmethod
    def get(mac_address: str) -> "IOTDevice":
        with shelve("plants.db") as db:
            user: IOTDevice = db[mac_address]
        return user
    
    @staticmethod
    def get_all() -> list["IOTDevice"]:
        with shelve("plants.db") as db:
            return db    


class Location(BaseModel):
    name: str
    description: str
    active: bool
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_by: str
    updated_at: datetime = Field(default_factory=datetime.now)

    def create(self):
        with shelve("locations.db") as db:
            self.created_by = "admin"
            self.updated_by = "admin"
            db[self.name] = self

    def update(self):
        with shelve("locations.db") as db:
            user: IOTDevice = db[self.name]
            user.updated_at = datetime.now()
            user.updated_by = "admin"
            db[self.name] = user
    
    @staticmethod
    def get(mac_address: str) -> "IOTDevice":
        with shelve("locations.db") as db:
            user: IOTDevice = db[mac_address]
        return user
    
    @staticmethod
    def get_all() -> list["IOTDevice"]:
        with shelve("locations.db") as db:
            return db  


class SoilMeasurement(BaseModel):
    id_: int = None
    percent: int
    iot_device_id: int
    iot_device: IOTDevice
    plant_id: int
    plant: Plant
    location_id: int
    location: Location
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_by: str
    updated_at: datetime = Field(default_factory=datetime.now)

    def create(self):
        with shelve("measurements.db") as db:
            self.created_by = "admin"
            self.updated_by = "admin"
            db[self.name] = self

    def update(self):
        with shelve("measuremnts.db") as db:
            user: IOTDevice = db[self.id_]
            user.updated_at = datetime.now()
            user.updated_by = "admin"
            db[self.id_] = user
    
    @staticmethod
    def get(id_: int) -> "IOTDevice":
        with shelve("measurements.db") as db:
            user: IOTDevice = db[id_]
        return user
    
    @staticmethod
    def get_all() -> list["IOTDevice"]:
        with shelve("measurements.db") as db:
            return db  