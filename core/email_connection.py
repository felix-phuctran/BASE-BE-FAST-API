from fastapi_mail import ConnectionConfig

from config.env import env

conf = ConnectionConfig(
    MAIL_USERNAME=f"{env.MAIL_USERNAME}",
    MAIL_PASSWORD=f"{env.MAIL_PASSWORD}",
    MAIL_FROM=f"{env.MAIL_FROM}",
    MAIL_PORT=int(env.MAIL_PORT),
    MAIL_SERVER=f"{env.MAIL_SERVER}",
    MAIL_STARTTLS=bool(env.MAIL_STARTTLS),
    MAIL_SSL_TLS=bool(env.MAIL_SSL_TLS),
    USE_CREDENTIALS=bool(env.USE_CREDENTIALS),
)
