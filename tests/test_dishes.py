"""Tests for Dishes CRUD requests"""

from http import HTTPStatus

import pytest
from httpx import AsyncClient


class TestDishes:
    """Main class for Dishes tests"""

    """Fixtures for Dishes Tests"""

    @pytest.fixture(scope="function")
    async def create_menu_submenu_and_dish_fixture(self, ac: AsyncClient):
        """Testing dish create endpoint"""
        data_for_menu = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response_to_menu_creation = await ac.post(
            "/api/v1/menus/",
            json=data_for_menu
        )
        assert response_to_menu_creation.status_code == HTTPStatus.CREATED
        TestDishes.menu_id = response_to_menu_creation.json()["id"]

        data_for_submenu = {
            "title": "My submenu 1",
            "description": "My submenu description 1"
        }
        response_to_submenu_creation = await ac.post(
            f"/api/v1/menus/{TestDishes.menu_id}/submenus",
            json=data_for_submenu
        )

        assert response_to_submenu_creation.status_code == HTTPStatus.CREATED
        TestDishes.submenu_id = response_to_submenu_creation.json()["id"]

        data_for_dish = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": "20.55"
        }
        response_to_dish_creation = await ac.post(
            f"/api/v1/menus/{TestDishes.menu_id}/submenus/{TestDishes.submenu_id}/dishes",
            json=data_for_dish
        )

        assert response_to_dish_creation.status_code == HTTPStatus.CREATED
        TestDishes.dish_id = response_to_dish_creation.json()["id"]
        yield

    @pytest.fixture(scope="function")
    async def delete_menu_submenu_and_dish_fixture(self, ac: AsyncClient):
        """Testing dish delete endpoint"""
        yield
        await ac.delete(
            f"/api/v1/menus/{TestDishes.menu_id}"
        )

    """Tests"""

    @pytest.mark.usefixtures('create_menu_submenu_and_dish_fixture', 'delete_menu_submenu_and_dish_fixture')
    async def test_get_dish_list(
            self,
            ac: AsyncClient) -> None:
        """Testing dish list get endpoint"""
        response = await ac.get(
            f"/api/v1/menus/{TestDishes.menu_id}/submenus/{TestDishes.submenu_id}/dishes"
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.usefixtures('create_menu_submenu_and_dish_fixture', 'delete_menu_submenu_and_dish_fixture')
    async def test_get_dish(
            self,
            ac: AsyncClient) -> None:
        """Testing dish get endpoint"""
        response = await ac.get(
            f"/api/v1/menus/{TestDishes.menu_id}/submenus/{TestDishes.submenu_id}/dishes/{TestDishes.dish_id}",
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

        """Testing all fields presence"""
        assert "title" in response.json()
        assert "id" in response.json()
        assert "description" in response.json()
        assert "submenu_id" in response.json()
        assert "price" in response.json()

        """Testing all fields values"""
        assert response.json()["id"] == TestDishes.dish_id
        assert response.json()["title"] == "My dish 1"
        assert response.json()["description"] == "My dish description 1"
        assert response.json()["submenu_id"] == TestDishes.submenu_id
        assert response.json()["price"] == "20.55"

        """Testing all fields values types"""
        assert type(response.json()["id"]) == str
        assert type(response.json()["title"]) == str
        assert type(response.json()["description"]) == str
        assert type(response.json()["submenu_id"]) == str
        assert type(response.json()["price"]) == str

    @pytest.mark.usefixtures('create_menu_submenu_and_dish_fixture', 'delete_menu_submenu_and_dish_fixture')
    async def test_patch_dish(
            self,
            ac: AsyncClient) -> None:
        """Testing dish patch endpoint"""
        data = {
            "title": "My updated dish 1",
            "description": "My updated dish description 1",
            "price": "10.22"
        }
        response = await ac.patch(
            f"/api/v1/menus/{TestDishes.menu_id}/submenus/{TestDishes.submenu_id}/dishes/{TestDishes.dish_id}",
            json=data
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

        """Testing all fields presence"""
        assert "title" in response.json()
        assert "id" in response.json()
        assert "description" in response.json()
        assert "submenu_id" in response.json()
        assert "price" in response.json()

        """Testing all fields values"""
        assert response.json()["id"] == TestDishes.dish_id
        assert response.json()["title"] == "My updated dish 1"
        assert response.json()["description"] == "My updated dish description 1"
        assert response.json()["submenu_id"] == TestDishes.submenu_id
        assert response.json()["price"] == "10.22"

        """Testing all fields values types"""
        assert type(response.json()["id"]) == str
        assert type(response.json()["title"]) == str
        assert type(response.json()["description"]) == str
        assert type(response.json()["submenu_id"]) == str
        assert type(response.json()["price"]) == str

    async def test_post_non_validated_data_in_dish(
            self,
            ac: AsyncClient) -> None:
        """Testing dish post endpoint with non validated data"""
        data = {
            "name": "My menu 1",
            "description": 1,
            "price": 22.44

        }
        response = await ac.post(
            f"/api/v1/menus/{TestDishes.menu_id}/submenus/{TestDishes.submenu_id}/dishes",
            json=data
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.usefixtures('create_menu_submenu_and_dish_fixture', "delete_menu_submenu_and_dish_fixture")
    async def test_delete_dish(self, ac: AsyncClient) -> None:
        """Testing dish delete endpoint"""

        response = await ac.delete(
            f"/api/v1/menus/{TestDishes.menu_id}/submenus/{TestDishes.submenu_id}/dishes/{TestDishes.dish_id}"
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

