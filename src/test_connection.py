# src/test_connection.py
"""
Test connection to Binance Futures (testnet or mock).
Usage:
    python src/test_connection.py --testnet
    python src/test_connection.py          # runs in live mode
"""

import argparse
from utils import create_client, logger, log_struct

def test_connection(testnet=False):
    """Check Binance Futures connection."""
    client = create_client(testnet)

    if client is None:
        print("⚠️ Running in mock mode — no valid API keys or client connection.")
        return

    try:
        info = client.exchange_info()
        symbols = len(info.get("symbols", []))
        print(f"✅ Connection successful! Exchange symbols available: {symbols}")
        log_struct(logger, "info", {"action": "test_connection_success", "symbols_count": symbols})
    except Exception as e:
        print("❌ Connection failed:", e)
        log_struct(logger, "error", {"action": "test_connection_failed", "error": str(e)})


def main():
    parser = argparse.ArgumentParser(description="Test Binance Futures API connection.")
    parser.add_argument("--testnet", action="store_true", help="Use Binance Futures Testnet.")
    args = parser.parse_args()

    test_connection(testnet=args.testnet)


if __name__ == "__main__":
    main()
