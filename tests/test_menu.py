"""Tests for Menu CRUD requests"""

from http import HTTPStatus

import pytest
from httpx import AsyncClient


class TestMenu:
    """Main class for Menu tests"""

    """Fixtures for Menu Tests"""
    @pytest.fixture(scope="function")
    async def create_menu_fixture(self, ac: AsyncClient):
        data = {"title": "My menu 1", "description": "My menu description 1"}
        response = await ac.post("/api/v1/menus/", json=data)
        assert response.status_code == HTTPStatus.CREATED
        TestMenu.menu_id = response.json()["id"]
        yield

    @pytest.fixture(scope="function")
    async def delete_menu_fixture(self, ac: AsyncClient):
        yield
        await ac.delete(f"/api/v1/menus/{TestMenu.menu_id}")

    """Tests"""
    async def test_get_menus(
            self,
            ac: AsyncClient) -> None:
        """Testing menus list endpoint with empty list"""
        response = await ac.get(
            "/api/v1/menus/"
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

    @pytest.mark.usefixtures('create_menu_fixture', 'delete_menu_fixture')
    async def test_get_menu(
            self,
            ac: AsyncClient) -> None:
        """Testing menu create endpoint"""
        response = await ac.get(
            f"/api/v1/menus/{TestMenu.menu_id}",
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

        """Testing all fields presence"""
        assert "title" in response.json()
        assert "id" in response.json()
        assert "description" in response.json()
        assert "submenus_count" in response.json()
        assert "dishes_count" in response.json()

        """Testing all fields values"""
        assert response.json()["id"] == TestMenu.menu_id
        assert response.json()["title"] == "My menu 1"
        assert response.json()["description"] == "My menu description 1"
        assert response.json()["submenus_count"] == 0
        assert response.json()["dishes_count"] == 0

        """Testing all fields values types"""
        assert type(response.json()["id"]) == str
        assert type(response.json()["title"]) == str
        assert type(response.json()["description"]) == str
        assert type(response.json()["submenus_count"]) == int
        assert type(response.json()["dishes_count"]) == int

    @pytest.mark.usefixtures('create_menu_fixture', 'delete_menu_fixture')
    async def test_patch_menu(
            self,
            ac: AsyncClient) -> None:
        """Testing menu patch endpoint"""
        data = {
            "title": "My updated menu 1",
            "description": "My updated menu description 1"
        }
        response = await ac.patch(
            f"/api/v1/menus/{TestMenu.menu_id}",
            json=data
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

        """Testing all fields presence"""
        assert "title" in response.json()
        assert "id" in response.json()
        assert "description" in response.json()
        assert "submenus_count" in response.json()
        assert "dishes_count" in response.json()

        """Testing all fields values"""
        assert response.json()["title"] == "My updated menu 1"
        assert response.json()["description"] == "My updated menu description 1"
        assert response.json()["submenus_count"] == 0
        assert response.json()["dishes_count"] == 0

        """Testing all fields values types"""
        assert type(response.json()["title"]) == str
        assert type(response.json()["description"]) == str
        assert type(response.json()["submenus_count"]) == int
        assert type(response.json()["dishes_count"]) == int

    async def test_post_non_validated_data_in_menu(
            self,
            ac: AsyncClient) -> None:
        """Testing menu post endpoint with non validated data"""
        data = {
            "name": "My menu 1",
            "description": 1
        }
        response = await ac.post(
            "/api/v1/menus/",
            json=data
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.usefixtures('create_menu_fixture')
    async def test_delete_menu(
            self,
            ac: AsyncClient) -> None:
        """Testing menu delete"""

        response = await ac.delete(
            f"/api/v1/menus/{TestMenu.menu_id}"
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK
