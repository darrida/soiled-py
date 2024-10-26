from fastapi import APIRouter, FastAPI
from routes import device, location, plant, soil, status, user

v1_app = FastAPI()

# status
v1_app.include_router(status.router)
# users
v1_app.include_router(user.router, prefix="/user", tags=["Users"])
# app
v1_app.include_router(device.router, prefix="/device", tags=["Devices"])
v1_app.include_router(location.router, prefix="/location", tags=["Locations"])
v1_app.include_router(plant.router, prefix="/plant", tags=["Plants"])
v1_app.include_router(soil.router, prefix="/soil", tags=["Soil"])
