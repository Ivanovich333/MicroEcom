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
- **.github/workflows/** - CI/CD pipeline configuration

## Architecture

- **Microservices Pattern**: Each service has its own responsibility and database
- **Database per Service**: Each microservice has its dedicated PostgreSQL database
- **API-First Design**: Well-documented RESTful APIs with OpenAPI/Swagger
- **Health Checks**: Each service has a health endpoint for monitoring
- **Containerization**: Docker for consistent development and deployment
- **CI/CD Pipeline**: Automated testing, building, and deployment with GitHub Actions

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

### Development Environment Setup

To set up your development environment, install the dependencies for the services you're working on:

```bash
cd services/user && pip install -r requirements.txt
cd services/product && pip install -r requirements.txt
cd services/order && pip install -r requirements.txt
cd services/api && pip install -r requirements.txt
```

## Testing

Each service includes its own test suite using pytest. The tests can be run within the Docker containers:

```bash
docker-compose exec product python -m pytest
docker-compose exec user python -m pytest
```

Or locally:

```bash
cd services/user && python -m pytest
cd services/product && python -m pytest
```

## Database Management

The system uses PostgreSQL with separate databases for each service:
- User DB: Port 5432
- Product DB: Port 5433

## CI/CD Pipeline

The project includes a comprehensive CI/CD pipeline implemented with GitHub Actions:

### Workflow Files

- **ci-cd.yml**: Main workflow for linting, testing, building, and deploying
- **security-scan.yml**: Security scanning for dependencies, code, and container images
- **infra-validation.yml**: Infrastructure validation for Docker Compose and Dockerfiles

### Pipeline Stages

1. **Lint**: Code quality checks with flake8, black, and isort
2. **Test**: Run unit and integration tests with pytest
3. **Build**: Build Docker images and push to GitHub Container Registry
4. **Security Scan**: Check for vulnerabilities in dependencies and code
5. **Deploy**: Deploy to staging or production environments

### Environment Deployments

- Pushes to `develop` branch deploy to the staging environment
- Pushes to `main` branch deploy to the production environment

### Status Badges

[![CI/CD Pipeline](https://github.com/yourusername/MicroEcom/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/yourusername/MicroEcom/actions/workflows/ci-cd.yml)
[![Security Scan](https://github.com/yourusername/MicroEcom/actions/workflows/security-scan.yml/badge.svg)](https://github.com/yourusername/MicroEcom/actions/workflows/security-scan.yml)
[![Infrastructure Validation](https://github.com/yourusername/MicroEcom/actions/workflows/infra-validation.yml/badge.svg)](https://github.com/yourusername/MicroEcom/actions/workflows/infra-validation.yml)

### Using the CI/CD Pipeline

1. **For Developers**:
   - Create a feature branch from `develop`
   - Make changes and push to GitHub
   - Create a pull request to `develop`
   - CI pipeline will run automatically
   - After approval and merge, changes will be deployed to staging

2. **For Release Managers**:
   - Create a pull request from `develop` to `main`
   - After approval and merge, changes will be deployed to production

## Documentation

For more detailed information about the CI/CD pipeline, see [CI/CD Pipeline Documentation](docs/ci-cd-pipeline.md).