# Product Catalog Microservice

This microservice is responsible for managing the product catalog for the MicroEcom platform.

## Features

- Product CRUD operations
- PostgreSQL integration
- RESTful API
- FastAPI framework
- Pydantic data validation
- SQLAlchemy ORM
- Alembic migrations
- Docker containerization
- Health check endpoint

## API Endpoints

| Method | URL | Description |
| ------ | --- | ----------- |
| GET | /api/v1/health | Check service health |
| GET | /api/v1/products | List all products |
| GET | /api/v1/products/{product_id} | Get product by ID |
| POST | /api/v1/products | Create a new product |
| PUT | /api/v1/products/{product_id} | Update a product |
| DELETE | /api/v1/products/{product_id} | Delete a product |

## Development

### Prerequisites

- Python 3.9+
- Docker and Docker Compose (for containerized development)
- PostgreSQL (for local development without Docker)

### Local Development

1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Set environment variables (see below)
5. Run the application: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8002`

### Using Docker

1. Build the image: `docker build -t product-service .`
2. Run the container: `docker run -p 8002:8002 product-service`

### Using Docker Compose

Run `docker-compose up -d` from the root of the project to start all services including this one.

### Testing

The service includes comprehensive tests using pytest:

```bash
# Run tests within the Docker container
docker-compose exec product python -m pytest

# Run tests locally
python -m pytest
```

The tests cover all API endpoints and ensure proper functionality of the product catalog operations.

## Environment Variables

| Variable | Description | Default |
| -------- | ----------- | ------- |
| DATABASE_USER | PostgreSQL username | postgres |
| DATABASE_PASSWORD | PostgreSQL password | postgres |
| DATABASE_HOST | PostgreSQL host | postgres |
| DATABASE_PORT | PostgreSQL port | 5432 |
| DATABASE_NAME | PostgreSQL database name | product_db |
| SERVICE_NAME | Service name for health checks | product | 