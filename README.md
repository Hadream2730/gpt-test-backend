# GPT Responses API Backend

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
```
OPENAI_API_KEY=your_api_key
```

## Run

```bash
uvicorn main:app --reload
```

## Endpoint

POST /chat

```json
{
  "system": "You are a helpful assistant",
  "messages": [
    { "role": "user", "content": "Hello!" }
  ]
}
```
