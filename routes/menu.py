"""Routes for Menu CRUD requests"""

from fastapi import APIRouter
from typing import Optional
from fastapi import Depends, HTTPException
from utils.database import get_db
from models.menu import Menu
from schemas.menu import MenuCreate, MenuUpdate
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter()


@router.get(
    "/api/v1/menus",
    status_code=200,
    summary="Gets a list of menus"
)
async def get_menus_list(db: Session = Depends(get_db)):
    """Function gets a list of menus"""

    menus = db.query(Menu).all()
    if menus:
        return menus
    return []


@router.get(
    "/api/v1/menus/{target_menu_id}",
    status_code=200,
    summary="Get specific menu"
)
async def get_menu(
        target_menu_id: Optional[UUID | str] = None,
        db: Session = Depends(get_db)):
    """Function gets a specific menu"""

    if target_menu_id is not None:
        menu = db.query(Menu).filter_by(id=target_menu_id).first()
        if menu:
            menu.submenus_count = len(menu.submenus)
            if menu.submenus_count > 0:
                total = 0
                for item in menu.submenus:
                    submenu_dishes_count = len(item.dishes)
                    total += submenu_dishes_count
                menu.dishes_count = total
            return menu
        raise HTTPException(status_code=404, detail="menu not found")
    return None


@router.post(
    "/api/v1/menus",
    status_code=201,
    summary="Creates a new menu"
)
async def create_menu(
        menu: MenuCreate,
        db: Session = Depends(get_db)):
    """Function creates a new menu"""

    menu = Menu(
        title=menu.title,
        description=menu.description,
        submenus_count=0,
        dishes_count=0
    )
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


@router.patch(
    "/api/v1/menus/{target_menu_id}",
    summary="Updates a specific menu"
)
async def update_menu(
        menu: MenuUpdate,
        target_menu_id: Optional[UUID | str] = None,
        db: Session = Depends(get_db)):
    """Function updates a specific menu"""

    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    existing_menu.title = menu.title
    existing_menu.id = target_menu_id
    existing_menu.description = menu.description
    db.commit()
    db.refresh(existing_menu)
    return existing_menu


@router.delete(
    "/api/v1/menus/{target_menu_id}",
    summary="Deletes a specific menu"
)
async def delete_menu(
        target_menu_id: Optional[UUID | str] = None,
        db: Session = Depends(get_db)):
    """Function deletes a specific menu"""

    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    db.delete(existing_menu)
    db.commit()
    return {"message": "Menu deleted"}
