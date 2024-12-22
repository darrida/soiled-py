from ninja import Router

from app_soiled.api import measurement, plant, sensor

router = Router()

router.add_router("sensor/", sensor.router, tags=["Sensor"])
router.add_router("measurement/", measurement.router, tags=["Measurement"])
router.add_router("plant/", plant.router, tags=["Plant"])
