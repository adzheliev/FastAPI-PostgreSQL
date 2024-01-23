"""Routes for Dish CRUD requests"""

from fastapi import APIRouter
from typing import Optional
from fastapi import Depends, HTTPException
from utils.database import get_db
from models.menu import Menu
from models.dish import Dish
from schemas.dish import DishCreate, DishUpdate
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter(tags=["Dishes API"])


@router.get(
    "/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes",
    status_code=200,
    description="The price will be rounded to 2 decimal places",
    summary="Gets a list of dishes in a specific menu and submenu"
)
async def get_dishes_list(
        target_menu_id: Optional[UUID | str] = None,
        target_submenu_id: Optional[UUID | str] = None,
        db: Session = Depends(get_db)):
    """Function gets a list of dishes in a specific menu and submenu"""

    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    if not existing_menu.submenus:
        return []

    existing_submenu = None
    for item in existing_menu.submenus:
        if str(item.id) == target_submenu_id:
            existing_submenu = item
            break

    if not existing_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    dishes = existing_submenu.dishes
    return dishes


@router.get(
    "/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}",
    status_code=200,
    description="The price will be rounded to 2 decimal places",
    summary="Gets a specific dish in a specific menu and submenu"
)
async def get_dish(
        target_menu_id: Optional[UUID | str] = None,
        target_submenu_id: Optional[UUID | str] = None,
        target_dish_id: Optional[UUID | str] = None,
        db: Session = Depends(get_db)):
    """Function gets a specific dish in a specific menu and submenu"""

    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    existing_submenu = None
    for submenu in existing_menu.submenus:
        if str(submenu.id) == target_submenu_id:
            existing_submenu = submenu
            break

    if not existing_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    existing_dish = None
    for dish in existing_submenu.dishes:
        if str(dish.id) == target_dish_id:
            existing_dish = dish
            break

    if not existing_dish:
        raise HTTPException(status_code=404, detail="dish not found")

    return existing_dish


@router.patch(
    "/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}",
    status_code=200,
    description="The price will be rounded to 2 decimal places",
    summary="Updates a specific dish in a specific menu and submenu"
)
async def update_dish(
        dish: DishUpdate,
        target_menu_id: Optional[UUID | str] = None,
        target_submenu_id: Optional[UUID | str] = None,
        target_dish_id: Optional[UUID | str] = None,
        db: Session = Depends(get_db)):
    """Function updates a specific dish in a specific menu and submenu"""

    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    existing_submenu = None
    for submenu in existing_menu.submenus:
        if str(submenu.id) == target_submenu_id:
            existing_submenu = submenu
            break

    if not existing_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    existing_dish = None
    for item in existing_submenu.dishes:
        if str(item.id) == target_dish_id:
            existing_dish = item
            break

    if not existing_dish:
        raise HTTPException(status_code=404, detail="dish not found")

    existing_dish.title = dish.title
    existing_dish.id = target_dish_id
    existing_dish.description = dish.description
    existing_dish.submenu_id = target_submenu_id
    existing_dish.price = "{:.2f}".format(float(dish.price))
    db.commit()
    db.refresh(existing_dish)
    return existing_dish


@router.post(
    "/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes",
    status_code=201,
    description="The price will be rounded to 2 decimal places",
    summary="Creates a new dish in a specific menu and submenu"
)
async def create_dish(
        dish: DishCreate,
        target_menu_id: Optional[UUID | str] = None,
        target_submenu_id: Optional[UUID | str] = None,
        db: Session = Depends(get_db)):
    """Function creates a new dish in a specific menu and submenu"""

    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    existing_submenu = None
    for submenu in existing_menu.submenus:
        if str(submenu.id) == target_submenu_id:
            existing_submenu = submenu
            break

    if not existing_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    dish = Dish(
        title=dish.title,
        price="{:.2f}".format(float(dish.price)),
        submenu_id=target_submenu_id,
        description=dish.description
    )

    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish


@router.delete(
    "/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}",
    summary="Deletes a specific dish from a specific menu and submenu"
)
async def delete_dish(
        target_menu_id: Optional[UUID | str] = None,
        target_submenu_id: Optional[UUID | str] = None,
        target_dish_id: Optional[UUID | str] = None,
        db: Session = Depends(get_db)):
    """Function deletes a specific dish from a specific menu and submenu"""

    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    existing_submenu = None
    for submenu in existing_menu.submenus:
        if str(submenu.id) == target_submenu_id:
            existing_submenu = submenu
            break

    if not existing_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    existing_dish = None
    for dish in existing_submenu.dishes:
        if str(dish.id) == target_dish_id:
            existing_dish = dish
            break

    if not existing_dish:
        raise HTTPException(status_code=404, detail="dish not found")

    db.delete(existing_dish)
    db.commit()
    return {"message": "Dish deleted"}
