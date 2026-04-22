from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.bars.bar import BarData
from bt_api_base.functions.utils import from_dict_get_float


class BeQuantBarData(BarData):
    def __init__(
        self,
        bar_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        period: str | None = None,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(bar_info, has_been_json_encoded)
        self.exchange_name = "BEQUANT"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.period = period
        self.bar_data = bar_info if has_been_json_encoded else None
        self.open_time: int | float = 0
        self.open_price: int | float = 0.0
        self.high_price: int | float = 0.0
        self.low_price: int | float = 0.0
        self.close_price: int | float = 0.0
        self.volume: int | float = 0.0
        self.has_been_init_data = False

    def init_data(self) -> BeQuantBarData:
        if not self.has_been_json_encoded:
            self.bar_data = (
                json.loads(self.bar_info) if isinstance(self.bar_info, str) else self.bar_info
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.bar_data, dict):
            data = self.bar_data
            self.open_time = int(from_dict_get_float(data, "t", 0.0) or 0)
            self.open_price = float(from_dict_get_float(data, "o", 0.0) or 0.0)
            self.high_price = float(from_dict_get_float(data, "h", 0.0) or 0.0)
            self.low_price = float(from_dict_get_float(data, "l", 0.0) or 0.0)
            self.close_price = float(from_dict_get_float(data, "c", 0.0) or 0.0)
            self.volume = float(from_dict_get_float(data, "v", 0.0) or 0.0)
        elif isinstance(self.bar_data, list) and len(self.bar_data) >= 5:
            self.open_time = int(self.bar_data[0])
            self.open_price = float(self.bar_data[1])
            self.high_price = float(self.bar_data[2])
            self.low_price = float(self.bar_data[3])
            self.close_price = float(self.bar_data[4])
            if len(self.bar_data) > 5:
                self.volume = float(self.bar_data[5])

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_symbol_name(self) -> str:
        return self.symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_server_time(self) -> float | int | None:
        return None

    def get_local_update_time(self) -> float | int | None:
        return self.local_update_time

    def get_open_time(self) -> int | float:
        self.init_data()
        return self.open_time

    def get_open_price(self) -> int | float:
        self.init_data()
        return self.open_price

    def get_high_price(self) -> int | float:
        self.init_data()
        return self.high_price

    def get_low_price(self) -> int | float:
        self.init_data()
        return self.low_price

    def get_close_price(self) -> int | float:
        self.init_data()
        return self.close_price

    def get_volume(self) -> int | float:
        self.init_data()
        return self.volume

    def get_amount(self) -> int | float:
        return 0.0

    def get_close_time(self) -> int | float:
        return self.get_open_time()

    def get_quote_asset_volume(self) -> int | float:
        return 0.0

    def get_base_asset_volume(self) -> int | float:
        return self.get_volume()

    def get_num_trades(self) -> int:
        return 0

    def get_taker_buy_base_asset_volume(self) -> int | float:
        return 0.0

    def get_taker_buy_quote_asset_volume(self) -> int | float:
        return 0.0

    def get_bar_status(self) -> bool | int:
        return True

    def get_all_data(self) -> dict[str, Any]:
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "symbol_name": self.symbol_name,
            "asset_type": self.asset_type,
            "period": self.period,
            "local_update_time": self.local_update_time,
            "open_time": self.open_time,
            "open_price": self.open_price,
            "high_price": self.high_price,
            "low_price": self.low_price,
            "close_price": self.close_price,
            "volume": self.volume,
        }

    def __str__(self) -> str:
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()


class BeQuantRequestBarData(BeQuantBarData):
    pass


class BeQuantWssBarData(BeQuantBarData):
    pass


__all__ = ["BeQuantBarData", "BeQuantRequestBarData", "BeQuantWssBarData"]
