from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Order Processing Service"
    
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "order_db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_BACKEND_URL: str = os.getenv("CELERY_BACKEND_URL", "redis://redis:6379/0")
    
    USER_SERVICE_URL: str = os.getenv("USER_SERVICE_URL", "http://user:8001")
    PRODUCT_SERVICE_URL: str = os.getenv("PRODUCT_SERVICE_URL", "http://product:8002")
    
    USER_SERVICE_ADMIN_EMAIL: str = os.getenv("USER_SERVICE_ADMIN_EMAIL", "admin@example.com")
    USER_SERVICE_ADMIN_PASSWORD: str = os.getenv("USER_SERVICE_ADMIN_PASSWORD", "admin123")

settings = Settings() 