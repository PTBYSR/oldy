import psutil
import platform


def detect() -> dict:
    return {
        "ram_gb": round(psutil.virtual_memory().total / 1e9, 1),
        "cpu_cores": psutil.cpu_count(logical=False),
        "os": platform.system(),
    }
