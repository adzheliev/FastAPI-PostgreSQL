from http import HTTPStatus
from httpx import AsyncClient


async def test_empty_menu_list(ac: AsyncClient) -> None:
    """Testing menus list endpoint with empty list"""
    response = await ac.get("/api/v1/menus/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


async def test_post_menu(ac: AsyncClient) -> None:
    """Testing menu post endpoint"""
    data = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
    response = await ac.post("/api/v1/menus/", json=data)

    """Testing status code"""
    assert response.status_code == HTTPStatus.CREATED


async def test_not_empty_menu_list(ac: AsyncClient) -> None:
    """Testing not empty menus list endpoint"""
    response = await ac.get("/api/v1/menus/")

    """Testing status code"""
    assert response.status_code == HTTPStatus.OK

    """Testing number of menus created code"""
    assert len(response.json()) == 1

    """Testing all fields presence"""
    assert "title" in response.json()[0]
    assert "id" in response.json()[0]
    assert "description" in response.json()[0]
    assert "submenus_count" in response.json()[0]
    assert "dishes_count" in response.json()[0]

    """Testing all fields values"""
    assert response.json()[0]["title"] == "My menu 1"
    assert response.json()[0]["description"] == "My menu description 1"
    assert response.json()[0]["submenus_count"] == 0
    assert response.json()[0]["dishes_count"] == 0

    """Testing all fields values types"""
    assert type(response.json()[0]["title"]) == str
    assert type(response.json()[0]["description"]) == str
    assert type(response.json()[0]["submenus_count"]) == int
    assert type(response.json()[0]["dishes_count"]) == int


async def test_post_menu_wit_same_parameters(ac: AsyncClient) -> None:
    """Testing menu post endpoint"""
    data = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
    response = await ac.post("/api/v1/menus/", json=data)

    """Testing status code"""
    assert response.status_code == HTTPStatus.CONFLICT




