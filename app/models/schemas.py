from pydantic import BaseModel, ConfigDict
from typing import Optional

class ImagePair(BaseModel):
    id: Optional[int] = None
    property_id: Optional[int] = None
    original_url: str
    edited_url: str
    description: str
    compliance_id: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class Property(BaseModel):
    id: Optional[int] = None
    address: str
    realtor_id: int
    price: float
    disclosure_status: Optional[str] = "Pending"
    image_pairs: list[ImagePair] = []
    
    model_config = ConfigDict(from_attributes=True)
