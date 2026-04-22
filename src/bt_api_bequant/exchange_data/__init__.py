from __future__ import annotations

from bt_api_base.containers.exchanges.exchange_data import ExchangeData

_FALLBACK_REST_PATHS = {
    "get_server_time": "GET /public/time",
    "get_exchange_info": "GET /public/symbol",
    "get_tick": "GET /public/ticker/{symbol}",
    "get_tick_all": "GET /public/ticker",
    "get_depth": "GET /public/orderbook/{symbol}",
    "get_trades": "GET /public/trades/{symbol}",
    "get_kline": "GET /public/candles/{symbol}",
    "make_order": "POST /spot/order",
    "cancel_order": "DELETE /spot/order/{client_order_id}",
    "cancel_all_orders": "DELETE /spot/order",
    "get_open_orders": "GET /spot/order",
    "query_order": "GET /spot/order/{client_order_id}",
    "get_balance": "GET /spot/balance",
    "get_account": "GET /spot/balance",
}


class BeQuantExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "BEQUANT___SPOT"
        self.rest_url = "https://api.bequant.io/api/3"
        self.wss_url = "wss://api.bequant.io/api/3/ws/public"
        self.rest_paths = dict(_FALLBACK_REST_PATHS)
        self.wss_paths = {}
        self.kline_periods = {
            "1m": "M1",
            "3m": "M3",
            "5m": "M5",
            "15m": "M15",
            "30m": "M30",
            "1h": "H1",
            "4h": "H4",
            "1d": "D1",
            "1w": "D7",
            "1M": "1M",
        }
        self.legal_currency = ["USDT", "USD", "BTC", "ETH", "EUR"]

    def get_symbol(self, symbol: str) -> str:
        return symbol.upper().replace("/", "").replace("-", "").replace("_", "")

    def get_period(self, key: str) -> str:
        return self.kline_periods.get(key, key)

    def get_rest_path(self, key: str, **kwargs) -> str:
        if key not in self.rest_paths or self.rest_paths[key] == "":
            raise ValueError(f"[{self.exchange_name}] REST path not found: {key}")
        return self.rest_paths[key]


class BeQuantExchangeDataSpot(BeQuantExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "SPOT"
