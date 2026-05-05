from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from google.genai import Client
import os

app = FastAPI()
client = Client(api_key=os.environ.get("GEMINI_API_KEY"))


@app.get("/api/idea", response_class=PlainTextResponse)
def idea():
    prompt = "Give me a great unexpected idea to become mega rich!"
    response = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
    return response.text
