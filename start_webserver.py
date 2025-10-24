#!/usr/bin/env python3
"""Standalone launcher for the VeighNa WebTrader stack."""

from __future__ import annotations

import json
from importlib import import_module
from pathlib import Path
from typing import Dict

import uvicorn

from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.utility import get_file_path
from vnpy_webtrader import WebEngine


CONFIG_FILENAME: str = "web_trader_setting.json"
DEFAULT_CONFIG: Dict[str, str] = {
    "username": "admin",
    "password": "admin",
    "req_address": "tcp://127.0.0.1:2014",
    "sub_address": "tcp://127.0.0.1:4102",
}


def ensure_web_trader_config() -> Dict[str, str]:
    """Ensure the WebTrader config file exists and contains required keys."""
    config_path: Path = get_file_path(CONFIG_FILENAME)
    config_path.parent.mkdir(parents=True, exist_ok=True)

    data: Dict[str, str] = {}
    if config_path.exists():
        try:
            with config_path.open("r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                data.update(loaded)
        except json.JSONDecodeError:
            print(f"Invalid JSON detected in {config_path}, recreating with defaults.")

    updated: bool = False
    for key, default_value in DEFAULT_CONFIG.items():
        if not data.get(key):
            data[key] = default_value
            updated = True

    previous_exists = config_path.exists()
    if not previous_exists or updated:
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        action = "Updated" if previous_exists else "Created"
        print(f"{action} WebTrader config at {config_path}")

    return data


def derive_bind_address(client_address: str) -> str:
    """Translate a client-facing RPC address to a server bind address."""
    if not client_address.startswith("tcp://"):
        return client_address

    try:
        host_port = client_address.split("://", 1)[1]
        host, port = host_port.rsplit(":", 1)
    except ValueError:
        return client_address

    host = host.strip()
    if host == "localhost":
        return f"tcp://127.0.0.1:{port}"

    return client_address


def load_fastapi_app() -> object:
    """Import the FastAPI application after the config is ready."""
    module = import_module("vnpy_webtrader.web")
    return module.app  # type: ignore[attr-defined]


def main() -> None:
    print("Starting VeighNa WebTrader...")

    config = ensure_web_trader_config()
    rep_address = derive_bind_address(config["req_address"])
    pub_address = derive_bind_address(config["sub_address"])

    print(f"RPC request address: {rep_address}")
    print(f"RPC publish address: {pub_address}")

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    web_engine = WebEngine(main_engine, event_engine)
    web_engine.start_server(rep_address, pub_address)

    fastapi_app = load_fastapi_app()
    host = "0.0.0.0"
    port = 8080
    print(f"Web UI available at http://{host}:{port}")
    print("Press Ctrl+C to stop.")

    try:
        uvicorn.run(fastapi_app, host=host, port=port, log_level="info")
    except KeyboardInterrupt:
        print("\nShutting down WebTrader...")
    finally:
        web_engine.close()
        main_engine.close()


if __name__ == "__main__":
    main()
