from datetime import datetime
from oldy.config import OLDY_DIR

LOG_FILE = OLDY_DIR / "oldy.log"


def write(event: str, detail: str = "") -> None:
    OLDY_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp}  {event:<10} {detail}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)
