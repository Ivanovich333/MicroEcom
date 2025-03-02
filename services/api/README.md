# API Gateway Microservice

This microservice serves as the API gateway for the MicroEcom platform, routing requests to the appropriate microservices.

## Features

- Request routing to microservices
- Single entry point for all client applications
- FastAPI framework
- Reverse proxy capabilities
- Service discovery
- Docker containerization
- Load balancing

## API Endpoints

| Method | URL | Description |
| ------ | --- | ----------- |
| * | /api/v1/users/* | Forward to User Management Service |
| * | /api/v1/products/* | Forward to Product Catalog Service |
| * | /docs | Swagger documentation |
| * | /redoc | ReDoc documentation |

## Development

### Prerequisites

- Python 3.9+
- Docker and Docker Compose (for containerized development)

### Local Development

1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Set environment variables (see below)
5. Run the application: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`

### Using Docker

1. Build the image: `docker build -t api-gateway .`
2. Run the container: `docker run -p 8000:8000 api-gateway`

### Using Docker Compose

Run `docker-compose up -d` from the root of the project to start all services including this one.

## Environment Variables

| Variable | Description | Default |
| -------- | ----------- | ------- |
| USER_SERVICE_URL | URL of the User Management Service | http://user:8001 |
| PRODUCT_SERVICE_URL | URL of the Product Catalog Service | http://product:8002 |

## Architecture

The API Gateway serves as the entry point for all client requests, routing them to the appropriate microservices based on the URL path. It provides a unified API while abstracting the underlying microservices architecture from clients. 