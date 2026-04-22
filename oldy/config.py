import json
from pathlib import Path

OLDY_DIR = Path.home() / ".oldy"
CONFIG_FILE = OLDY_DIR / "config.json"


def get() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE) as f:
        return json.load(f)


def set(key: str, value) -> None:
    OLDY_DIR.mkdir(parents=True, exist_ok=True)
    data = get()
    data[key] = value
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def clear() -> None:
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
