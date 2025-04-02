from fastapi import HTTPException, Request, status

from container.container import container

auth_service = container.get_service("auth")
translation = container.get_util("translation")
logger = container.get_util("logger")


async def check_auth_session_middleware(request: Request, call_next):
    """
    Middleware to check authentication session validity and manage user activity timeouts.

    This middleware:
    1. Skips authentication for public endpoints
    2. Verifies user is authenticated
    3. Checks if the session is still valid (not timed out)
    4. Updates the user's last activity timestamp

    Args:
        request: FastAPI request object
        call_next: Next middleware in the chain

    Returns:
        Response from the next middleware
    """
    # List of public endpoints that don't require authentication
    public_endpoints = [
        "/api/v1/health",
        "/api/v1/users/assign-role",
        "/docs",
        "/redoc",
        "/openapi.json",
    ]

    # Skip session checks for public endpoints
    if any(request.url.path.startswith(endpoint) for endpoint in public_endpoints):
        return await call_next(request)

    # Continue processing for protected endpoints
    try:
        # Check if user_id exists in request state
        if not hasattr(request.state, "user_id"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=translation.Auth["UnauthorizedAccess"],
            )

        # Get user_id from token
        user_id = request.state.user_id

        # Check session validity
        is_valid = await auth_service._check_session_validity(user_id)
        if not is_valid:
            logger.info(f"Session expired for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=translation.Auth["SessionExpired"],
            )

        # Update last activity timestamp
        await auth_service._update_user_activity(user_id)

        # Continue with the request
        response = await call_next(request)
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in auth session middleware: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=translation.Auth["SessionCreationFailed"],
        )
