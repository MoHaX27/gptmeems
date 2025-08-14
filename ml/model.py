"""ML module with LightGBM model for signal prediction.

This module contains a lightweight wrapper around a LightGBM model.  The
implementation is intentionally simplified – training and feature
engineering are represented by placeholders so that the bot can be
extended later without changing public APIs.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

try:  # optional dependency
    import lightgbm as lgb
except Exception:  # pragma: no cover - handled gracefully
    lgb = None  # type: ignore

FEATURES_FILE = Path(__file__).with_name("features_order.json")


class SignalModel:
    """Wrapper around LightGBM model used for signal prediction."""

    def __init__(self) -> None:
        self.model: Optional["lgb.Booster"] = None
        self.features_order = self._load_features_order()

    # ------------------------------------------------------------------
    def _load_features_order(self) -> list[str]:
        if FEATURES_FILE.exists():
            return json.loads(FEATURES_FILE.read_text())
        return []

    def _save_features_order(self, features: Iterable[str]) -> None:
        FEATURES_FILE.write_text(json.dumps(list(features)))

    # ------------------------------------------------------------------
    def train(self, df: pd.DataFrame, label: str = "target") -> None:
        """Train the model on provided dataframe.

        Parameters
        ----------
        df: pandas.DataFrame
            DataFrame containing feature columns and a target label.
        label: str
            Name of the target column.
        """
        if lgb is None:
            raise RuntimeError("LightGBM is not installed")

        features = [c for c in df.columns if c != label]
        train_data = lgb.Dataset(df[features], label=df[label])
        params = {"objective": "binary", "metric": "binary_logloss"}
        self.model = lgb.train(params, train_data)
        self._save_features_order(features)

    # ------------------------------------------------------------------
    def predict(self, df: pd.DataFrame) -> pd.Series:
        """Predict probabilities for provided dataframe."""
        if self.model is None:
            raise RuntimeError("Model is not trained")
        df = df[self.features_order]
        preds = self.model.predict(df)
        return pd.Series(preds, index=df.index)

