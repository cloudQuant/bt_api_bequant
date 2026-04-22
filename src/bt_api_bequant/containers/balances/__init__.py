from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.balances.balance import BalanceData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class BeQuantBalanceData(BalanceData):
    def __init__(
        self,
        balance_info: str | dict[str, Any],
        symbol_name: str | None,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(balance_info, has_been_json_encoded)
        self.exchange_name = "BEQUANT"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.balance_data = balance_info if has_been_json_encoded else None
        self.currency: str | None = symbol_name
        self.available: float | None = None
        self.locked: float | None = None
        self.total: float | None = None
        self.has_been_init_data = False

    def init_data(self) -> BeQuantBalanceData:
        if not self.has_been_json_encoded:
            self.balance_data = (
                json.loads(self.balance_info)
                if isinstance(self.balance_info, str)
                else self.balance_info
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.balance_data, dict):
            data = self.balance_data
            self.currency = from_dict_get_string(data, "currency", self.symbol_name)
            self.available = from_dict_get_float(data, "available", 0.0)
            self.locked = from_dict_get_float(data, "reserved", 0.0)
            self.total = from_dict_get_float(data, "total")
            if self.total is None:
                self.total = float((self.available or 0.0) + (self.locked or 0.0))

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return str(self.exchange_name)

    def get_asset_type(self) -> str:
        return str(self.asset_type)

    def get_all_data(self) -> dict[str, Any]:
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "symbol_name": self.get_symbol_name(),
            "asset_type": self.asset_type,
            "local_update_time": self.local_update_time,
            "available": self.available,
            "locked": self.locked,
            "total": self.total,
        }

    def get_server_time(self) -> float | None:
        return None

    def get_local_update_time(self) -> float | None:
        return float(self.local_update_time)

    def get_account_id(self) -> str | None:
        return None

    def get_account_type(self) -> str | None:
        return None

    def get_fee_tier(self) -> int | str | None:
        return None

    def get_max_withdraw_amount(self) -> float | None:
        return None

    def get_margin(self) -> float | None:
        self.init_data()
        return self.total

    def get_used_margin(self) -> float | None:
        self.init_data()
        return self.locked

    def get_maintain_margin(self) -> float | None:
        return None

    def get_available_margin(self) -> float | None:
        self.init_data()
        return self.available

    def get_open_order_initial_margin(self) -> float | None:
        return None

    def get_open_order_maintenance_margin(self) -> float | None:
        return None

    def get_unrealized_profit(self) -> float | None:
        return 0.0

    def get_interest(self) -> float | None:
        return None

    def get_symbol_name(self) -> str | None:
        self.init_data()
        return self.currency

    def get_available(self) -> float | None:
        self.init_data()
        return self.available

    def get_locked(self) -> float | None:
        self.init_data()
        return self.locked

    def get_total(self) -> float | None:
        self.init_data()
        return self.total

    def __str__(self) -> str:
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()


class BeQuantRequestBalanceData(BeQuantBalanceData):
    pass


class BeQuantWssBalanceData(BeQuantBalanceData):
    pass


__all__ = [
    "BeQuantBalanceData",
    "BeQuantRequestBalanceData",
    "BeQuantWssBalanceData",
]
