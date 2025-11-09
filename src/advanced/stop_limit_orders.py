"""
Stop-Limit Order CLI
Usage:
python src/advanced/stop_limit_orders.py BTCUSDT BUY 0.001 68000 68500 --testnet
"""
import argparse, sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils import create_client, logger, log_struct

def place_stop_limit_order(client, symbol, side, quantity, stop_price, limit_price, dryrun=False):
    payload = {
        "symbol": symbol,
        "side": side,
        "type": "STOP_MARKET",
        "quantity": quantity,
        "stopPrice": str(stop_price),
        "priceProtect": "TRUE"
    }
    log_struct(logger, "info", {"action": "placing_stop_limit", "payload": payload})
    if dryrun or client is None:
        return {"mock": True, "stopPrice": stop_price, "limitPrice": limit_price}
    return client.new_order(**payload)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol")
    parser.add_argument("side", choices=["BUY", "SELL"])
    parser.add_argument("quantity", type=float)
    parser.add_argument("stop_price", type=float)
    parser.add_argument("limit_price", type=float)
    parser.add_argument("--testnet", action="store_true")
    parser.add_argument("--dryrun", action="store_true")
    args = parser.parse_args()

    client = create_client(testnet=args.testnet)
    resp = place_stop_limit_order(client, args.symbol, args.side, args.quantity, args.stop_price, args.limit_price, args.dryrun)
    print("Order result:", resp)

if __name__ == "__main__":
    main()
