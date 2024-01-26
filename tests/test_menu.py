from http import HTTPStatus
from httpx import AsyncClient


async def test_empty_menu_list(ac: AsyncClient) -> None:
    """Testing empty menu list"""
    response = await ac.get("/api/v1/menus/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


