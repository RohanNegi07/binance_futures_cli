# src/cancel_order.py
"""
Cancel a specific or all open orders on Binance Futures.

Usage examples:
    # Cancel one order by ID
    python src/cancel_order.py BTCUSDT --order_id 123456789 --testnet

    # Cancel all open orders for a symbol
    python src/cancel_order.py BTCUSDT --all --testnet

    # Dry run (no real cancel)
    python src/cancel_order.py BTCUSDT --all --testnet --dryrun
"""

import argparse
from utils import create_client, logger, log_struct

def cancel_order(symbol, order_id=None, cancel_all=False, testnet=False, dryrun=False):
    """Cancel specific or all open orders."""
    client = create_client(testnet)

    if client is None:
        print("⚠️ No valid Binance client. Check your API keys or network connection.")
        return

    if dryrun:
        action = "Cancel ALL" if cancel_all else f"Cancel order {order_id}"
        print(f"🧪 Dry Run Mode: Would {action} for {symbol}")
        log_struct(logger, "info", {
            "action": "cancel_order_dryrun",
            "symbol": symbol,
            "order_id": order_id,
            "cancel_all": cancel_all,
            "testnet": testnet
        })
        return

    try:
        if cancel_all:
            response = client.cancel_all_open_orders(symbol=symbol)
            print(f"✅ All open orders for {symbol} canceled successfully.")
            log_struct(logger, "info", {
                "action": "cancel_all_orders_success",
                "symbol": symbol,
                "response": response
            })
        else:
            if not order_id:
                print("❌ Error: You must provide an order_id unless using --all")
                return
            response = client.cancel_order(symbol=symbol, orderId=order_id)
            print(f"✅ Order {order_id} for {symbol} canceled successfully.")
            log_struct(logger, "info", {
                "action": "cancel_order_success",
                "symbol": symbol,
                "order_id": order_id,
                "response": response
            })
    except Exception as e:
        print("❌ Error canceling order:", e)
        log_struct(logger, "error", {"action": "cancel_order_failed", "error": str(e)})


def main():
    parser = argparse.ArgumentParser(description="Cancel orders on Binance Futures.")
    parser.add_argument("symbol", type=str, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--order_id", type=int, help="Order ID to cancel.")
    parser.add_argument("--all", action="store_true", help="Cancel all open orders for the symbol.")
    parser.add_argument("--testnet", action="store_true", help="Use Binance Futures Testnet.")
    parser.add_argument("--dryrun", action="store_true", help="Simulate without executing.")
    args = parser.parse_args()

    cancel_order(
        symbol=args.symbol,
        order_id=args.order_id,
        cancel_all=args.all,
        testnet=args.testnet,
        dryrun=args.dryrun
    )


if __name__ == "__main__":
    main()
