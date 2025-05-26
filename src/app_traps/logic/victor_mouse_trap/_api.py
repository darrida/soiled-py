"""API module."""

from typing import Any

from pydantic import BaseModel

from ._client import VictorClient
from ._models import (
    Activity,
    MobileApp,
    Operator,
    Profile,
    Trap,
    User,
)


class VictorApi:
    """Access Victor remote API."""

    def __init__(self, victor_client: VictorClient, unknown: str = None) -> None:
        """Initialize VictorApi."""
        if not victor_client:
            raise ValueError("Victor client is required.")
        self._client = victor_client
        # self._unknown = RAISE if unknown is None else unknown

    def _get_json_list(self, url: str) -> list[dict[str, Any]]:
        response = self._client.get(url, timeout=5)
        response.raise_for_status()
        json = response.json()

        if isinstance(json, list):
            return json

        result = json.get("results")
        if result:
            return result

        raise Exception("Unexpected response content")

    def _get_list_by_schema(self, model: BaseModel, url: str) -> list[Any]:
        data = self._get_json_list(url)
        data_l = [model(**x) for x in data]
        return data_l

    def _get_json(self, url: str) -> dict[str, Any]:
        response = self._client.get(url)
        response.raise_for_status()
        return response.json()

    def _get_by_schema(self, model: BaseModel, url: str) -> Any:
        data = self._get_json(url)
        return model(**data)
        # return schema.load(self._get_json(url), unknown=self._unknown)

    def get_activity_logs(self) -> list[Activity]:
        """Get activity logs."""
        return self._get_list_by_schema(Activity, "activitylogs/")

    def get_activity_log_record(self, log_record_id: int) -> Activity:
        """Get activity log record by record id."""
        return self._get_by_schema(Activity, f"activitylogs/{log_record_id}/")

    def get_mobile_apps(self) -> list[MobileApp]:
        """Get mobile apps."""
        return self._get_list_by_schema(MobileApp, "mobileapps/")

    def get_mobile_app_by_id(self, app_id: int) -> MobileApp:
        """Get mobile app by app id."""
        return self.get_mobile_app_by_url(f"mobileapps/{app_id}/")

    def get_mobile_app_by_url(self, url: str) -> MobileApp:
        """Get mobile app by url."""
        return self._get_by_schema(MobileApp, url)

    def get_operators(self) -> list[Operator]:
        """Get operators."""
        return self._get_list_by_schema(Operator, "operators/")

    def get_operator_by_id(self, operator_id: int) -> Operator:
        """Get operator by operator id."""
        return self.get_operator_by_url(f"operators/{operator_id}/")

    def get_operator_by_url(self, url: str) -> Operator:
        """Get operator by url."""
        return self._get_by_schema(Operator, url)

    def get_profiles(self) -> list[Profile]:
        """Get profiles."""
        return self._get_list_by_schema(Profile, "profiles/")

    def get_profile_by_id(self, profile_id: int) -> Profile:
        """Get profile by profile id."""
        return self.get_profile_by_url(f"profiles/{profile_id}/")

    def get_profile_by_url(self, url: str) -> Profile:
        """Get profile by url."""
        return self._get_by_schema(Profile, url)

    def get_traps(self) -> list[Trap]:
        """Get traps."""
        return self._get_list_by_schema(Trap, "traps/")

    def get_trap_by_id(self, trap_id: int) -> Trap:
        """Get trap by trap id."""
        return self.get_trap_by_url(f"traps/{trap_id}/")

    def get_trap_by_url(self, url: str) -> Trap:
        """Get trap by url."""
        return self._get_by_schema(Trap, url)

    def get_trap_history(self, trap_id: int) -> list[Activity]:
        """Get trap history by trap id."""
        return self._get_list_by_schema(Activity, f"traps/{trap_id}/history/")

    def get_users(self) -> list[User]:
        """Get users."""
        return self._get_list_by_schema(User, "users/")

    def get_user_by_id(self, user_id: int) -> User:
        """Get user by user id."""
        return self.get_user_by_url(f"users/{user_id}/")

    def get_user_by_url(self, url: str) -> User:
        """Get user by user id."""
        return self._get_by_schema(User(), url)
