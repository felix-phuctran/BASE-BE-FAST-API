import os
from typing import Any, Optional

from dotenv import load_dotenv
from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings

load_dotenv()


class Env(BaseSettings):
    ENV: str = os.environ.get("ENV")
    API_V1_STR: str = os.environ.get("API_V1_STR")

    # Redis configuration
    REDIS_URL: str = os.environ.get("REDIS_URL")

    # Postgres configuration
    POSTGRES_ADOOR_SERVER: str = os.environ.get("POSTGRES_ADOOR_SERVER")
    POSTGRES_ADOOR_PORT: int = os.environ.get("POSTGRES_ADOOR_PORT")
    POSTGRES_ADOOR_USER: str = os.environ.get("POSTGRES_ADOOR_USER")
    POSTGRES_ADOOR_PASSWORD: str = os.environ.get("POSTGRES_ADOOR_PASSWORD")
    POSTGRES_ADOOR_DB: str = os.environ.get("POSTGRES_ADOOR_DB")

    # SQL Alchemy configuration
    SQLALCHEMY_ADOOR_URI: Optional[PostgresDsn] = None

    # JWT configuration
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXP_DAYS: int = os.environ.get("JWT_ACCESS_TOKEN_EXP_DAYS")
    JWT_REFRESH_TOKEN_EXP_DAYS: int = os.environ.get("JWT_REFRESH_TOKEN_EXP_DAYS")

    # Webhook facebook configuration
    MY_VERIFY_TOKEN: str = os.environ.get("MY_VERIFY_TOKEN")
    FACEBOOK_URL: str = os.environ.get("FACEBOOK_URL")

    # Webhook zalo configuration
    ZALO_URL: str = os.environ.get("ZALO_URL")
    ZALO_OAUTH_URL: str = os.environ.get("ZALO_OAUTH_URL")

    # Google oauth configuration
    GOOGLE_CLIENT_ID: str = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.environ.get("GOOGLE_CLIENT_SECRET")

    # CORS configuration
    BASE_FRONT_END_URL: str = os.environ.get("BASE_FRONT_END_URL")
    BASE_AI_URL: str = os.environ.get("BASE_AI_URL")

    # Email configuration
    MAIL_USERNAME: str = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.environ.get("MAIL_PASSWORD")
    MAIL_FROM: str = os.environ.get("MAIL_FROM")
    MAIL_PORT: int = os.environ.get("MAIL_PORT")
    MAIL_SERVER: str = os.environ.get("MAIL_SERVER")
    MAIL_STARTTLS: bool = os.environ.get("MAIL_STARTTLS")
    MAIL_SSL_TLS: bool = os.environ.get("MAIL_SSL_TLS")
    USE_CREDENTIALS: bool = os.environ.get("USE_CREDENTIALS")

    # WARN: Remember to configure these two environment variables in docker-compose.yml after removing them
    # AWS_ACCESS_KEY_ID: str = os.environ.get("AWS_ACCESS_KEY_ID")
    # AWS_SECRET_ACCESS_KEY: str = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_BUCKET: str = os.environ.get("AWS_BUCKET")
    CLOUDFRONT_DOMAIN: str = os.environ.get("CLOUDFRONT_DOMAIN")
    USE_CLOUDFRONT: bool = os.environ.get("USE_CLOUDFRONT", "True").lower() == "true"

    # CDN configuration
    CHECK_IP_URL: str = os.environ.get("CHECK_IP_URL")
    CLIENT_IP: str = os.environ.get("CLIENT_IP")

    @field_validator("SQLALCHEMY_ADOOR_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data.get("POSTGRES_ADOOR_USER"),
            password=info.data.get("POSTGRES_ADOOR_PASSWORD"),
            host=info.data.get("POSTGRES_ADOOR_SERVER"),
            port=info.data.get("POSTGRES_ADOOR_PORT"),
            path=info.data.get("POSTGRES_ADOOR_DB"),
        )

    class Config:
        case_sensitive = True


env = Env()
