# LLM Simple API Application

A FastAPI service to interact with Large Language Models (LLMs). It exposes endpoints to configure the target LLM (endpoint, model, API key) and to send prompts.

<img width="1741" height="808" alt="image" src="https://github.com/user-attachments/assets/28842038-8553-4709-a277-2ab024c30087" />


## Setup
1) Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
2) Install dependencies:
```bash
pip install .
```

## Run
```bash
uvicorn main:app --reload
```
The server runs at `http://localhost:8000`.

## Endpoints
- `GET /` — Welcome message
- `GET /health` — Health check
- `POST /configure` — Update endpoint, model, and api_key (all optional)
- `POST /configure/endpoint` — Update only endpoint
- `POST /configure/model` — Update only model
- `POST /configure/key` — Update only api_key
- `GET /configure/get` — Fetch current endpoint, model, and api_key
- `POST /ask` — Send a prompt to the configured LLM and get the response

## Request Examples
Update endpoint/model/api_key:
```bash
curl -X POST http://localhost:8000/configure \
  -H "Content-Type: application/json" \
  -d '{"endpoint": "http://127.0.0.1:8011/v1/chat/completions", "model": "gpt-4.1", "api_key": "your-key"}'
```

Ask the LLM:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?"}'
```

## Notes
- The configuration is stored in memory; restart resets values to defaults defined in `main.py`.
- Ensure your editor uses the project virtualenv to resolve imports and suppress linter warnings.

