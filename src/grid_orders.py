import argparse
from utils import create_client, logger

parser = argparse.ArgumentParser()
parser.add_argument("--symbol", required=True)
parser.add_argument("--lower", type=float, required=True)
parser.add_argument("--upper", type=float, required=True)
parser.add_argument("--steps", type=int, required=True)
parser.add_argument("--quantity", type=float, required=True)
parser.add_argument("--side", choices=["BUY", "SELL"], required=True)
parser.add_argument("--testnet", action="store_true")
args = parser.parse_args()

client = create_client(testnet=args.testnet)

def grid_strategy(symbol, lower, upper, steps, quantity, side):
    price_levels = [lower + i * (upper - lower) / steps for i in range(steps + 1)]
    for price in price_levels:
        try:
            order = client.new_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                price=round(price, 2),
                quantity=quantity,
                timeInForce="GTC"
            )
            print(f"✅ Grid Order at {price}:", order["orderId"])
            logger.info(f"Grid Order Placed: {order}")
        except Exception as e:
            print(f"❌ Failed at {price}: {e}")
            logger.error(f"Grid Order failed at {price}: {e}")

grid_strategy(args.symbol, args.lower, args.upper, args.steps, args.quantity, args.side)
