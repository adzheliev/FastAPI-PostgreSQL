"""Test of the special scenario of number of dishes and submenus in menu"""

from http import HTTPStatus
from httpx import AsyncClient


class ScenarioDishes:
    """Main class for Dishes tests"""
    menu_id = None
    submenu_id = None
    dish_id = None
    second_dish_id = None

    async def test_post_menu_for_submenus_and_dishes_scenario(
            self,
            ac: AsyncClient) -> None:
        """Testing menu post endpoint"""
        data = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response = await ac.post(
            "/api/v1/menus/",
            json=data
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.CREATED
        ScenarioDishes.menu_id = response.json()["id"]

    async def test_post_submenu_for_dishes_scenario(
            self,
            ac: AsyncClient) -> None:
        """Testing submenu post endpoint"""
        data = {
            "title": "My submenu 1",
            "description": "My submenu description 1"
        }
        response = await ac.post(
            f"/api/v1/menus/{ScenarioDishes.menu_id}/submenus",
            json=data
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.CREATED
        ScenarioDishes.submenu_id = response.json()["id"]

    async def test_empty_dishes_list_scenario(
            self,
            ac: AsyncClient) -> None:
        """Testing dishes list endpoint with empty list"""
        response = await ac.get(
            f"/api/v1/menus/{ScenarioDishes.menu_id}/submenus/{ScenarioDishes.submenu_id}/dishes"
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

    async def test_post_dish(
            self,
            ac: AsyncClient) -> None:
        """Testing dish post endpoint"""
        data = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": "13.40"
        }
        response = await ac.post(
            f"/api/v1/menus/{ScenarioDishes.menu_id}/submenus/{ScenarioDishes.submenu_id}/dishes",
            json=data
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.CREATED
        ScenarioDishes.dish_id = response.json()["id"]

    async def test_post_second_dish_scenario(
            self,
            ac: AsyncClient) -> None:
        """Testing dish post endpoint"""
        data = {
            "title": "My dish 2",
            "description": "My dish description 2",
            "price": "66.60"
        }
        response = await ac.post(
            f"/api/v1/menus/{ScenarioDishes.menu_id}/submenus/{ScenarioDishes.submenu_id}/dishes",
            json=data
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.CREATED
        ScenarioDishes.second_dish_id = response.json()["id"]

    async def test_not_empty_submenu_list_scenario(
            self,
            ac: AsyncClient) -> None:
        """Testing not empty dishes list endpoint"""
        response = await ac.get(
            f"/api/v1/menus/{ScenarioDishes.menu_id}/submenus/{ScenarioDishes.submenu_id}/dishes"
        )

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
        assert response.json()[0]["id"] == ScenarioDishes.dish_id
        assert response.json()[0]["title"] == "My dish 1"
        assert response.json()[0]["description"] == "My dish description 1"
        assert response.json()[0]["submenu_id"] == ScenarioDishes.submenu_id
        assert response.json()[0]["price"] == "13.40"

        """Testing all fields values types"""
        assert type(response.json()[0]["id"]) == str
        assert type(response.json()[0]["title"]) == str
        assert type(response.json()[0]["description"]) == str
        assert type(response.json()[0]["submenu_id"]) == str
        assert type(response.json()[0]["price"]) == str

    async def test_post_dish_wit_same_parameters_scenario(
            self,
            ac: AsyncClient) -> None:
        """Testing dish post endpoint with duplicate of menu"""
        data = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": "13.40"
        }
        response = await ac.post(
            f"/api/v1/menus/{ScenarioDishes.menu_id}/submenus/{ScenarioDishes.submenu_id}/dishes",
            json=data
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.CONFLICT

    async def test_number_of_dishes_in_dishes_list_after_duplicate_post_scenario(
            self,
            ac: AsyncClient) -> None:
        """Testing number of dishes in dishes list after duplicate post"""
        response = await ac.get(
            f"/api/v1/menus/{ScenarioDishes.menu_id}/submenus/{ScenarioDishes.submenu_id}/dishes"
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

        """Testing number of menus created"""
        assert len(response.json()) == 1

    async def test_patch_dishes(
            self,
            ac: AsyncClient) -> None:
        """Testing dishes patch endpoint"""
        data = {
            "title": "My updated dish 1",
            "description": "My updated dish description 1",
            "price": "10.22"
        }
        response = await ac.patch(
            f"/api/v1/menus/{ScenarioDishes.menu_id}/submenus/{ScenarioDishes.submenu_id}/dishes/{ScenarioDishes.dish_id}",
            json=data
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

    async def test_specific_patched_dish_scenario(
            self,
            ac: AsyncClient) -> None:
        """Testing patched dish"""
        response = await ac.get(
            f"/api/v1/menus/{ScenarioDishes.menu_id}/submenus/{ScenarioDishes.submenu_id}/dishes/{ScenarioDishes.dish_id}")

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

        """Testing all fields presence"""
        assert "title" in response.json()
        assert "id" in response.json()
        assert "description" in response.json()
        assert "submenu_id" in response.json()
        assert "price" in response.json()

        """Testing all fields values"""
        assert response.json()["id"] == ScenarioDishes.dish_id
        assert response.json()["title"] == "My updated dish 1"
        assert response.json()["description"] == "My updated dish description 1"
        assert response.json()["submenu_id"] == ScenarioDishes.submenu_id
        assert response.json()["price"] == "10.22"

        """Testing all fields values types"""
        assert type(response.json()["id"]) == str
        assert type(response.json()["title"]) == str
        assert type(response.json()["description"]) == str
        assert type(response.json()["submenu_id"]) == str
        assert type(response.json()["price"]) == str

    async def test_number_of_submenus_and_dishes_in_specific_menu_scenario(
            self,
            ac: AsyncClient) -> None:
        """Testing number of submenus and dishes_in specific menu"""
        response = await ac.get(
            f"/api/v1/menus/{ScenarioDishes.menu_id}"
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

        """Testing number of submenus and dishes"""
        assert response.json()['submenus_count'] == 1
        assert response.json()['dishes_count'] == 2

    async def test_post_non_validated_data_in_dish_scenario(
            self,
            ac: AsyncClient) -> None:
        """Testing dish post endpoint with non validated data"""
        data = {
            "name": "My menu 1",
            "description": 1
        }
        response = await ac.post(
            f"/api/v1/menus/{ScenarioDishes.menu_id}/submenus/{ScenarioDishes.submenu_id}/dishes",
            json=data
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_patch_not_existing_dish_scenario(
            self,
            ac: AsyncClient) -> None:
        """Testing non existing dish patch"""
        data = {
            "title": "My once again updated menu 1",
            "description": "My once again updated menu description 1",
            "price": "9.45"
        }
        response = await ac.patch(
            f"/api/v1/menus/{ScenarioDishes.menu_id}/submenus/{ScenarioDishes.submenu_id}/dishes/not_existing_dish",
            json=data
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.NOT_FOUND

    async def test_delete_not_existing_dish_scenario(
            self,
            ac: AsyncClient) -> None:
        """Testing non existing dish delete"""

        response = await ac.delete(
            f"/api/v1/menus/{ScenarioDishes.menu_id}/submenus/{ScenarioDishes.submenu_id}/dishes/not_existing_dish"
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.NOT_FOUND

    async def test_delete_existing_dish_scenario(self, ac: AsyncClient) -> None:
        """Testing existing dish delete"""

        response = await ac.delete(
            f"/api/v1/menus/{ScenarioDishes.menu_id}/submenus/{ScenarioDishes.submenu_id}/dishes/{ScenarioDishes.dish_id}"
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

    async def test_delete_existing_second_dish_scenario(self, ac: AsyncClient) -> None:
        """Testing existing dish delete"""

        response = await ac.delete(
            f"/api/v1/menus/{ScenarioDishes.menu_id}/submenus/{ScenarioDishes.submenu_id}/dishes/{ScenarioDishes.second_dish_id}"
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

    async def test_delete_existing_submenu_scenario(
            self,
            ac: AsyncClient) -> None:
        """Testing existing submenu delete"""

        response = await ac.delete(
            f"/api/v1/menus/{ScenarioDishes.menu_id}/submenus/{ScenarioDishes.submenu_id}"
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK

    async def test_delete_existing_menu_scenario(
            self,
            ac: AsyncClient) -> None:
        """Testing existing menu delete"""

        response = await ac.delete(
            f"/api/v1/menus/{ScenarioDishes.menu_id}"
        )

        """Testing status code"""
        assert response.status_code == HTTPStatus.OK