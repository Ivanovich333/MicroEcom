# Order Processing Microservice

This microservice handles order processing for the e-commerce platform. It provides APIs for creating, retrieving, and managing orders, and uses Celery with Redis for asynchronous processing of order-related tasks.

## Features

- Create new orders with multiple items
- Retrieve order details and history
- Update order status
- Cancel orders
- Asynchronous processing of orders using Celery
- Integration with User and Product services

## API Endpoints

- `POST /api/v1/orders/` - Create a new order
- `GET /api/v1/orders/` - List all orders
- `GET /api/v1/orders/{order_id}` - Get order details
- `GET /api/v1/orders/user/{user_id}` - Get orders for a specific user
- `PATCH /api/v1/orders/{order_id}/status` - Update order status
- `POST /api/v1/orders/{order_id}/cancel` - Cancel an order

## Architecture

The service follows a clean architecture pattern:

- **API Layer**: FastAPI endpoints for handling HTTP requests
- **Service Layer**: Business logic for order processing
- **Data Layer**: PostgreSQL database for storing order data
- **Async Processing**: Celery with Redis for background tasks

## Development

### Prerequisites

- Python 3.9+
- PostgreSQL
- Redis

### Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the service:
   ```
   uvicorn main:app --reload --host 0.0.0.0 --port 8003
   ```

3. Run Celery worker:
   ```
   celery -A app.celery_worker.celery_app worker --loglevel=info
   ```

### Testing

Run tests using pytest:
```
pytest
```

## Docker

Build and run using Docker:

```
docker build -t order-service .
docker run -p 8003:8003 order-service
```

For the Celery worker:

```
docker build -t order-worker -f Dockerfile.celery .
docker run order-worker
```

## Environment Variables

- `POSTGRES_SERVER` - PostgreSQL server hostname
- `POSTGRES_USER` - PostgreSQL username
- `POSTGRES_PASSWORD` - PostgreSQL password
- `POSTGRES_DB` - PostgreSQL database name
- `POSTGRES_PORT` - PostgreSQL port
- `CELERY_BROKER_URL` - Redis URL for Celery broker
- `CELERY_BACKEND_URL` - Redis URL for Celery result backend
- `USER_SERVICE_URL` - URL for the User service
- `PRODUCT_SERVICE_URL` - URL for the Product service 