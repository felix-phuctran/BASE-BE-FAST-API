from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.env import Env, env

async_engine = create_async_engine(
    env.SQLALCHEMY_TRIPC_SOLUTIONS_URI.unicode_string(),
    pool_size=10,  # Default number of connections to keep in the pool
    max_overflow=20,  # Extra connections allowed when pool is full
    pool_timeout=30,  # Max seconds to wait for a connection before timing out
    pool_recycle=1800,  # Reconnect if a connection is older than 1800s (30 min)
    pool_pre_ping=True,  # Ping the connection before using to ensure it's valid
    future=True,  # Use the future (SQLAlchemy 2.0) style engine
)

# Create an async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


engine = create_engine(
    env.SQLALCHEMY_TRIPC_SOLUTIONS_URI.unicode_string(),
    pool_size=20,
    max_overflow=40,
    pool_timeout=60,
    pool_recycle=3600,
    pool_pre_ping=True,
)


# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
