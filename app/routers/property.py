from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import orm_models, schemas
from app import crud

router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)

@router.get("/{property_id}", response_model=schemas.Property)
def get_property(property_id: int, db: Session = Depends(get_db)):
    db_prop = db.query(orm_models.Property).filter(orm_models.Property.id == property_id).first()
    if not db_prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_prop

@router.post("/", response_model=schemas.Property)
def create_property(property: schemas.Property, db: Session = Depends(get_db)):
    return crud.create_property(
        db=db,
        address=property.address,
        realtor_id=property.realtor_id,
        price=property.price,
        disclosure_status=property.disclosure_status
    )

@router.post("/{property_id}/upload-pair", response_model=schemas.ImagePair)
def upload_property_pair(property_id: int, image_pair: schemas.ImagePair, db: Session = Depends(get_db)):
    db_prop = db.query(orm_models.Property).filter(orm_models.Property.id == property_id).first()
    if not db_prop:
        raise HTTPException(status_code=404, detail="Property not found")
        
    return crud.add_image_pair(
        db=db,
        property_id=property_id,
        original_url=image_pair.original_url,
        edited_url=image_pair.edited_url,
        description=image_pair.description,
        compliance_id=image_pair.compliance_id
    )
