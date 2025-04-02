from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from api.v1.api import api_router
from core.env import env
from middleware.auth_session_middleware import check_auth_session_middleware
from middleware.cookie_session_middleware import add_cookie_session_middleware
from middleware.cors_middleware import add_cors_middleware
from utils.logger import setup_logger

logger = setup_logger()

def create_application():
    """Create and configure the FastAPI application"""
    # Create FastAPI application
    app = FastAPI(
        title="TRIPC SOLUTIONS API",
        description="Backend API for Ally AI platform",
        version="1.0.0",
        docs_url="/docs" if env.ENV != "production" else None,
        redoc_url="/redoc" if env.ENV != "production" else None,
    )

    # Configure middleware (order matters)
    configure_middleware(app)
    
    # Configure routes
    configure_routes(app)
    
    # Log environment
    if env.ENV in ["local", "dev"]:
        logger.info(f"API is running in {env.ENV} environment")
        
    return app

def configure_middleware(app):
    """Configure all middleware for the application"""
    # CORS should be first
    add_cors_middleware(app)
    
    # Cookie session second
    add_cookie_session_middleware(app)
    
    # Compression middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Auth session last
    app.middleware("http")(check_auth_session_middleware)

def configure_routes(app):
    """Configure all routes for the application"""
    # Include API routes
    app.include_router(api_router, prefix=env.API_V1_STR)
    
    # Health check endpoint
    @app.get("/api/v1/health", tags=["Health"])
    async def health_check():
        return {"status": "healthy"}

# Create the application
app = create_application()

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# delete all folders __pycache__ in the project
# FOR /R . %G IN (__pycache__) DO (IF EXIST "%G" (RMDIR /S /Q "%G"))

# uninstall all packages in environment python
# for /F %i in ('pip freeze') do pip uninstall -y %i

# install all packages in requirements.txt
# pip install -r requirements.txt

# remove all unused import and variables in the project
# powershell -Command "Get-ChildItem -Recurse -Include *.py -Exclude __init__.py | ForEach-Object { autoflake --remove-all-unused-imports --remove-unused-variables --in-place $_.FullName }"


