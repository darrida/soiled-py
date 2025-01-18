from django.contrib.admin.views.decorators import staff_member_required
from ninja import NinjaAPI, Swagger
from ninja.security import HttpBearer

from app_soiled.api import router as soiled_router


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token
        

api = NinjaAPI(csrf=False, docs=Swagger()) #, docs_decorator=staff_member_required) # auth=[AuthBearer()], 

api.add_router("soiled/", soiled_router, tags=["Soiled"])


@api.get("/status")
def hello(request):
    return {"alive": True}
