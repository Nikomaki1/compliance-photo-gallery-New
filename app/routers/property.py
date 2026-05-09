from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import Optional
import uuid

from app.database import get_db
from app.models import orm_models

router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)

# ======= PYDANTIC SCHEMAS =======
class ImagePair(BaseModel):
    id: Optional[int] = None
    property_id: Optional[int] = None
    before_url: str
    after_url: str
    description: str
    compliance_id: Optional[str] = None
    
    # This allows Pydantic to read data directly from the SQLAlchemy ORM!
    model_config = ConfigDict(from_attributes=True)

class Property(BaseModel):
    id: Optional[int] = None
    address: str
    realtor_id: int
    price: float
    disclosure_status: Optional[str] = "Pending"
    image_pairs: list[ImagePair] = []
    
    model_config = ConfigDict(from_attributes=True)


# ======= ENDPOINTS =======

@router.get("/{property_id}", response_model=Property)
def get_property(property_id: int, db: Session = Depends(get_db)):
    # Query database instead of returning dummy data
    db_prop = db.query(orm_models.Property).filter(orm_models.Property.id == property_id).first()
    if not db_prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_prop

@router.post("/", response_model=Property)
def create_property(property: Property, db: Session = Depends(get_db)):
    # Create database object
    new_prop = orm_models.Property(
        address=property.address,
        realtor_id=property.realtor_id,
        price=property.price
    )
    db.add(new_prop)
    db.commit()
    db.refresh(new_prop) # Grab the auto-generated ID from SQLite
    return new_prop

@router.post("/{property_id}/upload-pair", response_model=ImagePair)
def upload_property_pair(property_id: int, image_pair: ImagePair, db: Session = Depends(get_db)):
    # Validate property exists first
    db_prop = db.query(orm_models.Property).filter(orm_models.Property.id == property_id).first()
    if not db_prop:
        raise HTTPException(status_code=404, detail="Property not found")
        
    # Set the unique token
    generated_compliance_id = image_pair.compliance_id or f"COMP-{uuid.uuid4().hex[:8].upper()}"
    
    # Save the images permanently to the database
    new_pair = orm_models.ImagePair(
        property_id=property_id,
        before_url=image_pair.before_url,
        after_url=image_pair.after_url,
        description=image_pair.description,
        compliance_id=generated_compliance_id
    )
    db.add(new_pair)
    db.commit()
    db.refresh(new_pair)
    
    return new_pair
