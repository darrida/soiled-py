from datetime import datetime
from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from zoneinfo import ZoneInfo
from datetime import timedelta
from django.utils import timezone

from _shared.onepass import secret

from .logic.victor_mouse_trap import VictorApi, VictorClient
from .logic.victor_mouse_trap._models import Trap


@login_required # type: ignore
def get_traps_status(request):
    username = secret.get(item="victor", field="username")
    password = secret.get(item="victor", field="password")

    with VictorClient(username.get_secret_value(), password.get_secret_value()) as client:
        api = VictorApi(client)
        traps: list[Trap] = api.get_traps()

    data_l = []
    for trap in traps:
        last_date = local_time(trap.trapstatistics.last_report_date, output_format="%Y-%m-%d %I:%M%p")
        status = "Clear" if trap.trapstatistics.kills_present == 0 else "Tripped"
        text_color = "text-success" if status == "Clear" else "text-error"

        if trap.trapstatistics.last_report_date < timezone.now() - timedelta(days=7) and status == "Clear":
            status = "Unknown"
            text_color = "text-warning"
        
        data = {
            "name": trap.name,
            "status": status,
            "last_update": last_date,
            "text_color": text_color,
        }
        data_l.append(data)
    print(data_l)

    return render(request, "app_traps/hx_traps_widgets.html", context={"traps": data_l})


def local_time(datetime_: datetime | None, output_format: str = "%H:%M", tz: str = "America/Chicago") -> str | None:
    if not datetime_:
        return None
    datetime_ = datetime_.astimezone(ZoneInfo(tz))
    return datetime_.strftime(output_format)
