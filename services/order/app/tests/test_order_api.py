from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest
import json
from unittest import mock

from app.db.base import Base
from app.db.session import get_db
from app.models.order import OrderStatus
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

@pytest.fixture(autouse=True)
def mock_celery_task():
    with mock.patch("app.api.endpoints.orders.process_order") as mock_task:
        mock_task.delay.return_value = None
        yield mock_task

@pytest.fixture(autouse=True)
def mock_product_service():
    with mock.patch("app.crud.order.requests.get") as mock_get:
        mock_response = mock.MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "id": "test-product-id",
            "name": "Test Product",
            "price": 99.99,
            "stock": 10
        }
        mock_get.return_value = mock_response
        yield mock_get

@pytest.fixture
def sample_order_data():
    return {
        "user_id": "test-user-id",
        "shipping_address": "123 Test St, Test City, TS 12345",
        "billing_address": "123 Test St, Test City, TS 12345",
        "notes": "Test order notes",
        "items": [
            {
                "product_id": "test-product-id",
                "quantity": 2
            }
        ]
    }

def test_create_order(sample_order_data, mock_celery_task):
    response = client.post("/api/v1/orders/", json=sample_order_data)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == sample_order_data["user_id"]
    assert data["status"] == OrderStatus.PENDING
    assert data["total_amount"] == 199.98
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == "test-product-id"
    assert data["items"][0]["quantity"] == 2
    
    mock_celery_task.delay.assert_called_once()

def test_get_order():
    sample_data = {
        "user_id": "test-user-id",
        "shipping_address": "123 Test St, Test City, TS 12345",
        "billing_address": "123 Test St, Test City, TS 12345",
        "notes": "Test order notes",
        "items": [{"product_id": "test-product-id", "quantity": 1}]
    }
    create_response = client.post("/api/v1/orders/", json=sample_data)
    order_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["user_id"] == sample_data["user_id"]

def test_get_user_orders():
    user_id = "test-user-for-multiple-orders"
    for i in range(2):
        sample_data = {
            "user_id": user_id,
            "shipping_address": f"Address {i}",
            "billing_address": f"Address {i}",
            "notes": f"Order {i}",
            "items": [{"product_id": "test-product-id", "quantity": 1}]
        }
        client.post("/api/v1/orders/", json=sample_data)
    
    response = client.get(f"/api/v1/orders/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(order["user_id"] == user_id for order in data)

def test_update_order_status():
    sample_data = {
        "user_id": "test-user-id",
        "shipping_address": "123 Test St, Test City, TS 12345",
        "billing_address": "123 Test St, Test City, TS 12345",
        "notes": "Test order notes",
        "items": [{"product_id": "test-product-id", "quantity": 1}]
    }
    create_response = client.post("/api/v1/orders/", json=sample_data)
    order_id = create_response.json()["id"]
    
    status_update = {"status": OrderStatus.SHIPPED}
    response = client.patch(f"/api/v1/orders/{order_id}/status", json=status_update)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == OrderStatus.SHIPPED

def test_cancel_order():
    sample_data = {
        "user_id": "test-user-id",
        "shipping_address": "123 Test St, Test City, TS 12345",
        "billing_address": "123 Test St, Test City, TS 12345",
        "notes": "Test order notes",
        "items": [{"product_id": "test-product-id", "quantity": 1}]
    }
    create_response = client.post("/api/v1/orders/", json=sample_data)
    order_id = create_response.json()["id"]
    
    response = client.post(f"/api/v1/orders/{order_id}/cancel")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == OrderStatus.CANCELLED 