from fastapi import APIRouter
from typing import Optional
from fastapi import Depends, HTTPException
from utils.database import get_db
from models.menu import Menu
from models.dish import Dish
from schemas.dish import DishCreate, DishUpdate
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter()


@router.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes")
async def get_dishes_list(target_menu_id: Optional[UUID | str] = None, target_submenu_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    if not existing_menu.submenus:
        return []

    existing_submenu = None
    for item in existing_menu.submenus:
        if item.id == target_submenu_id:
            existing_submenu = item
            break

    if not existing_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    dishes = existing_submenu.dishes
    return dishes


@router.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
async def get_dish(target_menu_id: Optional[UUID | str] = None, target_submenu_id: Optional[UUID | str] = None, target_dish_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    existing_submenu = None
    for submenu in existing_menu.submenus:
        if submenu.id == target_submenu_id:
            existing_submenu = submenu
            break

    if not existing_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    existing_dish = None
    for dish in existing_submenu.dishes:
        if dish.id == target_dish_id:
            existing_dish = dish
            break

    if not existing_dish:
        raise HTTPException(status_code=404, detail="dish not found")

    return existing_dish


@router.patch("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
async def update_dish(dish: DishUpdate, target_menu_id: Optional[UUID | str] = None, target_submenu_id: Optional[UUID | str] = None, target_dish_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    existing_submenu = None
    for submenu in existing_menu.submenus:
        if submenu.id == target_submenu_id:
            existing_submenu = submenu
            break

    if not existing_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    existing_dish = None
    for item in existing_submenu.dishes:
        if item.id == target_dish_id:
            existing_dish = item
            break

    if not existing_dish:
        raise HTTPException(status_code=404, detail="dish not found")

    existing_dish.title = dish.title
    existing_dish.id = target_dish_id
    existing_dish.description = dish.description
    existing_dish.submenu_id = target_submenu_id
    existing_dish.price = dish.price
    db.commit()
    db.refresh(existing_dish)
    return existing_dish


@router.post("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes", status_code=201)
async def create_dish(dish: DishCreate, target_menu_id: Optional[UUID | str] = None, target_submenu_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    existing_submenu = None
    for submenu in existing_menu.submenus:
        if submenu.id == target_submenu_id:
            existing_submenu = submenu
            break

    if not existing_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")




    dish = Dish(title=dish.title, price=dish.price, submenu_id=target_submenu_id, description=dish.description)
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish


@router.delete("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
async def delete_dish(target_menu_id: Optional[UUID | str] = None, target_submenu_id: Optional[UUID | str] = None, target_dish_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    existing_submenu = None
    for submenu in existing_menu.submenus:
        if submenu.id == target_submenu_id:
            existing_submenu = submenu
            break

    if not existing_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    existing_dish = None
    for dish in existing_submenu.dishes:
        if dish.id == target_dish_id:
            existing_dish = dish
            break

    if not existing_dish:
        raise HTTPException(status_code=404, detail="dish not found")

    db.delete(existing_dish)
    db.commit()
    return {"message": "Dish deleted"}