from fastapi import Request, HTTPException, status
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
    
    def __call__(self, request: Request):
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean up old requests
        self.requests[client_ip] = [
            timestamp for timestamp in self.requests[client_ip]
            if current_time - timestamp < 60
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Try again later."
            )
        
        # Record request
        self.requests[client_ip].append(current_time)

rate_limiter = RateLimiter(requests_per_minute=60)
