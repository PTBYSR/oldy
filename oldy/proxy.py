import os
import signal
import subprocess
import sys
import time
from collections import deque

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import httpx

from oldy import config

app = FastAPI()
# We use an async client to handle streaming responses perfectly
client = httpx.AsyncClient(base_url="http://127.0.0.1:11434")

# Rate limiting: 30 requests per minute
request_history = deque()
RATE_LIMIT = 30
WINDOW_SIZE = 60

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
async def proxy(request: Request, path: str):
    api_key = config.get().get("api_key")
    auth_header = request.headers.get("authorization")

    # 1. Require Bearer Token
    if not auth_header or auth_header != f"Bearer {api_key}":
        raise HTTPException(status_code=401, detail="Unauthorized. Invalid API Key.")

    # 2. Rate Limiting
    now = time.time()
    while request_history and request_history[0] < now - WINDOW_SIZE:
        request_history.popleft()
    
    if len(request_history) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too Many Requests. Rate limit: 30/min.")
    
    request_history.append(now)

    # 3. Forward request to Ollama
    # Strip headers that might confuse Ollama (like Host, which triggers 403s)
    forward_headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host", "authorization")}

    url_path = request.url.path
    if request.url.query:
        url_path += "?" + request.url.query

    req = client.build_request(
        request.method,
        url_path,
        content=request.stream(),
        headers=forward_headers,
        timeout=None # Prevent timeout for long generations
    )
    
    r = await client.send(req, stream=True)
    return StreamingResponse(
        r.aiter_raw(), 
        status_code=r.status_code, 
        media_type=r.headers.get("content-type")
    )


def start():
    # Start uvicorn proxy in the background on port 11435
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "oldy.proxy:app", "--host", "127.0.0.1", "--port", "11435"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    config.set("proxy_pid", proc.pid)

def stop():
    pid = config.get().get("proxy_pid")
    if pid:
        try:
            if os.name == "nt":
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True)
            else:
                os.kill(pid, signal.SIGTERM)
        except (ProcessLookupError, OSError):
            pass
    config.set("proxy_pid", None)
