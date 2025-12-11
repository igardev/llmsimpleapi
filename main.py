from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import httpx

app = FastAPI(
    title="LLM Simple API Application",
    description="A simple API to interact with LLMs",
    version="1.0.0"
)


class AskRequest(BaseModel):
    prompt: str


class AskResponse(BaseModel):
    response: str


class ConfigureRequest(BaseModel):
    endpoint: Optional[str] = None
    model: Optional[str] = None
    api_key: Optional[str] = None


class ConfigureResponse(BaseModel):
    message: str
    endpoint: str
    model: str
    api_key: str


class ConfigureEndpointRequest(BaseModel):
    endpoint: str


class ConfigureEndpointResponse(BaseModel):
    message: str
    endpoint: str


class ConfigureModelRequest(BaseModel):
    model: str


class ConfigureModelResponse(BaseModel):
    message: str
    model: str


class ConfigureKeyRequest(BaseModel):
    api_key: str


class ConfigureKeyResponse(BaseModel):
    message: str
    api_key: str


class ConfigureGetResponse(BaseModel):
    endpoint: str
    model: str
    api_key: str


# In-memory storage
endpoint = "http://127.0.0.1:8011/v1/chat/completions"
model = ""
api_key = ""


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to LLM Simple API Application"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/configure/endpoint", response_model=ConfigureEndpointResponse)
async def configure_endpoint(config: ConfigureEndpointRequest):
    """Configure only the LLM endpoint."""
    global endpoint
    endpoint = config.endpoint
    return {
        "message": "Endpoint updated successfully",
        "endpoint": endpoint,
    }


@app.post("/configure/model", response_model=ConfigureModelResponse)
async def configure_model(config: ConfigureModelRequest):
    """Configure only the LLM model."""
    global model
    model = config.model
    return {
        "message": "Model updated successfully",
        "model": model,
    }


@app.post("/configure/key", response_model=ConfigureKeyResponse)
async def configure_key(config: ConfigureKeyRequest):
    """Configure only the LLM API key."""
    global api_key
    api_key = config.api_key
    return {
        "message": "API key updated successfully",
        "api_key": api_key,
    }


@app.get("/configure/get", response_model=ConfigureGetResponse)
async def get_configuration():
    """Return current configuration values."""
    return {
        "endpoint": endpoint,
        "model": model,
        "api_key": api_key,
    }


@app.post("/configure", response_model=ConfigureResponse)
async def configure_llm(config: ConfigureRequest):
    """Configure the LLM endpoint, model, and API key"""
    global endpoint, model, api_key
    
    if config.endpoint is not None:
        endpoint = config.endpoint
    if config.model is not None:
        model = config.model
    if config.api_key is not None:
        api_key = config.api_key
    
    return {
        "message": "Configuration updated successfully",
        "endpoint": endpoint,
        "model": model,
        "api_key": api_key
    }


@app.post("/ask", response_model=AskResponse)
async def ask_llm(body: AskRequest):
    """Send a prompt to the configured LLM and return its response."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": body.prompt},
        ],
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(endpoint, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"LLM request failed: {exc.response.text}",
        )
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"LLM request error: {exc}")

    data = resp.json()
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise HTTPException(status_code=502, detail="Unexpected LLM response format")

    return {"response": content}

