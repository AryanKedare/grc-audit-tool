from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models.framework import Framework, Control
from app.schemas.framework import FrameworkSchema, FrameworkListSchema, ControlSchema

router = APIRouter()


@router.get("/", response_model=List[FrameworkListSchema])
def list_frameworks(db: Session = Depends(get_db)):
    return db.query(Framework).all()


@router.get("/{framework_id}", response_model=FrameworkSchema)
def get_framework(framework_id: int, db: Session = Depends(get_db)):
    fw = (
        db.query(Framework)
        .options(joinedload(Framework.domains))
        .filter(Framework.id == framework_id)
        .first()
    )
    if not fw:
        raise HTTPException(status_code=404, detail="Framework not found")
    return fw


@router.get("/{framework_id}/controls", response_model=List[ControlSchema])
def get_framework_controls(framework_id: int, db: Session = Depends(get_db)):
    fw = db.query(Framework).filter(Framework.id == framework_id).first()
    if not fw:
        raise HTTPException(status_code=404, detail="Framework not found")
    controls = []
    for domain in fw.domains:
        controls.extend(domain.controls)
    return controls
