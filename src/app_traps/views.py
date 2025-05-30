from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from zoneinfo import ZoneInfo

from _shared.onepass import secret

from .logic.victor_mouse_trap import VictorApi, VictorAsyncClient
from .logic.victor_mouse_trap._models import Trap


@login_required # type: ignore
async def get_traps_status(request):
    username = await secret.aget(item="victor", field="username")
    password = await secret.aget(item="victor", field="password")

    async with VictorAsyncClient(username.get_secret_value(), password.get_secret_value()) as client:
        api = VictorApi(client)
        traps: list[Trap] = await api.get_traps()

    data_l = []
    for trap in traps:
        last_date = local_time(trap.trapstatistics.last_kill_date)
        text_color = "text-success" if trap.trapstatistics.kills_present == 0 else "text-error"
        status = "Clear" if trap.trapstatistics.kills_present == 0 else "Tripped"
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
