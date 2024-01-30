"""Test of the special scenario of number of dishes and submenus in menu"""

from http import HTTPStatus
from httpx import AsyncClient


class TestScenario:
    """Main class for Tests scenario"""

    async def test_dish_and_submenu_quantity(self, ac: AsyncClient):
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
        TestScenario.menu_id = response_to_menu_creation.json()["id"]

        data_for_submenu = {
            "title": "My submenu 1",
            "description": "My submenu description 1"
        }
        response_to_submenu_creation = await ac.post(
            f"/api/v1/menus/{TestScenario.menu_id}/submenus",
            json=data_for_submenu
        )

        assert response_to_submenu_creation.status_code == HTTPStatus.CREATED
        TestScenario.submenu_id = response_to_submenu_creation.json()["id"]

        data_for_dish = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": "20.55"
        }
        response_to_dish_creation = await ac.post(
            f"/api/v1/menus/{TestScenario.menu_id}/submenus/{TestScenario.submenu_id}/dishes",
            json=data_for_dish
        )

        assert response_to_dish_creation.status_code == HTTPStatus.CREATED

        data_for_second_dish = {
            "title": "My dish 2",
            "description": "My dish description 2",
            "price": "33.33"
        }
        response_to_second_dish_creation = await ac.post(
            f"/api/v1/menus/{TestScenario.menu_id}/submenus/{TestScenario.submenu_id}/dishes",
            json=data_for_second_dish
        )

        assert response_to_second_dish_creation.status_code == HTTPStatus.CREATED

        data_for_second_submenu = {
            "title": "My submenu 2",
            "description": "My submenu description 2"
        }
        response_for_second_submenu_creation = await ac.post(
            f"/api/v1/menus/{TestScenario.menu_id}/submenus",
            json=data_for_second_submenu
        )

        assert response_for_second_submenu_creation.status_code == HTTPStatus.CREATED

        data_for_third_submenu = {
            "title": "My submenu 3",
            "description": "My submenu description 3"
        }
        response_for_third_submenu_creation = await ac.post(
            f"/api/v1/menus/{TestScenario.menu_id}/submenus",
            json=data_for_third_submenu
        )

        assert response_for_third_submenu_creation.status_code == HTTPStatus.CREATED

        """Testing number of submenus and dishes_in specific menu"""
        response_to_dish_and_submenu_quantity_check = await ac.get(
            f"/api/v1/menus/{TestScenario.menu_id}"
        )

        """Testing status code"""
        assert response_to_dish_and_submenu_quantity_check.status_code == HTTPStatus.OK

        """Testing number of submenus and dishes fields"""
        assert "submenus_count" in response_to_dish_and_submenu_quantity_check.json()
        assert "dishes_count" in response_to_dish_and_submenu_quantity_check.json()

        """Testing number of submenus and dishes"""
        assert response_to_dish_and_submenu_quantity_check.json()['submenus_count'] == 3
        assert response_to_dish_and_submenu_quantity_check.json()['dishes_count'] == 2

        await ac.delete(
            f"/api/v1/menus/{TestScenario.menu_id}"
        )

