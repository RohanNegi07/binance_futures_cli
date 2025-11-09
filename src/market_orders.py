"""
Market order CLI
Usage:
python src/market_orders.py --symbol BTCUSDT --side BUY --quantity 0.001 --testnet
"""
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))

from utils import create_client, logger, log_struct, validate_symbol, get_symbol_filters

def validate_inputs(client, symbol, quantity):
    if quantity <= 0:
        raise ValueError("Quantity must be > 0")
    if client:
        info = client.exchange_info()
        if not validate_symbol(info, symbol):
            raise ValueError("Invalid symbol")
    return True

def place_market_order(client, symbol, side, quantity, dryrun=False):
    payload = {"symbol": symbol, "side": side, "type": "MARKET", "quantity": quantity}
    log_struct(logger, "info", {"action": "placing_market_order", "payload": payload})
    if dryrun or client is None:
        return {"mock": True, "status": "FILLED", "quantity": quantity}
    return client.new_order(**payload)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True, choices=["BUY","SELL"])
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--testnet", action="store_true")
    parser.add_argument("--dryrun", action="store_true")
    args = parser.parse_args()

    client = create_client(testnet=args.testnet)
    validate_inputs(client, args.symbol, args.quantity)
    resp = place_market_order(client, args.symbol, args.side, args.quantity, args.dryrun)
    print("Order response:", resp)

if __name__ == "__main__":
    main()
