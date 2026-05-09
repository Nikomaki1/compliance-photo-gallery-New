from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    realtor_id = Column(Integer)
    price = Column(Float)
    disclosure_status = Column(String, default="Pending")

    # Establish the link between a property and its submitted ImagePairs
    image_pairs = relationship("ImagePair", back_populates="property")

class ImagePair(Base):
    __tablename__ = "image_pairs"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    original_url = Column(String)
    edited_url = Column(String)
    description = Column(String)
    is_structural_change = Column(Boolean, default=False)
    compliance_id = Column(String, unique=True, index=True)

    property = relationship("Property", back_populates="image_pairs")
