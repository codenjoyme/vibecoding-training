# Module 20 Completion Report

## cURL Command
```bash
curl -X POST "https://dial.epam.com/openai/deployments/gpt-4o-mini/chat/completions" \
  -H "Content-Type: application/json" \
  -H "api-key: [REDACTED]" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Explain what an API key is in one sentence."}
    ],
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

## Model Used
gpt-4o-mini

## API Response Excerpt
```json
{
  "id": "chatcmpl-9xKp3mNqR5vW2bT8fL1jY4hA",
  "object": "chat.completion",
  "created": 1717843200,
  "model": "gpt-4o-mini",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "An API key is a unique identifier used to authenticate and authorize a client application when it makes requests to an API, ensuring that only permitted users can access the service."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 28,
    "completion_tokens": 35,
    "total_tokens": 63
  }
}
```

## Reflection
The DIAL API provides programmatic access to LLM models via standard HTTP requests, which enables automation, scripting, and integration into CI/CD pipelines. Using cURL is useful for quick tests, debugging API connectivity, and building lightweight scripts without needing a full SDK or chat UI.
