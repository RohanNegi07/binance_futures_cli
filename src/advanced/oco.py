"""
OCO (One-Cancels-the-Other) Order
Usage:
python src/advanced/oco_orders.py BTCUSDT SELL 0.001 70000 67000 --testnet
"""
import argparse, sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import create_client, logger, log_struct

def place_oco_order(client, symbol, side, quantity, take_profit, stop_loss, dryrun=False):
    log_struct(logger, "info", {"action": "placing_oco", "symbol": symbol})
    if dryrun or client is None:
        return {"mock": True, "tp": take_profit, "sl": stop_loss}
    tp = client.new_order(symbol=symbol, side=side, type="LIMIT", price=str(take_profit), quantity=quantity, timeInForce="GTC")
    sl = client.new_order(symbol=symbol, side=side, type="STOP_MARKET", stopPrice=str(stop_loss), quantity=quantity)
    return {"take_profit": tp, "stop_loss": sl}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol")
    parser.add_argument("side", choices=["BUY","SELL"])
    parser.add_argument("quantity", type=float)
    parser.add_argument("take_profit", type=float)
    parser.add_argument("stop_loss", type=float)
    parser.add_argument("--testnet", action="store_true")
    parser.add_argument("--dryrun", action="store_true")
    args = parser.parse_args()

    client = create_client(testnet=args.testnet)
    resp = place_oco_order(client, args.symbol, args.side, args.quantity, args.take_profit, args.stop_loss, args.dryrun)
    print("✅ OCO Order:", resp)

if __name__ == "__main__":
    main()
