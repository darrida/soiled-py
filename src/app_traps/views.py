from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from loguru import logger
from prefect.blocks.system import Secret
from zoneinfo import ZoneInfo

from .logic.victor_mouse_trap import VictorApi, VictorAsyncClient
from .logic.victor_mouse_trap._models import Trap


@login_required
async def get_traps_status(request):
    username: Secret = await Secret.load("victor-username")
    password: Secret = await Secret.load("victor-password")

    async with VictorAsyncClient(username.get(), password.get()) as client:
        api = VictorApi(client)
        traps: list[Trap] = await api.get_traps()

    data_l = []
    # print(traps)
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


def local_time(datetime_: datetime, output_format: str = "%H:%M", tz: str = "America/Chicago") -> str:
    # datetime_ = datetime.strptime(timestamp, str_format)
    datetime_ = datetime_.astimezone(ZoneInfo(tz))
    return datetime_.strftime(output_format)
