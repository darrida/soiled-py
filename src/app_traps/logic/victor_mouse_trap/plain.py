# from pydantic import BaseModel
# from datetime import datetime
# from typing import Any
# import requests


# class TrapStatistics(BaseModel):  # pylint: disable=too-many-instance-attributes
#     """Trap statistics data class."""

#     id: int  # pylint: disable=invalid-name
#     url: str
#     trap: str
#     trap_name: str
#     kills_present: int
#     install_date: datetime | None = None
#     owner_name: str
#     owner_email: str
#     last_report_date: datetime
#     last_kill_date: datetime | None = None
#     temperature: int | None = None
#     battery_level: int
#     total_kills: int | None = None
#     total_escapes: int | None = None
#     rx_power_level: int
#     firmware_version: str
#     trap_provisioned: bool
#     last_sequence_number: int | None = None
#     total_retreats: int | None = None
#     wireless_network_rssi: int
#     error_code: int
#     send_conn_lost_nt: bool
#     send_empty_trap_nt: bool
#     board_type: str
#     last_maintenance_date: str | datetime
#     bait_level: Any | None = None
#     current_bait: Any | None = None
#     last_bait_quantity: int | None = None

#     @property
#     def temperature_celcius(self) -> float | None:
#         """Get temperature in celcius."""
#         return round(self.temperature / 20, 1) if self.temperature else None


# class Trap(BaseModel):  # pylint: disable=too-many-instance-attributes
#     """Trap data class."""

#     id: int  # pylint: disable=invalid-name
#     url: str
#     corruption_status: int
#     corruption_status_options: list[tuple[int, str]] | None = None
#     operator: str | None = None
#     operator_name: str | None = None
#     name: str
#     ssid: str
#     serial_number: str
#     auto_upgrade: bool
#     status: int
#     location: str | None = None
#     lat: float | None = None
#     long: float | None = None
#     upgrade_firmware: str | None = None
#     commercial_gateway: str | None = None
#     commercial_monitor_mode_enabled: bool
#     lorawan_app_key: str
#     site_name: str | None = None
#     floor_plan_x: int | None = None
#     floor_plan_y: int | None = None
#     building_name: str | None = None
#     floor_name: str | None = None
#     room: str | None = None
#     room_name: str | None = None
#     trap_type: int
#     trap_type_verbose: str
#     alerts: int
#     trapstatistics: TrapStatistics

#     @property
#     def corruption_status_verbose(self) -> str | None:
#         """Get description of corruption_status code."""
#         if self.corruption_status_options:
#             return next(
#                 item[1]
#                 for item in self.corruption_status_options
#                 if item[0] == self.corruption_status
#             )
#         return None


# def _get_json_list(self, url: str) -> list[dict[str, Any]]:
#     response = request

#     response = self._client.get(url, timeout=5)
#     response.raise_for_status()
#     json = response.json()

#     if isinstance(json, list):
#         return json

#     result = json.get("results")
#     if result:
#         return result

#     raise Exception("Unexpected response content")


# def _get_list_by_schema(self, model: BaseModel, url: str) -> list[Any]:
#     data = _get_json_list(url)
#     data_l = [model(**x) for x in data]
#     return data_l


# def get_traps(self) -> list[Trap]:
#     """Get traps."""
#     return _get_list_by_schema(Trap, "traps/")