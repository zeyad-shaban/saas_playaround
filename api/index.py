from typing import Any
from dotenv import load_dotenv
_ = load_dotenv(dotenv_path=".env.local")

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse
from google.genai import Client
from google.api_core import exceptions as google_exceptions
import os
from .auth import verify_token


app = FastAPI()
client = Client(api_key=os.environ.get("GEMINI_API_KEY"))


@app.get("/api/python/idea", response_class=StreamingResponse)
async def idea(user_data: dict[str, Any] = Depends(verify_token)):
    user_id = user_data.get("sub")
    print(f"Generating idea for user: {user_id}")
    
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
            
    return StreamingResponse(
        stream_generator(),
        media_type="event-stream",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache",
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
