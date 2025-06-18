from fastapi.middleware.cors import CORSMiddleware

from config.env import env


def add_cors_middleware(app):
    """
    Add CORS middleware to the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    origins = [
        "http://localhost:3000",
        env.BASE_FRONT_END_URL,
        env.FACEBOOK_URL,
        env.ZALO_URL,
        env.ZALO_OAUTH_URL,
    ]

    # Filter out None values
    origins = [origin for origin in origins if origin]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
