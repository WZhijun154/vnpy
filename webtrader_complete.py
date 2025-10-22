#!/usr/bin/env python3
"""
Complete VeighNa WebTrader Server
This starts both the RPC server (backend) and FastAPI web server (frontend)
"""

import threading
import time
import uvicorn
from pathlib import Path

from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy_webtrader import WebEngine
from vnpy_webtrader.web import app  # FastAPI app
from vnpy.trader.utility import get_file_path

def create_config_file():
    """Create default web_trader_setting.json if it doesn't exist"""
    config = {
        "username": "admin",
        "password": "admin",
        "req_address": "tcp://localhost:2014",
        "sub_address": "tcp://localhost:4102"
    }

    config_path = get_file_path("web_trader_setting.json")
    if not Path(config_path).exists():
        import json
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"Created config file: {config_path}")
    return config

def start_rpc_server():
    """Start the VeighNa RPC server (backend)"""
    print("Starting VeighNa RPC Server...")

    # Create VeighNa core
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)

    # Create WebEngine (RPC server)
    web_engine = WebEngine(main_engine, event_engine)

    # Start RPC server with default addresses
    rep_address = "tcp://*:2014"  # Request-Reply port
    pub_address = "tcp://*:4102"  # Publish-Subscribe port

    print(f"RPC REP address: {rep_address}")
    print(f"RPC PUB address: {pub_address}")

    web_engine.start_server(rep_address, pub_address)
    print("RPC Server started successfully!")

    return web_engine

def start_web_server():
    """Start the FastAPI web server (frontend)"""
    print("Starting FastAPI Web Server...")

    # Start uvicorn server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )

def main():
    """Start complete WebTrader system"""
    print("=" * 50)
    print("VeighNa WebTrader Complete Server")
    print("=" * 50)

    # Create config file if needed
    config = create_config_file()

    # Start RPC server in background thread
    rpc_thread = threading.Thread(target=start_rpc_server, daemon=True)
    rpc_thread.start()

    # Give RPC server time to start
    time.sleep(2)

    print("\n" + "=" * 50)
    print("Starting Web Frontend...")
    print("Web Interface will be available at: http://localhost:8080")
    print("Default login: admin/admin")
    print("=" * 50)

    try:
        # Start web server (this blocks)
        start_web_server()
    except KeyboardInterrupt:
        print("\nShutting down servers...")

if __name__ == "__main__":
    main()