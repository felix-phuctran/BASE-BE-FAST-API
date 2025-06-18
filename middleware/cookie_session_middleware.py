from starlette.middleware.sessions import SessionMiddleware

from config.env import env


def add_cookie_session_middleware(app):
    """
    Add cookie-based session middleware to the FastAPI application.
    This middleware handles client-side session storage using encrypted cookies.

    Args:
        app: FastAPI application instance
    """
    app.add_middleware(
        SessionMiddleware,
        secret_key=env.JWT_SECRET_KEY,
        # session_cookie="ally_session",
        # max_age=1800,  # 30 minutes
        # same_site="lax",
        # https_only=env.ENV != "local"  # Only use HTTPS in non-local environments
    )
