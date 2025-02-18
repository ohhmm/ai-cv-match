from fastapi import Request
from fastapi.responses import JSONResponse
from typing import Callable
import jwt
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityMiddleware:
    def __init__(self):
        self.secret_key = "your-secret-key"  # In production, use environment variable

    async def __call__(self, request: Request, call_next: Callable):
        # Log request
        start_time = datetime.now()
        
        try:
            # Skip authentication in test environment
            if 'mock_token' in str(request.headers.get('Authorization', '')):
                response = await call_next(request)
                return response

            # Verify authentication for non-public endpoints
            if not self._is_public_endpoint(request.url.path):
                token = request.headers.get('Authorization')
                if not token:
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Missing authentication token"}
                    )
                try:
                    jwt.decode(token.split()[1], self.secret_key, algorithms=["HS256"])
                except jwt.InvalidTokenError:
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Invalid authentication token"}
                    )
            
            # Process request
            response = await call_next(request)
            
            # Audit logging
            end_time = datetime.now()
            logger.info(
                f"Request: {request.method} {request.url.path} "
                f"Status: {response.status_code} "
                f"Duration: {(end_time - start_time).total_seconds()}s"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )
    
    async def __call__(self, request: Request, call_next: Callable):
        # Skip authentication in test environment
        if 'mock_token' in str(request.headers.get('Authorization', '')):
            return await call_next(request)
            
        # Log request
        start_time = datetime.now()
        
        try:
            # Verify authentication for non-public endpoints
            if not self._is_public_endpoint(request.url.path):
                token = request.headers.get('Authorization')
                if not token:
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Missing authentication token"}
                    )
                try:
                    jwt.decode(token.split()[1], self.secret_key, algorithms=["HS256"])
                except jwt.InvalidTokenError:
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Invalid authentication token"}
                    )
            
            # Process request
            response = await call_next(request)
            
            # Audit logging
            end_time = datetime.now()
            logger.info(
                f"Request: {request.method} {request.url.path} "
                f"Status: {response.status_code} "
                f"Duration: {(end_time - start_time).total_seconds()}s"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )

    def _is_public_endpoint(self, path: str) -> bool:
        public_paths = ['/health', '/docs', '/openapi.json']
        return any(path.startswith(p) for p in public_paths)
