# User Management Microservice

This microservice handles user registration, authentication, and profile management for the MicroEcom platform.

## Features

- User registration with email validation
- Secure password hashing with bcrypt
- JWT-based authentication
- User profile management
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
| POST | /api/v1/register | Register a new user |
| POST | /api/v1/login/access-token | Login and get access token |
| GET | /api/v1/me | Get current user profile |
| PUT | /api/v1/me | Update current user profile |
| GET | /api/v1/users/{user_id} | Get user by ID (admin only) |

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
5. Run migrations: `alembic upgrade head`
6. Run the application: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8001`

### Using Docker

1. Build the image: `docker build -t user-service .`
2. Run the container: `docker run -p 8001:8001 user-service`

### Using Docker Compose

Run `docker-compose up -d` from the root of the project to start all services including this one.

### Testing

The service includes comprehensive tests using pytest:

```bash
# Run tests within the Docker container
docker-compose exec user python -m pytest

# Run tests locally
python -m pytest
```

The tests cover authentication, user registration, and profile management endpoints.

## Environment Variables

| Variable | Description | Default |
| -------- | ----------- | ------- |
| DATABASE_USER | PostgreSQL username | postgres |
| DATABASE_PASSWORD | PostgreSQL password | postgres |
| DATABASE_HOST | PostgreSQL host | postgres |
| DATABASE_PORT | PostgreSQL port | 5432 |
| DATABASE_NAME | PostgreSQL database name | user_db |
| SECRET_KEY | Secret key for JWT token generation | None |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration time in minutes | 60 |
| SERVICE_NAME | Service name for health checks | user |

## Architecture

The service follows a clean architecture pattern with:

- **Models**: SQLAlchemy ORM models for database interaction
- **Schemas**: Pydantic schemas for request/response validation
- **CRUD**: Database access operations
- **API**: FastAPI endpoints
- **Auth**: Authentication mechanisms including JWT token handling
- **Core**: Core configuration and settings

## Database Schema

The User model includes:
- id (UUID): Unique identifier
- email: User's email (unique)
- username: User's username (unique)
- hashed_password: Securely hashed password
- full_name: User's full name
- is_active: Whether the user account is active
- is_superuser: Whether the user has admin privileges
- created_at: Timestamp of account creation
- updated_at: Timestamp of last account update

## Recent Updates

- Fixed circular import issues between database models
- Added email-validator package for proper email validation
- Integrated Pydantic v2 compatibility changes
- Enhanced error handling for duplicate email/username validation 