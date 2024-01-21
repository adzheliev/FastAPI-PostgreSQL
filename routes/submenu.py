from fastapi import APIRouter
from typing import Optional
from fastapi import Depends, HTTPException
from utils.database import get_db
from models.menu import Menu
from models.submenu import Submenu
from schemas.submenu import SubmenuCreate, SubmenuUpdate
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter()


@router.get("/api/v1/menus/{target_menu_id}/submenus")
async def get_submenus_list(target_menu_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    submenus = existing_menu.submenus
    return submenus


@router.post("/api/v1/menus/{target_menu_id}/submenus", status_code=201)
async def create_submenu(submenu: SubmenuCreate, target_menu_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    submenu = Submenu(title=submenu.title, description=submenu.description, menu_id=target_menu_id)
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    return submenu


@router.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
async def get_submenu(target_menu_id: Optional[UUID | str] = None, target_submenu_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
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

    return existing_submenu


@router.patch("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
async def update_submenu(submenu: SubmenuUpdate, target_menu_id: Optional[UUID | str] = None, target_submenu_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    existing_menu = db.query(Menu).filter_by(id=target_menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="menu not found")

    existing_submenu = None
    for item in existing_menu.submenus:
        if item.id == target_submenu_id:
            existing_submenu = item
            break

    if not existing_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    existing_submenu.title = submenu.title
    existing_submenu.description = submenu.description
    db.commit()
    db.refresh(existing_submenu)
    return existing_submenu


@router.delete("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
async def delete_submenu(target_menu_id: Optional[UUID | str] = None, target_submenu_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
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

    db.delete(existing_submenu)
    db.commit()
    return {"message": "Submenu deleted"}