import pytest
from unittest.mock import MagicMock, patch
import os
import requests

from app.celery_worker.tasks import process_order
from app.models.order import OrderStatus
from app.schemas.order import OrderUpdateStatus


@pytest.fixture
def mock_env_vars():
    os.environ["USE_SQLITE"] = "False"
    yield
    if "USE_SQLITE" in os.environ:
        del os.environ["USE_SQLITE"]


@pytest.fixture
def mock_db_session():
    with patch("app.celery_worker.tasks.SessionLocal") as mock_session:
        db_session = MagicMock()
        mock_session.return_value = db_session
        yield mock_session


@pytest.fixture
def mock_get_order():
    with patch("app.celery_worker.tasks.get_order_by_id") as mock:
        yield mock


@pytest.fixture
def mock_update_status():
    with patch("app.celery_worker.tasks.update_order_status") as mock:
        yield mock


@pytest.fixture
def mock_requests():
    with patch("app.celery_worker.tasks.requests.get") as mock:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "test-product-1",
            "name": "Test Product",
            "price": 99.99,
            "stock": 10
        }
        mock_response.raise_for_status = MagicMock()
        mock.return_value = mock_response
        yield mock


@pytest.fixture
def mock_order():
    order = MagicMock()
    order.id = "test-order-id"
    order.user_id = "test-user-1"
    order.items = [
        MagicMock(product_id="test-product-1", quantity=2)
    ]
    return order


def test_process_order_success(mock_db_session, mock_get_order, mock_update_status, mock_requests, mock_order, mock_env_vars):
    mock_get_order.return_value = mock_order
    
    result = process_order("test-order-id")

    assert "processed successfully" in result

    assert mock_update_status.call_count == 2
    assert mock_update_status.call_args_list[0][0][2].status == OrderStatus.PROCESSING
    assert mock_update_status.call_args_list[1][0][2].status == OrderStatus.SHIPPED

    assert mock_requests.call_count == 1
    mock_requests.assert_called_with(f"http://product:8002/api/v1/products/test-product-1")


def test_process_order_product_unavailable(mock_db_session, mock_get_order, mock_update_status, mock_requests, mock_order, mock_env_vars):
    mock_get_order.return_value = mock_order
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "test-product-1",
        "name": "Test Product",
        "price": 99.99,
        "stock": 1
    }
    mock_response.raise_for_status = MagicMock()
    mock_requests.return_value = mock_response
    
    result = process_order("test-order-id")

    assert "Insufficient stock" in result

    assert mock_update_status.call_count == 2
    assert mock_update_status.call_args_list[0][0][2].status == OrderStatus.PROCESSING
    assert mock_update_status.call_args_list[1][0][2].status == OrderStatus.CANCELLED


def test_process_order_not_found(mock_db_session, mock_get_order, mock_update_status, mock_env_vars):
    mock_get_order.return_value = None
    
    result = process_order("test-order-id")

    assert "not found" in result

    mock_update_status.assert_not_called() 