from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.tickers.ticker import TickerData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class BeQuantTickerData(TickerData):
    def __init__(
        self,
        ticker_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(ticker_info, has_been_json_encoded)
        self.exchange_name = "BEQUANT"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.ticker_data: dict[str, Any] | None = (
            ticker_info if has_been_json_encoded and isinstance(ticker_info, dict) else None
        )
        self.ticker_symbol_name: str | None = None
        self.last_price: float | None = None
        self.bid_price: float | None = None
        self.ask_price: float | None = None
        self.open_24h: float | None = None
        self.high_24h: float | None = None
        self.low_24h: float | None = None
        self.volume_24h: float | None = None
        self.has_been_init_data = False

    def init_data(self) -> BeQuantTickerData:
        if not self.has_been_json_encoded:
            self.ticker_data = (
                json.loads(self.ticker_info) if isinstance(self.ticker_info, str) else {}
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.ticker_data, dict):
            data = self.ticker_data
            self.ticker_symbol_name = from_dict_get_string(data, "symbol", self.symbol_name)
            self.last_price = from_dict_get_float(data, "last")
            self.bid_price = from_dict_get_float(data, "bid")
            self.ask_price = from_dict_get_float(data, "ask")
            self.open_24h = from_dict_get_float(data, "open")
            self.high_24h = from_dict_get_float(data, "high")
            self.low_24h = from_dict_get_float(data, "low")
            self.volume_24h = from_dict_get_float(data, "volume")

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_symbol_name(self) -> str:
        return self.symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_last_price(self) -> float | None:
        self.init_data()
        return self.last_price

    def get_bid_price(self) -> float | None:
        self.init_data()
        return self.bid_price

    def get_ask_price(self) -> float | None:
        self.init_data()
        return self.ask_price

    def get_high(self) -> float | None:
        self.init_data()
        return self.high_24h

    def get_low(self) -> float | None:
        self.init_data()
        return self.low_24h

    def get_volume(self) -> float | None:
        self.init_data()
        return self.volume_24h


class BeQuantRequestTickerData(BeQuantTickerData):
    pass


class BeQuantWssTickerData(BeQuantTickerData):
    pass


__all__ = [
    "BeQuantRequestTickerData",
    "BeQuantTickerData",
    "BeQuantWssTickerData",
]
