<p align="center">
  <img src="oldy-hero.png" alt="Oldy Header" width="100">
</p>

# ⚡ Oldy

**Turn any old laptop into an AI server with a dedicated free API key.**

Oldy is a lightweight wrapper for [Ollama](https://ollama.com) designed specifically for recycling old hardware into accessible AI endpoints.

## 🚀 Quick Start

### Install
```bash
pip install oldy
```

### Usage
```bash
oldy start      # Auto-detect hardware, pick model, and start public server
oldy stop       # Shut down the tunnel and local engine
oldy status     # Check RAM, CPU, and model performance
oldy models     # Browse and switch between supported models
oldy logs       # View live request logs
oldy url        # Display your public ngrok URL
oldy key        # Display your secure API key
```

## 🧠 Why Oldy?

While Ollama is the engine, Oldy is the specialized driver for aging hardware:

- **Hardware Safety:** Ollama will let you download models that crash your system; Oldy calculates your RAM/CPU first to ensure a stable experience.
- **Instant Public Access:** Ollama only works on `localhost`; Oldy automatically provisions a secure public URL and API key.
- **Hardware Monitoring:** Built-in status checks help you see exactly how the model is performing on your specific hardware.

---

## 🔌 Connecting

Oldy is compatible with the OpenAI API format. Just provide your public URL as the `base_url` and your generated API key.

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

---

## 🛠️ How it works

Oldy manages Ollama under the hood so you don't have to. An **ngrok tunnel** makes your local server publicly accessible without networking setup. All traffic is secured by a built-in **FastAPI proxy** that handles:
- **Authentication:** Only requests with your Bearer token are allowed.
- **Rate Limiting:** Enforces a 30 req/min limit to prevent hardware overheating.
- **Header Sanitization:** Ensures compatibility between public requests and the local engine.

## 📊 Supported Models (v1)

| Model            | Size   | Min RAM |
|------------------|--------|---------|
| tinyllama        | 0.6GB  | 1GB     |
| qwen2:1.5b       | 0.9GB  | 2GB     |
| deepseek-r1:1.5b | 1.1GB  | 2GB     |
| gemma:2b         | 1.5GB  | 3GB     |
| llama3.2:3b      | 2.0GB  | 3GB     |
| phi3:mini        | 2.3GB  | 4GB     |
| mistral:7b       | 4.1GB  | 6GB     |

---
*Requirements: Python 3.10+, Linux/macOS/Windows, 4GB+ RAM.*
