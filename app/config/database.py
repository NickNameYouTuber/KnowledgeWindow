from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings
import urllib.parse


# URL encode the password and other components to handle special characters
def create_safe_database_url(url: str) -> str:
    # Parse the existing URL
    parsed = urllib.parse.urlparse(url)

    # Reconstruct the URL with proper encoding
    safe_url = f"postgresql://{parsed.username}:{urllib.parse.quote(parsed.password)}@{parsed.hostname}"

    # Add port if it exists
    if parsed.port:
        safe_url += f":{parsed.port}"

    # Add database name
    safe_url += f"/{parsed.path[1:]}"  # Remove leading slash from path

    return safe_url


# Create database URL with proper encoding
SAFE_DATABASE_URL = create_safe_database_url(settings.DATABASE_URL)

# Create engine with updated connection parameters
engine = create_engine(
    SAFE_DATABASE_URL,
    connect_args={
        "client_encoding": "utf8",
        "options": "-c client_encoding=utf8"
    }
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()