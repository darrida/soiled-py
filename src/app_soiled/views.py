# Create your views here.
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from zoneinfo import ZoneInfo

from .models import Measurement, Plant


@login_required
def temp(request):
    return render(request, "app_soiled/temp.html")


@login_required
def get_statuses(request):
    plants = Plant.objects.filter(active=True)
    data_l = []
    for plant in plants:
        measurement = Measurement.objects.filter(plant__pk=plant.pk).latest()
        text_color = "text-error" if int(measurement.moisture_percent) < 80 else "text-success"
        data = {
            "name": f"{plant.name} ({plant.location.name})",
            "moisture_percent": measurement.moisture_percent,
            "last_update": measurement.created_at,
            "text_color": text_color
        }
        data_l.append(data)

    return render(request, "app_soiled/hx_plants.html", context={"plants": data_l})


@login_required
def get_status_table(request):
    plants = Plant.objects.filter(active=True)
    data_l = []
    for plant in plants:
        data = {}
        if measurements := list(Measurement.objects.filter(plant__pk=plant.pk).order_by("-created_at")[:2]):
            if len(measurements) < 2:
                arrow_direction = "right"
                arrow_color = "text-info"
                text_color = "text-info"
            else:
                if measurements[0].moisture_percent >= measurements[1].moisture_percent:
                    arrow_direction = "up-right"
                    arrow_color = "text-success"
                else:
                    arrow_direction = "down-right"
                    arrow_color = "text-error"
                text_color = "text-error" if int(measurements[0].moisture_percent) < 80 else "text-success"
            data = {
                "name": f"{plant.name} ({plant.location.name})",
                "moisture_percent": f"{measurements[0].moisture_percent}%",
                "last_update": local_time(measurements[0].created_at),
                "text_color": text_color,
                "arrow_direction": arrow_direction,
                "arrow_color": arrow_color
            }
        else:
            data["name"] = f"{plant.name} (not enough data)"
        data_l.append(data)

    return render(request, "app_soiled/hx_plants_table.html", context={"plants": data_l})


def local_time(datetime_: datetime, output_format: str = "%I:%M %p", tz: str = "America/Chicago") -> str:
    # datetime_ = datetime.strptime(timestamp, str_format)
    datetime_ = datetime_.astimezone(ZoneInfo(tz))
    return datetime_.strftime(output_format)