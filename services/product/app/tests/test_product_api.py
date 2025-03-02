from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest
import json

from app.db.base import Base
from app.db.session import get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def sample_product():
    return {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 99.99,
        "stock": 10,
        "image_url": "https://example.com/test.jpg"
    }

@pytest.fixture
def updated_product():
    return {
        "name": "Updated Test Product",
        "description": "This is an updated test product",
        "price": 199.99,
        "stock": 20,
        "image_url": "https://example.com/updated.jpg"
    }

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "product"}

def test_get_all_products_empty():
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert response.json() == []

def test_product_crud_flow(sample_product, updated_product):
    
    response = client.post(
        "/api/v1/products",
        json=sample_product,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_product["name"]
    assert data["price"] == sample_product["price"]
    assert data["stock"] == sample_product["stock"]
    assert "id" in data
    product_id = data["id"]

    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_product["name"]
    assert data["price"] == sample_product["price"]
    assert data["stock"] == sample_product["stock"]

    response = client.put(
        f"/api/v1/products/{product_id}",
        json=updated_product,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_product["name"]
    assert data["price"] == updated_product["price"]
    assert data["stock"] == updated_product["stock"]

    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_product["name"]
    assert data["price"] == updated_product["price"]
    assert data["stock"] == updated_product["stock"]

    response = client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == updated_product["name"]
    assert data[0]["price"] == updated_product["price"]
    assert data[0]["stock"] == updated_product["stock"]

    response = client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == 200

    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 404

def test_partial_update_product(sample_product):
    
    response = client.post(
        "/api/v1/products",
        json=sample_product,
    )
    assert response.status_code == 201
    product_id = response.json()["id"]
    
    partial_update = {
        "name": "Partially Updated Product",
        "price": 149.99
    }
    response = client.put(
        f"/api/v1/products/{product_id}",
        json=partial_update,
    )
    assert response.status_code == 200
    data = response.json()
    
    assert data["name"] == partial_update["name"]
    assert data["price"] == partial_update["price"]
    
    assert data["stock"] == sample_product["stock"]
    assert data["description"] == sample_product["description"]
    assert data["image_url"] == sample_product["image_url"]
    
    client.delete(f"/api/v1/products/{product_id}")

def test_nonexistent_product():
    response = client.get("/api/v1/products/9999")
    assert response.status_code == 404

def test_invalid_product_data():
    invalid_product = {
        "name": "Invalid Product",
        "price": "not a number",
        "stock": 10
    }
    response = client.post(
        "/api/v1/products",
        json=invalid_product,
    )
    assert response.status_code == 422