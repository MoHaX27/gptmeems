"""Feature engineering utilities for technical indicators."""
from __future__ import annotations

import pandas as pd


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Compute basic technical indicators for the dataframe.

    The function expects a dataframe with columns: ``open``, ``high``,
    ``low``, ``close`` and ``volume``.
    """
    result = df.copy()
    result["ema20"] = df["close"].ewm(span=20).mean()
    result["ema50"] = df["close"].ewm(span=50).mean()
    result["ema200"] = df["close"].ewm(span=200).mean()
    delta = df["close"].diff()
    up, down = delta.clip(lower=0), -delta.clip(upper=0)
    roll_up = up.ewm(span=14).mean()
    roll_down = down.ewm(span=14).mean()
    rs = roll_up / roll_down
    result["rsi"] = 100 - (100 / (1 + rs))
    result["obv"] = ( (df["volume"].where(delta > 0, -df["volume"])) ).cumsum()
    return result
