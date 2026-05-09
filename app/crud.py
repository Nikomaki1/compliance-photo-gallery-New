from sqlalchemy.orm import Session
from app.models import orm_models
import uuid

def create_property(db: Session, address: str, realtor_id: int, price: float, disclosure_status: str = "Pending"):
    """Create a new property listing."""
    db_property = orm_models.Property(
        address=address,
        realtor_id=realtor_id,
        price=price,
        disclosure_status=disclosure_status
    )
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

def add_image_pair(db: Session, property_id: int, original_url: str, edited_url: str, description: str, compliance_id: str = None):
    """Add an ImagePair to an existing property."""
    comp_id = compliance_id or uuid.uuid4().hex[:8].upper()
    db_image_pair = orm_models.ImagePair(
        property_id=property_id,
        original_url=original_url,
        edited_url=edited_url,
        description=description,
        compliance_id=comp_id
    )
    db.add(db_image_pair)
    db.commit()
    db.refresh(db_image_pair)
    return db_image_pair

def get_image_pairs_by_property(db: Session, property_id: int):
    """Retrieve all image pairs for a property by its ID."""
    return db.query(orm_models.ImagePair).filter(orm_models.ImagePair.property_id == property_id).all()

def update_property_disclosure_status(db: Session, property_id: int, new_status: str):
    """Update a property's disclosure status."""
    db_property = db.query(orm_models.Property).filter(orm_models.Property.id == property_id).first()
    if db_property:
        db_property.disclosure_status = new_status
        db.commit()
        db.refresh(db_property)
    return db_property
