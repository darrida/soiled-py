# ruff: noqa: S101
import pytest

from _core.onepass import OnePasswordFieldNotFound, OnePasswordItemNotFound, secret


def test_get_onepass_secret_sync():
    password = secret.get(item="pytest-item", field="password")
    assert password.get_secret_value() == "pytest-pass"


@pytest.mark.asyncio
async def test_get_onepass_secret_async():
    password = await secret.aget(item="pytest-item", field="password")
    assert password.get_secret_value() == "pytest-pass"


@pytest.mark.asyncio
async def test_get_onepass_field_missing():
    with pytest.raises(OnePasswordFieldNotFound) as e:
        await secret.aget(item="pytest-item", field="not-found")
    assert str(e.value) == "Field `not-found` not found for op://project-secrets/pytest-item/not-found (op://<VAULT>/<ITEM>/<FIELD>)"


@pytest.mark.asyncio
async def test_get_onepass_item_missing():
    with pytest.raises(OnePasswordItemNotFound) as e:
        await secret.aget(item="not-found", field="password")
    assert str(e.value) == "Item `not-found` not found for op://project-secrets/not-found/password (op://<VAULT>/<ITEM>/<FIELD>)"

# async def test_get_onepass_vaule_missing(): ...

# async def test_get_onepass_section_missiong(): ...