# MicroEcom

MicroEcom is a microservices-based e-commerce platform built with FastAPI, designed for serverless environments and high scalability. Each service is containerized for easy deployment and management.

## Project Structure

- **services/** - Contains all microservices
  - **user/** - User Management Microservice
    - User registration, authentication, and profile management
  - **product/** - Product Catalog Microservice
  - **cart/** - Shopping Cart Microservice
  - **order/** - Order Management Microservice
  - **payment/** - Payment Processing Microservice
  - **gateway/** - API Gateway for service orchestration
- **docs/** - Documentation
- **scripts/** - Utility scripts

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+

### Running Locally

1. Clone the repository
2. Run `docker-compose up -d`
3. Access the API at http://localhost:8000
4. Access the documentation at http://localhost:8000/docs