import os
import shutil
import signal
import socket
import subprocess
import time

from rich.console import Console

from oldy import config, log

console = Console()


def is_installed() -> bool:
    return shutil.which("ollama") is not None


def install() -> None:
    with console.status("[bold]Installing Ollama...[/]"):
        result = subprocess.run(
            "curl -fsSL https://ollama.com/install.sh | sh",
            shell=True,
            capture_output=True,
            text=True,
        )
    if result.returncode != 0:
        raise RuntimeError(f"Ollama install failed:\n{result.stderr}")


def is_pulled(model_name: str) -> bool:
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
        return model_name in result.stdout
    except subprocess.TimeoutExpired:
        return False


def pull(model_name: str) -> None:
    if is_pulled(model_name):
        console.print(f"[dim]{model_name} already downloaded.[/]")
        return
    console.print(f"[bold]Pulling {model_name}...[/]")
    result = subprocess.run(["ollama", "pull", model_name])
    if result.returncode != 0:
        e = RuntimeError(f"Failed to pull {model_name}")
        log.write("ERROR", str(e))
        raise e


def start() -> None:
    # If already serving (e.g. Windows tray app), skip spawning a new process
    if _port_open("localhost", 11434):
        config.set("ollama_pid", None)
        log.write("START", f"model={config.get().get('selected_model', 'unknown')} (reused existing)")
        return

    proc = subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    config.set("ollama_pid", proc.pid)

    for _ in range(20):
        time.sleep(0.5)
        if _port_open("localhost", 11434):
            log.write("START", f"model={config.get().get('selected_model', 'unknown')}")
            return
    e = RuntimeError("Ollama did not start within 10 seconds")
    log.write("ERROR", str(e))
    raise e


def stop() -> None:
    if os.name == "nt":
        try:
            subprocess.run(["taskkill", "/F", "/IM", "ollama app.exe"], capture_output=True)
            subprocess.run(["taskkill", "/F", "/IM", "ollama.exe"], capture_output=True)
        except OSError:
            pass
    else:
        pid = config.get().get("ollama_pid")
        if pid:
            try:
                os.kill(pid, signal.SIGTERM)
            except (ProcessLookupError, OSError):
                pass
    log.write("STOP")
    config.set("ollama_pid", None)


def _port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False
