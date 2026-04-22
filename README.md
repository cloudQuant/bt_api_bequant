# bt_api_bequant

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_bequant.svg)](https://pypi.org/project/bt_api_bequant/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_bequant.svg)](https://pypi.org/project/bt_api_bequant/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_bequant/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_bequant/actions)
[![Docs](https://readthedocs.org/projects/bt-api-bequant/badge/?version=latest)](https://bt-api-bequant.readthedocs.io/)

---

<!-- English -->
# bt_api_bequant

> **BeQuant exchange plugin for bt_api** — Unified REST and WebSocket API for Spot trading and more.

`bt_api_bequant` is a runtime plugin for [bt_api](https://github.com/cloudQuant/bt_api_py) that connects to **BeQuant** exchange. It depends on [bt_api_base](https://github.com/cloudQuant/bt_api_base) for core infrastructure.

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-bequant.readthedocs.io/ |
| Chinese Docs | https://bt-api-bequant.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_bequant |
| PyPI | https://pypi.org/project/bt_api_bequant/ |
| Issues | https://github.com/cloudQuant/bt_api_bequant/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://github.com/cloudQuant/bt_api_py |

---

## Features

### Supported Asset Types

| Asset Type | Code | REST | WebSocket | Description |
|---|---|---|---|---|
| Spot | `BEQUANT___SPOT` | ✅ | ✅ | Spot trading |

### Dual API Modes

- **REST API** — Synchronous polling for order management, balance queries, historical data
- **WebSocket API** — Real-time streaming for ticker, order book, k-lines, trades, account updates

### Plugin Architecture

Auto-registers at import time via `ExchangeRegistry`. Works seamlessly with `BtApi`:

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BEQUANT___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("BEQUANT___SPOT", "BTCUSDT")
balance = api.get_balance("BEQUANT___SPOT")
order = api.make_order(exchange_name="BEQUANT___SPOT", symbol="BTCUSDT", volume=0.001, price=50000, order_type="limit")
```

### Unified Data Containers

All exchange responses normalized to bt_api_base container types:

- `TickContainer` — 24hr rolling ticker
- `OrderBookContainer` — Order book depth
- `BarContainer` — K-line/candlestick
- `TradeContainer` — Individual trades
- `OrderContainer` — Order status and fills
- `PositionContainer` — Futures/margin positions
- `AccountBalanceContainer` — Asset balances

---

## Installation

### From PyPI (Recommended)

```bash
pip install bt_api_bequant
```

### From Source

```bash
git clone https://github.com/cloudQuant/bt_api_bequant
cd bt_api_bequant
pip install -e .
```

### Requirements

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`
- `requests` for HTTP client
- `websocket-client` for WebSocket client

---

## Quick Start

### 1. Install

```bash
pip install bt_api_bequant
```

### 2. Get ticker (public — no API key needed)

```python
from bt_api_py import BtApi

api = BtApi()
ticker = api.get_tick("BEQUANT___SPOT", "BTCUSDT")
print(f"BTCUSDT price: {ticker.price}")
```

### 3. Place an order (requires API key)

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BEQUANT___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

order = api.make_order(
    exchange_name="BEQUANT___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=50000,
    order_type="limit",
)
print(f"Order placed: {order.id}")
```

### 4. bt_api Plugin Integration

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BEQUANT___SPOT": {"api_key": "key", "secret": "secret"}
})

# REST calls
ticker = api.get_tick("BEQUANT___SPOT", "BTCUSDT")
balance = api.get_balance("BEQUANT___SPOT")

# WebSocket subscription
api.subscribe("BEQUANT___SPOT___BTCUSDT", [
    {"topic": "ticker", "symbol": "BTCUSDT"},
    {"topic": "depth", "symbol": "BTCUSDT", "depth": 20},
])
queue = api.get_data_queue("BEQUANT___SPOT")
msg = queue.get(timeout=10)
```

---

## Architecture

```
bt_api_bequant/
├── plugin.py                     # register_plugin() — bt_api plugin entry point
├── registry_registration.py       # register_bequant() — feeds / exchange_data registration
├── exchange_data/
│   └── bequant_exchange_data.py # BeQuantExchangeData
├── feeds/
│   ├── live_bequant/
│   │   ├── spot.py             # BeQuantRequestDataSpot
│   │   └── request_base.py     # RequestData base class
├── containers/                   # Normalized data container types
├── gateway/
│   └── adapter.py             # BeQuantGatewayAdapter
└── errors/
    └── bequant_translator.py  # BeQuantErrorTranslator → bt_api_base.ApiError
```

---

## Supported Operations

| Category | Operation | Notes |
|---|---|---|
| **Market Data** | `get_ticker` | 24hr rolling ticker |
| | `get_orderbook` | Order book depth |
| | `get_bars` | K-line/candlestick |
| | `get_trades` | Recent trade history |
| **Account** | `get_balance` | All asset balances |
| | `get_position` | Positions |
| | `get_open_orders` | All open orders |
| | `get_order` | Single order by ID |
| **Trading** | `make_order` | LIMIT/MARKET orders |
| | `cancel_order` | Cancel order |
| **WebSocket** | `subscribe_symbols` | Market data streams |
| | `poll_output` | Blocking/non-blocking output poll |

---

## Error Handling

All BeQuant API errors are translated to bt_api_base `ApiError` subclasses.

---

## Documentation

| Doc | Link |
|-----|------|
| **English** | https://bt-api-bequant.readthedocs.io/ |
| **中文** | https://bt-api-bequant.readthedocs.io/zh/latest/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://cloudquant.github.io/bt_api_py/ |

---

## License

MIT — see [LICENSE](LICENSE).

---

## Support

- [GitHub Issues](https://github.com/cloudQuant/bt_api_bequant/issues) — bug reports, feature requests
- Email: yunjinqi@gmail.com

---

---

## 中文

> **bt_api 的 BeQuant 交易所插件** — 为现货交易等提供统一的 REST 和 WebSocket API。

`bt_api_bequant` 是 [bt_api](https://github.com/cloudQuant/bt_api_py) 的运行时插件，连接 **BeQuant** 交易所。依赖 [bt_api_base](https://github.com/cloudQuant/bt_api_base) 提供核心基础设施。

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-bequant.readthedocs.io/ |
| 中文文档 | https://bt-api-bequant.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_bequant |
| PyPI | https://pypi.org/project/bt_api_bequant/ |
| 问题反馈 | https://github.com/cloudQuant/bt_api_bequant/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://github.com/cloudQuant/bt_api_py |

---

## 功能特点

### 支持的资产类型

| 资产类型 | 代码 | REST | WebSocket | 说明 |
|---|---|---|---|---|
| 现货 | `BEQUANT___SPOT` | ✅ | ✅ | 现货交易 |

### 双 API 模式

- **REST API** — 同步轮询：订单管理、余额查询、历史数据
- **WebSocket API** — 实时流：行情、订单簿、K线、交易、账户更新

### 插件架构

通过 `ExchangeRegistry` 在导入时自动注册，与 `BtApi` 无缝协作：

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BEQUANT___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("BEQUANT___SPOT", "BTCUSDT")
balance = api.get_balance("BEQUANT___SPOT")
order = api.make_order(exchange_name="BEQUANT___SPOT", symbol="BTCUSDT", volume=0.001, price=50000, order_type="limit")
```

### 统一数据容器

所有交易所响应规范化为 bt_api_base 容器类型：

- `TickContainer` — 24小时滚动行情
- `OrderBookContainer` — 订单簿深度
- `BarContainer` — K线/蜡烛图
- `TradeContainer` — 逐笔成交
- `OrderContainer` — 订单状态和成交
- `PositionContainer` — 持仓
- `AccountBalanceContainer` — 资产余额

---

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install bt_api_bequant
```

### 从源码安装

```bash
git clone https://github.com/cloudQuant/bt_api_bequant
cd bt_api_bequant
pip install -e .
```

### 系统要求

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`
- `requests` HTTP 客户端
- `websocket-client` WebSocket 客户端

---

## 快速开始

### 1. 安装

```bash
pip install bt_api_bequant
```

### 2. 获取行情（公开接口，无需 API key）

```python
from bt_api_py import BtApi

api = BtApi()
ticker = api.get_tick("BEQUANT___SPOT", "BTCUSDT")
print(f"BTCUSDT 价格: {ticker.price}")
```

### 3. 下单交易（需要 API key）

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BEQUANT___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

order = api.make_order(
    exchange_name="BEQUANT___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=50000,
    order_type="limit",
)
print(f"订单已下单: {order.id}")
```

### 4. bt_api 插件集成

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BEQUANT___SPOT": {"api_key": "key", "secret": "secret"}
})

# REST 调用
ticker = api.get_tick("BEQUANT___SPOT", "BTCUSDT")
balance = api.get_balance("BEQUANT___SPOT")

# WebSocket 订阅
api.subscribe("BEQUANT___SPOT___BTCUSDT", [
    {"topic": "ticker", "symbol": "BTCUSDT"},
    {"topic": "depth", "symbol": "BTCUSDT", "depth": 20},
])
queue = api.get_data_queue("BEQUANT___SPOT")
msg = queue.get(timeout=10)
```

---

## 架构

```
bt_api_bequant/
├── plugin.py                     # register_plugin() — bt_api 插件入口
├── registry_registration.py       # register_bequant() — feeds / exchange_data 注册
├── exchange_data/
│   └── bequant_exchange_data.py # BeQuantExchangeData
├── feeds/
│   ├── live_bequant/
│   │   ├── spot.py             # BeQuantRequestDataSpot
│   │   └── request_base.py     # RequestData 基类
├── containers/                   # 规范化数据容器类型
├── gateway/
│   └── adapter.py             # BeQuantGatewayAdapter
└── errors/
    └── bequant_translator.py  # BeQuantErrorTranslator → bt_api_base.ApiError
```

---

## 支持的操作

| 类别 | 操作 | 说明 |
|---|---|---|
| **行情数据** | `get_ticker` | 24小时滚动行情 |
| | `get_orderbook` | 订单簿深度 |
| | `get_bars` | K线/蜡烛图 |
| | `get_trades` | 近期成交历史 |
| **账户** | `get_balance` | 所有资产余额 |
| | `get_position` | 持仓 |
| | `get_open_orders` | 所有挂单 |
| | `get_order` | 按ID查询单笔订单 |
| **交易** | `make_order` | 限价/市价订单 |
| | `cancel_order` | 撤销订单 |
| **WebSocket** | `subscribe_symbols` | 行情数据流订阅 |
| | `poll_output` | 阻塞/非阻塞输出轮询 |

---

## 错误处理

所有 BeQuant API 错误均翻译为 bt_api_base `ApiError` 子类。

---

## 文档

| 文档 | 链接 |
|-----|------|
| **英文文档** | https://bt-api-bequant.readthedocs.io/ |
| **中文文档** | https://bt-api-bequant.readthedocs.io/zh/latest/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://cloudquant.github.io/bt_api_py/ |

---

## 许可证

MIT — 详见 [LICENSE](LICENSE)。

---

## 技术支持

- [GitHub Issues](https://github.com/cloudQuant/bt_api_bequant/issues) — bug 报告、功能请求
- 邮箱: yunjinqi@gmail.com