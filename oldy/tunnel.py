import io
import os
import platform
import signal
import subprocess
import time
import zipfile

import httpx

from oldy import config, log
from oldy.config import OLDY_DIR

NGROK_PATH = OLDY_DIR / ("ngrok.exe" if os.name == "nt" else "ngrok")


def _get_download_url() -> str:
    system = platform.system().lower()
    machine = platform.machine().lower()
    arch = "amd64" if "x86_64" in machine or "amd64" in machine else "arm64"

    if system == "windows":
        return f"https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-{arch}.zip"
    if system == "linux":
        return f"https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-{arch}.tgz"
    if system == "darwin":
        return f"https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-{arch}.zip"
    raise RuntimeError(f"Unsupported OS: {system}")


def _download_ngrok() -> None:
    print("Downloading ngrok...")
    url = _get_download_url()
    with httpx.stream("GET", url, follow_redirects=True) as r:
        r.raise_for_status()
        data = b"".join(r.iter_bytes())

    if url.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            binary_name = "ngrok.exe" if os.name == "nt" else "ngrok"
            with zf.open(binary_name) as src, open(NGROK_PATH, "wb") as dst:
                dst.write(src.read())
    else:
        import tarfile
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
            member = tf.getmember("ngrok")
            with tf.extractfile(member) as src, open(NGROK_PATH, "wb") as dst:
                dst.write(src.read())

    if os.name != "nt":
        import stat
        NGROK_PATH.chmod(NGROK_PATH.stat().st_mode | stat.S_IEXEC)


def _prompt_for_token() -> None:
    print("\nngrok requires a free account for public URLs.")
    print("  1. Sign up at:        https://dashboard.ngrok.com/signup")
    print("  2. Verify your email  (check inbox)")
    print("  3. Copy your token:   https://dashboard.ngrok.com/get-started/your-authtoken\n")

    try:
        token = input("Paste your ngrok auth token: ").strip()
    except (KeyboardInterrupt, EOFError):
        raise RuntimeError("No auth token provided.")
    if not token:
        raise RuntimeError("No auth token provided.")

    config.set("ngrok_token", token)
    print("Auth token saved.\n")


def ensure_ngrok() -> None:
    OLDY_DIR.mkdir(parents=True, exist_ok=True)
    if not NGROK_PATH.exists():
        _download_ngrok()
    if not config.get().get("ngrok_token"):
        _prompt_for_token()


def start(port: int = 11434) -> str:
    token = config.get().get("ngrok_token")
    if not token:
        raise RuntimeError("No ngrok auth token set.")

    proc = subprocess.Popen(
        [str(NGROK_PATH), "http", str(port), "--authtoken", token, "--host-header=localhost", "--log", "stdout"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    config.set("tunnel_pid", proc.pid)

    deadline = time.time() + 15
    while time.time() < deadline:
        time.sleep(1)
        try:
            r = httpx.get("http://localhost:4040/api/tunnels", timeout=2)
            for t in r.json().get("tunnels", []):
                url = t.get("public_url", "")
                if url.startswith("https://"):
                    config.set("public_url", url)
                    log.write("TUNNEL", f"url={url}")
                    return url
        except Exception:
            pass

        if proc.poll() is not None:
            output = proc.stdout.read() if proc.stdout else ""
            log.write("ERROR", f"ngrok exited: {output[:500]}")
            print(f"\n[ngrok error]\n{output}\n")
            config.set("public_url", None)
            return None

    log.write("ERROR", "ngrok did not return URL within 15s")
    config.set("public_url", None)
    return None


def stop() -> None:
    pid = config.get().get("tunnel_pid")
    if pid:
        try:
            if os.name == "nt":
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True)
            else:
                os.kill(pid, signal.SIGTERM)
        except (ProcessLookupError, OSError):
            pass
    config.set("tunnel_pid", None)
    config.set("public_url", None)
