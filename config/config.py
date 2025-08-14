"""Configuration module for the trading bot."""
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Telegram
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "PUT_YOUR_TELEGRAM_TOKEN_HERE")

# Bybit API keys
BYBIT_API_KEY: str = os.getenv("BYBIT_API_KEY", "")
BYBIT_API_SECRET: str = os.getenv("BYBIT_API_SECRET", "")

# Default timeframes to scan
TIMEFRAMES = ["5m", "15m", "30m", "1h", "4h", "1d"]

# Model settings
MODEL_THRESHOLD: float = float(os.getenv("MODEL_THRESHOLD", "0.5"))

# Database path
DATA_PATH = Path(__file__).resolve().parent.parent / "storage"
DB_FILE = DATA_PATH / "bot.db"

