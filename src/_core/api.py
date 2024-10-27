from ninja import NinjaAPI

from app_soiled.api import router as soiled_router

api = NinjaAPI()

api.add_router("/soiled/", soiled_router, tags=["Soiled"])

@api.get("/status")
def hello(request):
    return {"alive": True}