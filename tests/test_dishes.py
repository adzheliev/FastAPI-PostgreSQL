"""Tests for Dishes CRUD requests"""

from http import HTTPStatus
from httpx import AsyncClient


class TestDishes:
    """Main class for Dishes tests"""
    menu_id = None
    submenu_id = None
    dish_id =None

    async def test_post_menu_for_submenus_and_dishes(self, ac: AsyncClient) -> None:
        """Testing menu post endpoint"""
        data = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response = await ac.post("/api/v1/menus/", json=data)

        """Testing status code"""
        assert response.status_code == HTTPStatus.CREATED
        TestDishes.menu_id = response.json()["id"]

    async def test_post_submenu_for_dishes(self, ac: AsyncClient) -> None:
        """Testing submenu post endpoint"""
        data = {
            "title": "My submenu 1",
            "description": "My submenu description 1"
        }
        response = await ac.post(f"/api/v1/menus/{TestDishes.menu_id}/submenus", json=data)

        """Testing status code"""
        assert response.status_code == HTTPStatus.CREATED
        TestDishes.submenu_id = response.json()["id"]

    async def test_empty_dishes_list(self, ac: AsyncClient) -> None:
        """Testing dishes list endpoint with empty list"""
        response = await ac.get(f"/api/v1/menus/{TestDishes.menu_id}/submenus/{TestDishes.submenu_id}/dishes")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

    async def test_post_dish(self, ac: AsyncClient) -> None:
        """Testing dish post endpoint"""
        data = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": "13.40"
        }
        response = await ac.post(f"/api/v1/menus/{TestDishes.menu_id}/submenus/{TestDishes.submenu_id}/dishes", json=data)

        """Testing status code"""
        assert response.status_code == HTTPStatus.CREATED
        TestDishes.dish_id = response.json()["id"]

    async def test_not_empty_submenu_list(self, ac: AsyncClient) -> None:
        """Testing not empty dishes list endpoint"""
        response = await ac.get(f"/api/v1/menus/{TestDishes.menu_id}/submenus/{TestDishes.submenu_id}/dishes")

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

        """Testing number of menus created code"""
        assert len(response.json()) == 1

        """Testing all fields presence"""
        assert "title" in response.json()[0]
        assert "id" in response.json()[0]
        assert "description" in response.json()[0]
        assert "submenu_id" in response.json()[0]
        assert "price" in response.json()[0]

        """Testing all fields values"""
        assert response.json()[0]["id"] == TestDishes.dish_id
        assert response.json()[0]["title"] == "My dish 1"
        assert response.json()[0]["description"] == "My dish description 1"
        assert response.json()[0]["submenu_id"] == TestDishes.submenu_id
        assert response.json()[0]["price"] == "13.40"

        """Testing all fields values types"""
        assert type(response.json()[0]["id"]) == str
        assert type(response.json()[0]["title"]) == str
        assert type(response.json()[0]["description"]) == str
        assert type(response.json()[0]["submenu_id"]) == str
        assert type(response.json()[0]["price"]) == str

    async def test_post_dish_wit_same_parameters(self, ac: AsyncClient) -> None:
        """Testing menu post endpoint with duplicate of menu"""
        data = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": "13.40"
        }
        response = await ac.post(f"/api/v1/menus/{TestDishes.menu_id}/submenus/{TestDishes.submenu_id}/dishes", json=data)

        """Testing status code"""
        assert response.status_code == HTTPStatus.CONFLICT

