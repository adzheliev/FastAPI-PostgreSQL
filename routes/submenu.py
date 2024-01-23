"""Routes for Submenu CRUD requests"""

from fastapi import APIRouter
from typing import Optional
from fastapi import Depends, HTTPException
from utils.database import get_db
from models.menu import Menu
from models.submenu import Submenu
from schemas.submenu import SubmenuCreate, SubmenuUpdate
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter(prefix='/api/v1/menus', tags=["Submenus API"])


@router.get(
    "/{target_menu_id}/submenus",
    status_code=200,
    summary="Gets a list of submenus in a specific menu"
)
async def get_submenus_list(
        target_menu_id: Optional[UUID | str] = None,
        db: Session = Depends(get_db)):
    """Function gets a list of submenus in a specific menu"""

    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    submenus = existing_menu.submenus
    return submenus


@router.get(
    "/{target_menu_id}/submenus/{target_submenu_id}",
    status_code=200,
    summary="Gets a specific submenu in a specific menu"
)
async def get_submenu(
        target_menu_id: Optional[UUID | str] = None,
        target_submenu_id: Optional[UUID | str] = None,
        db: Session = Depends(get_db)):
    """Function gets a specific submenu in a specific menu"""

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
    existing_submenu.dishes_count = len(existing_submenu.dishes)

    return existing_submenu


@router.post(
    "/{target_menu_id}/submenus",
    status_code=201,
    summary="Creates a new submenu in a specific menu"
)
async def create_submenu(
        submenu: SubmenuCreate,
        target_menu_id: Optional[UUID | str] = None,
        db: Session = Depends(get_db)):
    """Function creates submenu in a specific menu"""

    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    submenu = Submenu(
        title=submenu.title,
        description=submenu.description,
        menu_id=target_menu_id
    )
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    return submenu


@router.patch(
    "/{target_menu_id}/submenus/{target_submenu_id}",
    summary="Updates a specific submenu in a specific menu"
)
async def update_submenu(
        submenu: SubmenuUpdate,
        target_menu_id: Optional[UUID | str] = None,
        target_submenu_id: Optional[UUID | str] = None,
        db: Session = Depends(get_db)):
    """Function updates a specific submenu in a specific menu"""

    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    existing_submenu = None
    for item in existing_menu.submenus:
        if str(item.id) == target_submenu_id:
            existing_submenu = item
            break

    if not existing_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    existing_submenu.title = submenu.title
    existing_submenu.description = submenu.description
    db.commit()
    db.refresh(existing_submenu)
    return existing_submenu


@router.delete(
    "/{target_menu_id}/submenus/{target_submenu_id}",
    summary="Deletes a specific submenu in a specific menu"
)
async def delete_submenu(
        target_menu_id: Optional[UUID | str] = None,
        target_submenu_id: Optional[UUID | str] = None,
        db: Session = Depends(get_db)):
    """Function deletes a specific submenu in a specific menu"""

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

    db.delete(existing_submenu)
    db.commit()
    return {"message": "Submenu deleted"}
