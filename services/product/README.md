# Product Catalog Microservice

This microservice is responsible for managing the product catalog in the MicroEcom platform.

## Features

- Product management (CRUD operations)
- PostgreSQL integration for data storage
- RESTful API endpoints
- Containerized with Docker

## API Endpoints

- `GET /api/v1/products` - List all products
- `POST /api/v1/products` - Create a new product
- `GET /api/v1/products/{product_id}` - Get a specific product
- `PUT /api/v1/products/{product_id}` - Update a product
- `DELETE /api/v1/products/{product_id}` - Delete a product

## Development

### Prerequisites

- Python 3.11+
- Docker and Docker Compose

### Local Development

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the service:
   ```
   uvicorn main:app --reload --host 0.0.0.0 --port 8002
   ```

4. Access the API documentation at http://localhost:8002/docs

### Running with Docker

```
docker-compose up -d product
```

### Running Tests

```
pytest
```

## Environment Variables

- `ENVIRONMENT` - Development/production environment
- `POSTGRES_SERVER` - PostgreSQL server hostname
- `POSTGRES_USER` - PostgreSQL username
- `POSTGRES_PASSWORD` - PostgreSQL password
- `POSTGRES_DB` - PostgreSQL database name
- `POSTGRES_PORT` - PostgreSQL port 