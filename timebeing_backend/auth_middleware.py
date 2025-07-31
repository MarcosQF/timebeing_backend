import os
import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from clerk_backend_api import Clerk, AuthenticateRequestOptions

from .settings import settings

# Configure logger
logger = logging.getLogger(__name__)

# Initialize Clerk SDK
clerk_secret = settings.CLERK_SECRET_KEY or os.getenv("CLERK_SECRET_KEY")
jwt_key = settings.JWT_KEY or os.getenv("JWT_KEY")

if not clerk_secret:
    logger.error("CLERK_SECRET_KEY não configurada")
    raise ValueError("CLERK_SECRET_KEY é obrigatória")

if not jwt_key:
    logger.error("JWT_KEY não configurada")
    raise ValueError("JWT_KEY é obrigatória")

clerk_sdk = Clerk(bearer_auth=clerk_secret)

async def get_current_user_id(request: Request) -> str:
    """
    Dependency to extract and validate user ID from Clerk JWT token.
    
    Returns:
        str: The authenticated user's ID
        
    Raises:
        HTTPException: If authentication fails or token is invalid
    """
    try:
        # Log the request details for debugging
        auth_header = request.headers.get("authorization")
        origin = request.headers.get("origin")
        
        logger.info(f"Auth attempt - Origin: {origin}, Has Auth Header: {bool(auth_header)}")
        
        if not auth_header:
            logger.warning("No authorization header found")
            raise HTTPException(
                status_code=401, 
                detail="Authorization header missing"
            )

        if not auth_header.startswith("Bearer "):
            logger.warning("Invalid authorization header format")
            raise HTTPException(
                status_code=401, 
                detail="Invalid authorization header format"
            )

        # Authenticate the request using Clerk
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=[
                    "http://localhost:3000",
                    "http://127.0.0.1:3000",
                ],
                jwt_key=jwt_key
            )
        )

        # Check if user is signed in
        if not request_state.is_signed_in:
            logger.warning("User not signed in according to Clerk")
            raise HTTPException(
                status_code=401, 
                detail="Authentication required - user not signed in"
            )

        # Extract user ID from the token payload
        user_id = request_state.payload.get("sub")
        if not user_id:
            logger.error("Token payload missing user ID (sub)")
            raise HTTPException(
                status_code=401, 
                detail="Invalid token - missing user ID"
            )

        return user_id

    except HTTPException as e:
        logger.warning(f"Authentication failed: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Authentication error: {str(e)}"
        )

# Type alias for dependency injection
CurrentUserId = Annotated[str, Depends(get_current_user_id)]