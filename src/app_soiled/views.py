# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Measurement, Plant


@login_required
def temp(request):
    return render(request, "app_soiled/temp.html")


@login_required
def get_plant_status(request):
    plants = Plant.objects.filter(active=True)
    data_l = []
    for plant in plants:
        measurement = Measurement.objects.filter(plant__pk=plant.pk).latest()
        print(measurement.moisture_percent)
        data = {
            "name": f"{plant.name} ({plant.location.name})",
            "moisture_percent": measurement.moisture_percent,
            "last_update": measurement.created_at,
        }
        data_l.append(data)

    return render(request, "app_soiled/hx_plants.html", context={"plants": data_l})