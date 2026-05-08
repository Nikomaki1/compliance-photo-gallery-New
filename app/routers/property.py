from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)

class Property(BaseModel):
    id: Optional[int] = None
    address: str
    realtor_id: int
    price: float

@router.get("/{property_id}", response_model=Property)
def get_property(property_id: int):
    # Returning dummy data for now
    return Property(
        id=property_id,
        address="123 Dummy St, Mytown, ST 12345",
        realtor_id=999,
        price=450000.0
    )

@router.post("/", response_model=Property)
def create_property(property: Property):
    # Imitate creating a listing by adding a dummy ID if none exists
    if property.id is None:
        property.id = 101 # Dummy generated ID
    return property
