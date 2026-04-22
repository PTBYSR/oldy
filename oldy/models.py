from rich.console import Console
from rich.table import Table
from oldy import config

console = Console()

MODELS = [
    {"name": "tinyllama",        "size_gb": 0.6,  "params": "1.1B", "quant": "Q4"},
    {"name": "qwen2:1.5b",       "size_gb": 0.9,  "params": "1.5B", "quant": "Q4"},
    {"name": "deepseek-r1:1.5b", "size_gb": 1.1,  "params": "1.5B", "quant": "Q4"},
    {"name": "gemma:2b",         "size_gb": 1.5,  "params": "2B",   "quant": "Q4"},
    {"name": "llama3.2:3b",      "size_gb": 2.0,  "params": "3B",   "quant": "Q4"},
    {"name": "phi3:mini",        "size_gb": 2.3,  "params": "3.8B", "quant": "Q4"},
    {"name": "mistral:7b",       "size_gb": 4.1,  "params": "7B",   "quant": "Q4"},
]


def get_safety_label(model_size_gb: float, ram_gb: float) -> tuple[str, str]:
    ratio = model_size_gb / ram_gb
    if ratio < 0.7:
        return "✓ safe", "green"
    if ratio < 0.9:
        return "⚠  tight", "yellow"
    return "✗ too large", "red"


def filter_models(ram_gb: float) -> list[dict]:
    return [m for m in MODELS if m["size_gb"] <= ram_gb]


def pick(hw: dict) -> str:
    ram_gb = hw["ram_gb"]
    available = filter_models(ram_gb)

    table = Table(show_header=True, header_style="bold")
    table.add_column("#",      style="dim", width=3)
    table.add_column("Model",  min_width=20)
    table.add_column("Params", width=7)
    table.add_column("Size",   width=7)
    table.add_column("RAM fit", width=13)

    for i, m in enumerate(available, start=1):
        label, color = get_safety_label(m["size_gb"], ram_gb)
        table.add_row(
            str(i),
            m["name"],
            m["params"],
            f"{m['size_gb']}GB",
            f"[{color}]{label}[/{color}]",
        )

    console.print(table)

    import sys
    choices = [m["name"] for m in available]
    sys.stdout.write("Select number or model name: ")
    sys.stdout.flush()
    try:
        answer = sys.stdin.readline().strip()
    except (KeyboardInterrupt, EOFError):
        raise SystemExit(1)
    if not answer:
        raise SystemExit(1)

    if answer.isdigit():
        idx = int(answer) - 1
        if 0 <= idx < len(available):
            answer = available[idx]["name"]
        else:
            console.print(f"[red]Invalid number. Pick 1–{len(available)}.[/red]")
            return pick(hw)

    if answer not in choices:
        console.print("[red]Invalid selection.[/red]")
        return pick(hw)

    config.set("selected_model", answer)
    return answer
