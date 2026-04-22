from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.orderbooks.orderbook import OrderBookData


def _normalize_levels(raw_levels: Any) -> tuple[list[float], list[float]]:
    prices: list[float] = []
    volumes: list[float] = []
    if not isinstance(raw_levels, list):
        return prices, volumes

    for level in raw_levels:
        if isinstance(level, dict):
            price = level.get("price", level.get("0", 0.0))
            volume = level.get("size", level.get("quantity", level.get("1", 0.0)))
        elif isinstance(level, (list, tuple)) and len(level) >= 2:
            price, volume = level[0], level[1]
        else:
            continue
        prices.append(float(price))
        volumes.append(float(volume))
    return prices, volumes


class BeQuantOrderBookData(OrderBookData):
    def __init__(
        self,
        orderbook_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(orderbook_info, has_been_json_encoded)
        self.exchange_name = "BEQUANT"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.has_been_init_data = False

    def init_data(self) -> BeQuantOrderBookData:
        if not self.has_been_json_encoded:
            self.order_book_data = (
                json.loads(self.order_book_info)
                if isinstance(self.order_book_info, str)
                else self.order_book_info
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        payload = self.order_book_data if isinstance(self.order_book_data, dict) else {}
        self.order_book_symbol_name = str(payload.get("symbol", self.symbol_name))
        bids = payload.get("bid", payload.get("bids", []))
        asks = payload.get("ask", payload.get("asks", []))
        self.bid_price_list, self.bid_volume_list = _normalize_levels(bids)
        self.ask_price_list, self.ask_volume_list = _normalize_levels(asks)

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return str(self.exchange_name)

    def get_local_update_time(self) -> float | None:
        return self.local_update_time

    def get_symbol_name(self) -> str:
        return str(self.symbol_name)

    def get_asset_type(self) -> str:
        return str(self.asset_type)

    def get_server_time(self) -> float | None:
        return self.server_time

    def get_bid_price_list(self) -> list[float] | None:
        self.init_data()
        return self.bid_price_list

    def get_ask_price_list(self) -> list[float] | None:
        self.init_data()
        return self.ask_price_list

    def get_bid_volume_list(self) -> list[float] | None:
        self.init_data()
        return self.bid_volume_list

    def get_ask_volume_list(self) -> list[float] | None:
        self.init_data()
        return self.ask_volume_list

    def get_bid_trade_nums(self) -> list[int] | None:
        return self.bid_trade_nums

    def get_ask_trade_nums(self) -> list[int] | None:
        return self.ask_trade_nums

    def __str__(self) -> str:
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()


class BeQuantRequestOrderBookData(BeQuantOrderBookData):
    pass


class BeQuantWssOrderBookData(BeQuantOrderBookData):
    pass


__all__ = [
    "BeQuantOrderBookData",
    "BeQuantRequestOrderBookData",
    "BeQuantWssOrderBookData",
]
