from ninja import NinjaAPI

from app_soiled.api import router as soiled_router

api = NinjaAPI()

api.add_router("/soiled/", soiled_router, tags=["Soiled"])

@api.get("/hello")
def hello(request):
    return "Hello world"