#!/usr/bin/env python3
"""
Proper VeighNa WebTrader Server
Based on vnpy_webtrader source code patterns
"""

from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy_webtrader import WebEngine
import threading
import time

def main():
    """Start VeighNa WebTrader Server properly"""
    print("Starting VeighNa WebTrader Server...")

    # Create VeighNa core engines
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)

    print("VeighNa core engine initialized")

    # Create WebEngine directly (this is the actual web server)
    web_engine = WebEngine(main_engine, event_engine)

    print("WebEngine created")
    print(f"WebEngine type: {type(web_engine)}")

    # Check available methods
    methods = [method for method in dir(web_engine) if not method.startswith('_')]
    print(f"WebEngine methods: {methods}")

    # Start the web server
    try:
        print("Starting web server...")

        # The WebEngine should have a start or run method
        if hasattr(web_engine, 'start'):
            print("Using start() method...")
            web_engine.start()
        elif hasattr(web_engine, 'run'):
            print("Using run() method...")
            web_engine.run()
        else:
            print("No start/run method found. Available methods:")
            for method in methods:
                if 'start' in method.lower() or 'run' in method.lower() or 'serve' in method.lower():
                    print(f"  - {method}")

        print("Web server should be running now!")
        print("Check http://localhost:8080 or similar...")

        # Keep running
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down web server...")
    except Exception as e:
        print(f"Error starting web server: {e}")

if __name__ == "__main__":
    main()