import asyncio

from django.conf import settings
from onepassword.client import Client
from pydantic import SecretStr


# @lru_cache()
async def onepass_client() -> Client:
    return await Client.authenticate(auth=settings.ONEPASS_TOKEN.get_secret_value(), integration_name="soiled-py-integration", integration_version="v1.0.0")


class secret:
    @staticmethod
    def get(item: str, field: str, section: str = None, vault: str = None) -> SecretStr:
        return asyncio.run(secret.aget(item, field, section, vault))
    
    @staticmethod
    async def aget(item: str, field: str, section: str = None, vault: str = "project-secrets") -> SecretStr:
        client = await onepass_client()
        if section:
            uri = f"op://{vault}/{item}/{section}/{field}"
        else:
            uri = f"op://{vault}/{item}/{field}"
        return SecretStr(secret_value=await client.secrets.resolve(uri))
    

class value:
    @staticmethod
    def get(item: str, field: str, section: str = None, vault: str = None) -> str:
        return asyncio.run(secret.aget(item, field, section, vault))
    
    @staticmethod
    async def aget(item: str, field: str, section: str = None, vault: str = "project-secrets") -> str:
        if field == "password":
            raise ValueError("`password` field must be retrieved using `secret.get`")
        client = await onepass_client()
        if section:
            uri = f"op://{vault}/{item}/{section}/{field}"
        else:
            uri = f"op://{vault}/{item}/{field}"
        return await client.secrets.resolve(uri)
    