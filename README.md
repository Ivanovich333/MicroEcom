# MicroEcom

MicroEcom is a microservices-based e-commerce platform built with FastAPI, designed for serverless environments and high scalability. Each service is containerized for easy deployment and management.

## Project Structure

- **services/** - Contains all microservices
  - **user/** - User Management Microservice
    - User registration, authentication, and profile management
  - **product/** - Product Catalog Microservice
    - Product CRUD operations, catalog management
  - **api/** - API Gateway for service orchestration
    - Route and proxy requests to appropriate microservices
  - **Future services**:
    - **cart/** - Shopping Cart Microservice
    - **order/** - Order Management Microservice
    - **payment/** - Payment Processing Microservice
- **docs/** - Documentation

## Architecture

- **Microservices Pattern**: Each service has its own responsibility and database
- **Database per Service**: Each microservice has its dedicated PostgreSQL database
- **API-First Design**: Well-documented RESTful APIs with OpenAPI/Swagger
- **Health Checks**: Each service has a health endpoint for monitoring
- **Containerization**: Docker for consistent development and deployment
- **CI/CD Ready**: Designed for easy integration with CI/CD pipelines

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+

### Running Locally

1. Clone the repository
2. Run `docker-compose up -d`
3. Services will be available at:
   - API Gateway: http://localhost:8000
   - User Service: http://localhost:8001
   - Product Service: http://localhost:8002
4. Access service documentation:
   - User Service: http://localhost:8001/docs
   - Product Service: http://localhost:8002/docs

## Testing

Each service includes its own test suite using pytest. The tests can be run within the Docker containers:

```bash
docker-compose exec product python -m pytest
docker-compose exec user python -m pytest
```

## Database Management

The system uses PostgreSQL with separate databases for each service:
- User DB: Port 5432
- Product DB: Port 5433