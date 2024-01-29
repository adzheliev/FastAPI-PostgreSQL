"""Tests for Submenu CRUD requests"""

from http import HTTPStatus
from httpx import AsyncClient


class TestSubmenu:
    """Main class for Submenu tests"""
    menu_id = None
    submenu_id = None

    async def test_post_menu_for_submenus(self, ac: AsyncClient) -> None:
        """Testing menu post endpoint"""
        data = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response = await ac.post("/api/v1/menus/", json=data)

        """Testing status code"""
        assert response.status_code == HTTPStatus.CREATED
        TestSubmenu.menu_id = response.json()["id"]

    async def test_empty_submenu_list(self, ac: AsyncClient) -> None:
        """Testing submenus list endpoint with empty list"""
        response = await ac.get(f"/api/v1/menus/{TestSubmenu.menu_id}/submenus")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

    async def test_post_submenu(self, ac: AsyncClient) -> None:
        """Testing submenu post endpoint"""
        data = {
            "title": "My submenu 1",
            "description": "My submenu description 1"
        }
        response = await ac.post(f"/api/v1/menus/{TestSubmenu.menu_id}/submenus", json=data)

        """Testing status code"""
        assert response.status_code == HTTPStatus.CREATED
        TestSubmenu.submenu_id = response.json()["id"]

    async def test_not_empty_submenu_list(self, ac: AsyncClient) -> None:
        """Testing not empty submenus list endpoint"""
        response = await ac.get(f"/api/v1/menus/{TestSubmenu.menu_id}/submenus")

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

        """Testing number of menus created code"""
        assert len(response.json()) == 1

        """Testing all fields presence"""
        assert "title" in response.json()[0]
        assert "id" in response.json()[0]
        assert "description" in response.json()[0]
        assert "menu_id" in response.json()[0]
        assert "dishes_count" in response.json()[0]

        """Testing all fields values"""
        assert response.json()[0]["id"] == TestSubmenu.submenu_id
        assert response.json()[0]["title"] == "My submenu 1"
        assert response.json()[0]["description"] == "My submenu description 1"
        assert response.json()[0]["menu_id"] == TestSubmenu.menu_id
        assert response.json()[0]["dishes_count"] == 0

        """Testing all fields values types"""
        assert type(response.json()[0]["id"]) == str
        assert type(response.json()[0]["title"]) == str
        assert type(response.json()[0]["description"]) == str
        assert type(response.json()[0]["menu_id"]) == str

    async def test_post_submenu_wit_same_parameters(self, ac: AsyncClient) -> None:
        """Testing menu post endpoint with duplicate of menu"""
        data = {
            "title": "My submenu 1",
            "description": "My submenu description 1"
        }
        response = await ac.post(f"/api/v1/menus/{TestSubmenu.menu_id}/submenus", json=data)

        """Testing status code"""
        assert response.status_code == HTTPStatus.CONFLICT

    async def test_number_of_submenus_in_menus_list_after_duplicate_post(self, ac: AsyncClient) -> None:
        """Testing number of submenus in menu after duplicate post"""
        response = await ac.get(f"/api/v1/menus/{TestSubmenu.menu_id}/submenus")

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

        """Testing number of menus created"""
        assert len(response.json()) == 1

    async def test_patch_submenu(self, ac: AsyncClient) -> None:
        """Testing submenu patch endpoint"""
        data = {
            "title": "My updated submenu 1",
            "description": "My updated submenu description 1"
        }
        response = await ac.patch(f"/api/v1/menus/{TestSubmenu.menu_id}/submenus/{TestSubmenu.submenu_id}", json=data)

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

    async def test_specific_patched_submenu(self, ac: AsyncClient) -> None:
        """Testing patched submenu"""
        response = await ac.get(f"/api/v1/menus/{TestSubmenu.menu_id}/submenus/{TestSubmenu.submenu_id}")

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

    async def test_post_non_validated_data_in_submenu(self, ac: AsyncClient) -> None:
        """Testing submenu post endpoint with non validated data"""
        data = {
            "name": "My menu 1",
            "description": 1
        }
        response = await ac.post(f"/api/v1/menus/{TestSubmenu.menu_id}/submenus", json=data)

        """Testing status code"""
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_patch_not_existing_submenu(self, ac: AsyncClient) -> None:
        """Testing non existing submenu patch"""
        data = {
            "title": "My once again updated menu 1",
            "description": "My once again updated menu description 1"
        }
        response = await ac.patch(f"/api/v1/menus/{TestSubmenu.menu_id}/submenus/non_existing_submenu", json=data)

        """Testing status code"""
        assert response.status_code == HTTPStatus.NOT_FOUND

    async def test_delete_not_existing_submenu(self, ac: AsyncClient) -> None:
        """Testing non existing submenu delete"""

        response = await ac.delete(f"/api/v1/menus/{TestSubmenu.menu_id}/submenus/non_existing_submenu")

        """Testing status code"""
        assert response.status_code == HTTPStatus.NOT_FOUND

    async def test_delete_existing_submenu(self, ac: AsyncClient) -> None:
        """Testing existing submenu delete"""

        response = await ac.delete(f"/api/v1/menus/{TestSubmenu.menu_id}/submenus/{TestSubmenu.submenu_id}")

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

    async def test_delete_existing_menu(self, ac: AsyncClient) -> None:
        """Testing existing menu delete"""

        response = await ac.delete(f"/api/v1/menus/{TestSubmenu.menu_id}")

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK
