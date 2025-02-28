# User Management Microservice

This microservice handles user registration, authentication, and profile management for the MicroEcom platform.

## Features

- User registration with email and username validation
- Secure password hashing with bcrypt
- JWT-based authentication
- User profile management
- PostgreSQL database integration
- Alembic migrations
- Input validation with Pydantic
- Email validation with email-validator

## API Endpoints

### User Authentication

- `POST /api/v1/register` - Register a new user
  ```json
  {
    "email": "user@example.com",
    "username": "username",
    "password": "password123",
    "full_name": "Full Name"
  }
  ```

- `POST /api/v1/login/access-token` - Login and get access token
  ```
  Form data:
  username: user@example.com
  password: password123
  ```

### User Profile Management

- `GET /api/v1/me` - Get current user profile
  ```
  Header:
  Authorization: Bearer {access_token}
  ```

- `PUT /api/v1/me` - Update current user profile
  ```json
  {
    "full_name": "Updated Name"
  }
  ```

### Admin Access

- `GET /api/v1/users/{user_id}` - Get user by ID (requires admin privileges or to be the same user)

### Service Health

- `GET /api/v1/health` - Health check endpoint

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

## Development

### Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables (or create a .env file):
   ```
   POSTGRES_SERVER=localhost
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=user_db
   POSTGRES_PORT=5432
   SECRET_KEY=yoursecretkey
   ```

3. Run migrations:
   ```
   alembic upgrade head
   ```

4. Start the service:
   ```
   uvicorn main:app --reload --port 8001
   ```

### Testing

Run tests with pytest:
```
pytest app/tests
```

## Docker

Build and run with Docker:
```
docker build -t user-service .
docker run -p 8001:8001 user-service
```

Or use docker-compose:
```
docker-compose up -d
```

## Recent Updates

- Fixed circular import issues between database models
- Added email-validator package for proper email validation
- Integrated Pydantic v2 compatibility changes
- Enhanced error handling for duplicate email/username validation 