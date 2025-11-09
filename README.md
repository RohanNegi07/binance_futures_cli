# Binance Futures CLI Trading Bot

A Python-powered Command-Line Interface (CLI) for trading on Binance Futures (UMFutures).
Supports Market, Limit, Stop-Limit, OCO, and TWAP orders with Testnet and Live Trading modes.

Built with a modular structure for scalability and automation — perfect for developers, traders, and AI-integrated trading systems.

# Features

Supports both Testnet (sandbox) and Live Binance Futures environments
Place Market, Limit, Stop-Limit, OCO, and TWAP (time-weighted) orders
Structured logging for tracking all actions in bot.log
Dry-run mode for safe testing without sending real trades
Modular file structure for custom bot extension or automation
Environment variable support via .env file for API key management
Clean error handling and user feedback

# Project Structure
binance_futures_cli/
│
├── .env
├── bot.log
├── README.md
├── requirements.txt
│
├── src/
│   ├── utils.py
│   ├── market_orders.py
│   ├── limit_orders.py
│   ├── grid_orders.py
│   ├── test_connection.py
│   │
│   └── advanced/
│       ├── stop_limit_orders.py
│       ├── oco_orders.py
│       ├── twap_orders.py
│
└── venv/  (optional virtual environment)

# Setup Instructions
1️⃣ Clone Repository
git clone https://github.com/<your-username>/binance-futures-cli.git
cd binance-futures-cli

2️⃣ Create and Activate Virtual Environment
python -m venv venv
# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a .env file in the project root with:

BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret


# Tip:
You can get your API key & secret from
Binance Testnet
 or
Binance Official API Management

# Test Your Connection
To Binance Testnet:
python src/test_connection.py --testnet


Expected Output:

# API Key is valid and authorized for trading.
Can trade: True, Account type: FUTURES

 -Commands
 Market Order
python src/market_orders.py --symbol BTCUSDT --side BUY --quantity 0.001 --testnet

 -Limit Order
python src/limit_orders.py --symbol BTCUSDT --side SELL --quantity 0.001 --price 70000 --testnet

 -Stop-Limit Order
python src/advanced/stop_limit_orders.py BTCUSDT BUY 0.001 68000 68500 --testnet

 -OCO (One-Cancels-the-Other) Order
python src/advanced/oco_orders.py BTCUSDT SELL 0.001 70000 67000 --testnet

 -TWAP (Time-Weighted Average Price) Order

Split 0.01 BTC into 10 trades every 5 seconds:

python src/advanced/twap_orders.py BTCUSDT BUY 0.01 10 5 --testnet

# Dry Run Mode (No Real Trades)

Test logic without sending orders:

python src/limit_orders.py --symbol BTCUSDT --side BUY --quantity 0.001 --price 68000 --dryrun


Output:

Order response: {'mock': True, 'status': 'NEW', 'price': 68000}

# Logging

All actions are logged in bot.log with timestamps and structured data:

2025-11-08 14:22:01 - INFO - action: placing_limit_order | symbol: BTCUSDT | side: BUY | price: 68000
2025-11-08 14:22:02 - INFO - action: placing_stop_limit | stopPrice: 68500

# Requirements

Install dependencies via:

pip install -r requirements.txt

Example requirements.txt
python-binance==1.0.19
python-dotenv==1.0.1
apscheduler==3.10.4
requests
websocket-client
tzlocal
urllib3

# Example Usage
- Direct Run
python src/advanced/stop_limit_orders.py BTCUSDT BUY 0.001 68000 68500 --testnet

- Module Run (Preferred for packages)
python -m src.advanced.stop_limit_orders BTCUSDT BUY 0.001 68000 68500 --testnet

# Extend This Project

You can easily add:

Custom indicators (EMA, RSI)

Auto grid bots

Machine Learning trade signals

Telegram/Discord alerts

Backtesting mode

Add new scripts under src/advanced/ or extend utils.py for shared tools.