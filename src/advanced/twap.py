"""
TWAP (Time-Weighted Average Price) order
Usage:
python src/advanced/twap_orders.py BTCUSDT BUY 0.01 10 5 --testnet
Splits total 0.01 into 10 smaller market orders every 5 seconds
"""
import argparse, time, sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import create_client, logger, log_struct

def twap_order(client, symbol, side, total_qty, chunks, interval, dryrun=False):
    qty_per_order = total_qty / chunks
    for i in range(chunks):
        log_struct(logger, "info", {"action": "TWAP_order", "chunk": i+1, "qty": qty_per_order})
        if not dryrun and client:
            client.new_order(symbol=symbol, side=side, type="MARKET", quantity=qty_per_order)
        else:
            print(f"Mock order {i+1}/{chunks}: {qty_per_order}")
        time.sleep(interval)
    print("✅ TWAP Completed.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol")
    parser.add_argument("side", choices=["BUY","SELL"])
    parser.add_argument("total_qty", type=float)
    parser.add_argument("chunks", type=int)
    parser.add_argument("interval", type=float)
    parser.add_argument("--testnet", action="store_true")
    parser.add_argument("--dryrun", action="store_true")
    args = parser.parse_args()

    client = create_client(testnet=args.testnet)
    twap_order(client, args.symbol, args.side, args.total_qty, args.chunks, args.interval, args.dryrun)

if __name__ == "__main__":
    main()
