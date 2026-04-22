import psutil
import httpx
from datetime import datetime
from oldy import config


def get_status() -> dict:
    cfg = config.get()

    mem = psutil.virtual_memory()
    ram_used_gb  = round(mem.used / 1e9, 1)
    ram_total_gb = round(mem.total / 1e9, 1)
    ram_percent  = mem.percent

    cpu_percent = psutil.cpu_percent(interval=1)

    started_at = cfg.get("started_at")
    if started_at:
        delta = datetime.now() - datetime.fromisoformat(started_at)
        uptime = str(delta).split(".")[0]
    else:
        uptime = "not running"

    try:
        r = httpx.get("http://localhost:11434", timeout=2)
        ollama_alive = r.status_code == 200
    except Exception:
        ollama_alive = False

    return {
        "ram_used_gb":  ram_used_gb,
        "ram_total_gb": ram_total_gb,
        "ram_percent":  ram_percent,
        "cpu_percent":  cpu_percent,
        "uptime":       uptime,
        "model":        cfg.get("selected_model", "none"),
        "public_url":   cfg.get("public_url", "not set"),
        "api_key":      cfg.get("api_key", "not set"),
        "ollama_alive": ollama_alive,
    }
