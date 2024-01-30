"""Tests for Submenu CRUD requests"""

from http import HTTPStatus

import pytest
from httpx import AsyncClient


class TestSubmenu:
    """Main class for Submenu tests"""

    """Fixtures for Submenu Tests"""

    @pytest.fixture(scope="function")
    async def create_menu_and_submenu_fixture(self, ac: AsyncClient):
        """Testing submenu create endpoint"""
        data_for_menu = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response_to_menu_creation = await ac.post(
            "/api/v1/menus/",
            json=data_for_menu
        )
        assert response_to_menu_creation.status_code == HTTPStatus.CREATED
        TestSubmenu.menu_id = response_to_menu_creation.json()["id"]

        data_for_submenu = {
            "title": "My submenu 1",
            "description": "My submenu description 1"
        }
        response_to_submenu_creation = await ac.post(
            f"/api/v1/menus/{TestSubmenu.menu_id}/submenus",
            json=data_for_submenu
        )

        assert response_to_submenu_creation.status_code == HTTPStatus.CREATED
        TestSubmenu.submenu_id = response_to_submenu_creation.json()["id"]
        yield

    @pytest.fixture(scope="function")
    async def delete_menu_and_submenu_fixture(self, ac: AsyncClient):
        """Testing submenu delete endpoint"""
        yield
        await ac.delete(
            f"/api/v1/menus/{TestSubmenu.menu_id}"
        )

    """Tests"""
    @pytest.mark.usefixtures('create_menu_and_submenu_fixture', 'delete_menu_and_submenu_fixture')
    async def test_get_submenus_list(
            self,
            ac: AsyncClient) -> None:
        """Testing submenus get list endpoint"""
        response = await ac.get(
            f"/api/v1/menus/{TestSubmenu.menu_id}/submenus"
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.usefixtures('create_menu_and_submenu_fixture', 'delete_menu_and_submenu_fixture')
    async def test_get_submenu(
            self,
            ac: AsyncClient) -> None:
        """Testing submenu get endpoint"""
        response = await ac.get(
            f"/api/v1/menus/{TestSubmenu.menu_id}/submenus/{TestSubmenu.submenu_id}",
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

        """Testing all fields presence"""
        assert "title" in response.json()
        assert "id" in response.json()
        assert "description" in response.json()
        assert "menu_id" in response.json()
        assert "dishes_count" in response.json()

        """Testing all fields values"""
        assert response.json()["id"] == TestSubmenu.submenu_id
        assert response.json()["title"] == "My submenu 1"
        assert response.json()["description"] == "My submenu description 1"
        assert response.json()["menu_id"] == TestSubmenu.menu_id
        assert response.json()["dishes_count"] == 0

        """Testing all fields values types"""
        assert type(response.json()["id"]) == str
        assert type(response.json()["title"]) == str
        assert type(response.json()["description"]) == str
        assert type(response.json()["menu_id"]) == str
        assert type(response.json()["dishes_count"]) == int

    @pytest.mark.usefixtures('create_menu_and_submenu_fixture', 'delete_menu_and_submenu_fixture')
    async def test_patch_submenu(
            self,
            ac: AsyncClient) -> None:
        """Testing submenu patch endpoint"""
        data = {
            "title": "My updated submenu 1",
            "description": "My updated submenu description 1"
        }
        response = await ac.patch(
            f"/api/v1/menus/{TestSubmenu.menu_id}/submenus/{TestSubmenu.submenu_id}",
            json=data
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

        """Testing all fields presence"""
        assert "title" in response.json()
        assert "id" in response.json()
        assert "description" in response.json()
        assert "menu_id" in response.json()
        assert "dishes_count" in response.json()

        """Testing all fields values"""
        assert response.json()["id"] == TestSubmenu.submenu_id
        assert response.json()["title"] == "My updated submenu 1"
        assert response.json()["description"] == "My updated submenu description 1"
        assert response.json()["menu_id"] == TestSubmenu.menu_id
        assert response.json()["dishes_count"] == 0

        """Testing all fields values types"""
        assert type(response.json()["id"]) == str
        assert type(response.json()["title"]) == str
        assert type(response.json()["description"]) == str
        assert type(response.json()["menu_id"]) == str
        assert type(response.json()["dishes_count"]) == int

    async def test_post_non_validated_data_in_submenu(
            self,
            ac: AsyncClient) -> None:
        """Testing submenu post endpoint with non validated data"""
        data = {
            "name": "My menu 1",
            "description": 1
        }
        response = await ac.post(
            f"/api/v1/menus/{TestSubmenu.menu_id}/submenus",
            json=data
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.usefixtures('create_menu_and_submenu_fixture', "delete_menu_and_submenu_fixture")
    async def test_delete_submenu(
            self,
            ac: AsyncClient) -> None:
        """Testing submenu delete endpoint"""

        response = await ac.delete(
            f"/api/v1/menus/{TestSubmenu.menu_id}/submenus/{TestSubmenu.submenu_id}"
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK


