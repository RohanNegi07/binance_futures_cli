import os
import logging
from dotenv import load_dotenv
from binance.um_futures import UMFutures

load_dotenv()

# -----------------------
# Logger Setup
# -----------------------
def setup_logger():
    logger = logging.getLogger("BinanceBot")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler("bot.log")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

logger = setup_logger()

def log_struct(logger, level, data: dict):
    """Structured log entry"""
    msg = " | ".join(f"{k}: {v}" for k, v in data.items())
    getattr(logger, level, logger.info)(msg)

# -----------------------
# Environment + Validation
# -----------------------
def get_env(var):
    return os.getenv(var)

def create_client(testnet=False):
    api_key = get_env("BINANCE_API_KEY")
    api_secret = get_env("BINANCE_API_SECRET")
    base_url = "https://testnet.binancefuture.com" if testnet else None
    if not api_key or not api_secret:
        logger.warning("API keys not found, running in dryrun mode.")
        return None
    try:
        return UMFutures(key=api_key, secret=api_secret, base_url=base_url)
    except Exception as e:
        log_struct(logger, "error", {"action": "client_creation_failed", "error": str(e)})
        return None

def validate_symbol(info, symbol):
    for sym in info.get("symbols", []):
        if sym["symbol"] == symbol:
            return True
    return False

def get_symbol_filters(info, symbol):
    for sym in info.get("symbols", []):
        if sym["symbol"] == symbol:
            return sym.get("filters", [])
    return []

def round_to_tick(price, tick_size):
    return round(price / tick_size) * tick_size
