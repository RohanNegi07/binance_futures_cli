"""
Limit order CLI
Usage:
python src/limit_orders.py --symbol BTCUSDT --side SELL --quantity 0.001 --price 70000 --testnet
"""
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))

from utils import create_client, logger, log_struct, validate_symbol

def place_limit_order(client, symbol, side, quantity, price, timeInForce="GTC", dryrun=False):
    payload = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "quantity": quantity,
        "price": str(price),
        "timeInForce": timeInForce
    }
    log_struct(logger, "info", {"action": "placing_limit_order", "payload": payload})
    if dryrun or client is None:
        return {"mock": True, "status": "NEW", "price": price}
    return client.new_order(**payload)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True, choices=["BUY","SELL"])
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--price", required=True, type=float)
    parser.add_argument("--testnet", action="store_true")
    parser.add_argument("--dryrun", action="store_true")
    args = parser.parse_args()

    client = create_client(testnet=args.testnet)
    resp = place_limit_order(client, args.symbol, args.side, args.quantity, args.price, dryrun=args.dryrun)
    print("Order response:", resp)

if __name__ == "__main__":
    main()
