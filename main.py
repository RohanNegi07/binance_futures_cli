import os
import sys
import subprocess

MENU = """
==============================
  💹 BINANCE CLI TRADING BOT
==============================

1️⃣  Test Binance Connection
2️⃣  Place Market Order
3️⃣  Place Limit Order
4️⃣  Run Grid Trading Strategy
5️⃣  Exit
------------------------------
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_command(cmd):
    try:
        subprocess.run([sys.executable] + cmd, check=True)
    except Exception as e:
        print("❌ Command failed:", e)

def get_symbol(): return input("Enter symbol (e.g. BTCUSDT): ").upper().strip()
def get_side(): return input("Side (BUY/SELL): ").upper().strip()
def get_float(prompt): return float(input(f"{prompt}: ").strip())

def main():
    while True:
        clear()
        print(MENU)
        choice = input("Select an option: ").strip()
        if choice == "1":
            run_command(["src/test_connection.py", "--testnet"])
        elif choice == "2":
            symbol, side, qty = get_symbol(), get_side(), get_float("Quantity")
            run_command(["src/market_orders.py", "--symbol", symbol, "--side", side, "--quantity", str(qty), "--testnet"])
        elif choice == "3":
            symbol, side, qty, price = get_symbol(), get_side(), get_float("Quantity"), get_float("Limit Price")
            run_command(["src/limit_orders.py", "--symbol", symbol, "--side", side, "--quantity", str(qty), "--price", str(price), "--testnet"])
        elif choice == "4":
            symbol, lower, upper, steps, qty, side = get_symbol(), get_float("Lower price"), get_float("Upper price"), int(get_float("Steps")), get_float("Qty/order"), get_side()
            run_command(["src/grid_orders.py", "--symbol", symbol, "--lower", str(lower), "--upper", str(upper), "--steps", str(steps), "--quantity", str(qty), "--side", side, "--testnet"])
        elif choice == "5":
            print("👋 Goodbye!")
            break
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
