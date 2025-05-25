import asyncio

from onepassword.lib.aarch64.op_uniffi_core import Error as OnePasswordError
from django.conf import settings
from onepassword.client import Client
from pydantic import SecretStr


# @lru_cache()
async def onepass_client() -> Client:
    return await Client.authenticate(auth=settings.ONEPASSWORD_TOKEN.get_secret_value(), integration_name="soiled-py-integration", integration_version="v1.0.0")


class OnePasswordFieldNotFound(Exception):
    pass


class OnePasswordItemNotFound(Exception):
    pass


class secret:
    @staticmethod
    def get(item: str, field: str, section: str | None = None, vault: str = "project-secrets") -> SecretStr:
        return asyncio.run(secret.aget(item, field, section, vault))
    
    @staticmethod
    async def aget(item: str, field: str, section: str | None = None, vault: str = "project-secrets") -> SecretStr:
        client = await onepass_client()
        if section:
            uri = f"op://{vault}/{item}/{section}/{field}"
        else:
            uri = f"op://{vault}/{item}/{field}"
        try:
            return SecretStr(secret_value=await client.secrets.resolve(uri))
        except OnePasswordError.Error as e:
            if "specified field cannot be found within the item" in str(e):
                raise OnePasswordFieldNotFound(f"Field `{field}` not found for {uri} (op://<VAULT>/<ITEM>/<FIELD>)")
            elif "no item matched the secret reference query" in str(e):
                raise OnePasswordItemNotFound(f"Item `{item}` not found for {uri} (op://<VAULT>/<ITEM>/<FIELD>)")
            else:
                raise OnePasswordError.Error(e) from e

    