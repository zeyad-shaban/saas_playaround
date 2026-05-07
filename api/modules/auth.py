from fastapi import HTTPException, Depends, Request
from jose import jwt, JWTError
import os
from collections.abc import Mapping

# 1. Grab the public key from env
PUBLIC_KEY = os.environ.get("PEM_Public_Key")


async def verify_token(request: Request) -> Mapping[str, object]:
    assert PUBLIC_KEY is not None, "CLERK_JWT_PUBLIC_KEY not found in enviornment variables"
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = auth_header.split(" ")[1]

    try:
        # Verify the token using the Public Key
        # This checks: 1. Is the signature real? 2. Is it expired?
        payload = jwt.decode(
            token, 
            PUBLIC_KEY, 
            algorithms=["RS256"],
            # Clerk uses your Frontend URL as the 'azp' (Authorized Party)
            options={"verify_aud": False} 
        )
        return payload  # This contains the user's ID and data
    except JWTError as e:
        print(f"JWT Verification Failed: {e}")
        raise HTTPException(status_code=401, detail="Token is invalid or expired")