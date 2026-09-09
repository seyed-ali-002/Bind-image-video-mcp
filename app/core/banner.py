from __future__ import annotations

from app.core.config import settings
from app.core.connection import info

WIDTH = 76


def _row(label: str, value: str) -> str:
    text = f"{label:<18} {value}"
    return f"│ {text:<{WIDTH - 2}} │"


def _box(title: str, rows: list[tuple[str, str]]) -> None:
    print("┌" + "─" * WIDTH + "┐")
    print(f"│ {title:<{WIDTH - 2}} │")
    print("├" + "─" * WIDTH + "┤")
    for label, value in rows:
        print(_row(label, value))
    print("└" + "─" * WIDTH + "┘")


def startup(port: int) -> None:
    data = info(mask_token=False)
    print()
    _box(
        "BINA  •  IMAGE & VIDEO MCP SERVER",
        [
            ("Status", "RUNNING"),
            ("Local", f"http://{settings.host}:{port}"),
            ("MCP", f"http://{settings.host}:{port}/mcp"),
            ("Connector", data["custom_connector_url"]),
            ("Token", data["token"]),
        ],
    )
    print("  Health       /health")
    print("  Doctor       /doctor")
    print("  Providers    /providers")
    print("  Assets       /assets")
    print("  Stop         Ctrl+C")
    print()
