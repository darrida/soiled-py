from django.urls import path

from .views import get_plant_status, temp

urlpatterns = [
    path("", temp, name="temp"),
    path("hx-plants-widgets", get_plant_status, name="hx_plants_widgets"),
]