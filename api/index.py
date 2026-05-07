from typing import Any
from dotenv import load_dotenv
from pathlib import Path
from urllib import error as urllib_error
from urllib import request as urllib_request
import requests
import json

_ = load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env.local")

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from google.genai import Client
from google.api_core import exceptions as google_exceptions
import os
from api.modules.auth import verify_token

app = FastAPI()
client = Client(api_key=os.environ.get("GEMINI_API_KEY"))

CLERK_SECRET_KEY = os.environ.get("CLERK_SECRET_KEY")
CLERK_API_BASE = "https://api.clerk.com/v1"


def _get_user_subscription_status(user_id: str) -> str:
    if not CLERK_SECRET_KEY:
        raise RuntimeError("CLERK_SECRET_KEY is missing")

    url = f"{CLERK_API_BASE}/users/{user_id}/billing/subscription"
    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {CLERK_SECRET_KEY}",
            "Content-Type": "application/json",
        },
    ).json()

    return response["subscription_items"][0]["plan"]["slug"]


def _has_paid_subscription(user_id: str) -> bool:
    status = _get_user_subscription_status(user_id)
    return status in {"basic_tier"}


async def stream_generator():
    try:
        prompt = "Give me a great unexpected idea to become mega rich!"

        response_stream = await client.aio.models.generate_content_stream(model="gemini-3.1-flash-lite-preview", contents=prompt)

        async for chunk in response_stream:
            if chunk.text:
                yield chunk.text

    except google_exceptions.ResourceExhausted as e:
        yield "ERROR: Model quota exceeded. Please try again later."
        print(f"[Quota Error] {str(e)}")

    except google_exceptions.InvalidArgument as e:
        yield "ERROR: Invalid request to Gemini API. Please check your prompt."
        print(f"[Invalid Argument] {str(e)}")

    except google_exceptions.ServiceUnavailable as e:
        yield "ERROR: Gemini API service is temporarily unavailable. Please try again."
        print(f"[Service Unavailable] {str(e)}")

    except google_exceptions.DeadlineExceeded as e:
        yield "ERROR: Request timed out. Please try again."
        print(f"[Timeout] {str(e)}")

    except Exception as e:
        yield f"ERROR: An unexpected error occurred: {str(e)}"
        print(f"[Unexpected Error] {type(e).__name__}: {str(e)}")


@app.get("/api/python/idea", response_class=StreamingResponse)
async def idea(user_data: dict[str, Any] = Depends(verify_token)):
    user_id = user_data.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized: missing user id")

    try:
        is_paid = _has_paid_subscription(user_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    if not is_paid:
        raise HTTPException(status_code=403, detail="Forbidden: active paid subscription required")

    print(f"Generating idea for user: {user_id}, paid_subscriber: {is_paid}")

    return StreamingResponse(
        stream_generator(),
        media_type="event-stream",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache",
        },
    )


if __name__ == "__main__":
    uvicorn.run("api.index:app", host="127.0.0.1", port=8000, reload=True)
