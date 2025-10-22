#!/usr/bin/env python3
"""
VeighNa WebTrader Server Startup Script
Based on official documentation: https://www.vnpy.com/docs/cn/community/app/web_trader.html
"""

from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine

# Import WebTrader application
from vnpy_webtrader import WebTraderApp, WebEngine

# Optional: Add some trading gateways if needed
# from vnpy_ctp import CtpGateway

def main():
    """
    Start VeighNa with WebTrader module
    """
    print("Starting VeighNa WebTrader Server...")

    # Create event engine and main engine
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)

    # Add WebTrader application
    main_engine.add_app(WebTraderApp)

    # Optional: Add trading gateways
    # main_engine.add_gateway(CtpGateway)

    print("VeighNa Engine initialized successfully")
    print("Available apps:", list(main_engine.apps.keys()))

    # WebTrader app is loaded as "RpcService"
    if "RpcService" in main_engine.apps:
        print("WebTrader (RpcService) app loaded successfully")
        webtrader_app = main_engine.apps["RpcService"]

        # Start the web server
        print("Starting WebTrader web server...")
        print("WebTrader app methods:", [method for method in dir(webtrader_app) if not method.startswith('_')])

        # Check if it has WebEngine
        if hasattr(webtrader_app, 'engine') and webtrader_app.engine:
            web_engine = webtrader_app.engine
            print("WebEngine found:", type(web_engine))
            print("WebEngine methods:", [method for method in dir(web_engine) if not method.startswith('_')])

            # Try to start the server
            if hasattr(web_engine, 'start'):
                print("Starting web server on default port...")
                web_engine.start()
            elif hasattr(web_engine, 'run'):
                print("Running web server...")
                web_engine.run()

        # Keep the engine running
        print("Server should be running. Press Ctrl+C to stop...")
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
    else:
        print("Failed to load WebTrader app")
        print("Available apps:", list(main_engine.apps.keys()))

if __name__ == "__main__":
    main()