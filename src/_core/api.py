from ninja import NinjaAPI
from ninja.security import HttpBearer

from app_soiled.api import router as soiled_router


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token
        

api = NinjaAPI(auth=[AuthBearer()], csrf=False)

api.add_router("soiled/", soiled_router, tags=["Soiled"])


@api.get("/status")
def hello(request):
    return {"alive": True}
