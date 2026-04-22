from __future__ import annotations

from bt_api_base.balance_utils import nested_balance_handler as _bequant_balance_handler
from bt_api_base.registry import ExchangeRegistry

from bt_api_bequant.exchange_data import BeQuantExchangeDataSpot
from bt_api_bequant.feeds.live_bequant.spot import BeQuantRequestDataSpot


def register_bequant(registry: ExchangeRegistry | type[ExchangeRegistry]) -> None:
    registry.register_feed("BEQUANT___SPOT", BeQuantRequestDataSpot)
    registry.register_exchange_data("BEQUANT___SPOT", BeQuantExchangeDataSpot)
    registry.register_balance_handler("BEQUANT___SPOT", _bequant_balance_handler)


def register(registry: ExchangeRegistry | None = None) -> None:
    if registry is None:
        register_bequant(ExchangeRegistry)
        return
    register_bequant(registry)
