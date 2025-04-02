from core.env import env
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

async_engine = create_async_engine(
    env.SQLALCHEMY_ORGS_URI.unicode_string(),
    pool_size=10,        # Default number of connections to keep in the pool
    max_overflow=20,     # Extra connections allowed when pool is full
    pool_timeout=30,     # Max seconds to wait for a connection before timing out
    pool_recycle=1800,   # Reconnect if a connection is older than 1800s (30 min)
    pool_pre_ping=True,  # Ping the connection before using to ensure it's valid
    future=True,         # Use the future (SQLAlchemy 2.0) style engine
)

AsyncOrgSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)
