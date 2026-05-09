import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Connect to an isolated test SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_compliance.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Recreate tables specifically for the test
Base.metadata.create_all(bind=engine)

# Dependency override so our FastAPI routes use this test database instead of the real one
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_property_with_two_images():
    # 1. Create a dummy property in the DB via POST endpoint
    prop_response = client.post(
        "/properties/",
        json={
            "address": "900 Test Highway",
            "realtor_id": 55,
            "price": 100000.0,
            "disclosure_status": "Pending"
        }
    )
    assert prop_response.status_code == 200
    property_id = prop_response.json()["id"]

    # 2. Upload first image pair
    img_resp_1 = client.post(
        f"/properties/{property_id}/upload-pair",
        json={
            "original_url": "https://images.com/before1.jpg",
            "edited_url": "https://images.com/after1.jpg",
            "description": "Fixed roof leak"
        }
    )
    assert img_resp_1.status_code == 200

    # 3. Upload second image pair
    img_resp_2 = client.post(
        f"/properties/{property_id}/upload-pair",
        json={
            "original_url": "https://images.com/before2.jpg",
            "edited_url": "https://images.com/after2.jpg",
            "description": "Repainted exterior"
        }
    )
    assert img_resp_2.status_code == 200

    # 4. Assert that GET endpoint retrieves the property AND its exactly 2 linked pairs
    final_response = client.get(f"/properties/{property_id}")
    assert final_response.status_code == 200
    
    data = final_response.json()
    
    assert "image_pairs" in data, "No image_pairs key found in property response"
    assert len(data["image_pairs"]) == 2, "Endpoint did not return exactly 2 image pairs"
    
    descriptions = [pair["description"] for pair in data["image_pairs"]]
    assert "Fixed roof leak" in descriptions
    assert "Repainted exterior" in descriptions
