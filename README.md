<p align="center">
  <img src="oldy-hero.png" alt="Oldy Header" width="100">
</p>

# Oldy

Turn any old laptop into an AI server with a dedicated free API key.

## What it does

Install Oldy on a low-RAM laptop. It detects your hardware, picks a model that fits,
starts a local AI server, and gives you a public URL you can hit from anywhere.

## Requirements

- Python 3.10+
- Linux or macOS
- 4GB+ RAM

## Install

pip install oldy

## Usage

oldy start      # detect hardware, pick model, start server, get public URL
oldy stop       # shut everything down
oldy status     # RAM, CPU, uptime, current model
oldy models     # browse and switch models
oldy logs       # live request log
oldy url        # print your public URL
oldy key        # print your secure API key

## Why Oldy?

While Ollama is the engine, Oldy is the specialized driver for old hardware:

- **Hardware Safety:** Ollama will let you download models that crash your laptop; Oldy calculates your RAM/CPU first to ensure a stable experience.
- **Instant Public Access:** Ollama only works on `localhost`; Oldy automatically sets up a secure public URL and API key.
- **Hardware Monitoring:** Oldy gives you built-in status checks to see exactly how the model is performing on your specific hardware.

## Connecting to Oldy

Oldy is compatible with the OpenAI API format. You can use any standard library, but you must provide your public URL as the `base_url` and your API key.

### Python (OpenAI SDK)

```python
from openai import OpenAI

client = OpenAI(
    base_url="YOUR_OLDY_URL/v1",
    api_key="YOUR_API_KEY"
)

response = client.chat.completions.create(
    model="gemma:2b",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

### cURL

```bash
curl -X POST YOUR_OLDY_URL/api/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gemma:2b", "prompt": "Hello!", "stream": false}'
```

## How it works


Oldy manages Ollama under the hood. You never touch Ollama directly.
An ngrok tunnel makes your local server publicly accessible without
port forwarding or networking setup. All traffic is secured by a 
built-in FastAPI proxy that requires an API key and enforces 
rate limits to protect your laptop's hardware.

## Supported models (v1)

| Model            | Size   | Min RAM |
|------------------|--------|---------|
| tinyllama        | 0.6GB  | 1GB     |
| qwen2:1.5b       | 0.9GB  | 2GB     |
| deepseek-r1:1.5b | 1.1GB  | 2GB     |
| gemma:2b         | 1.5GB  | 3GB     |
| llama3.2:3b      | 2.0GB  | 3GB     |
| phi3:mini        | 2.3GB  | 4GB     |
| mistral:7b       | 4.1GB  | 6GB     |
