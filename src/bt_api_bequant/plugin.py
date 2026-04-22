from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bt_api_base.plugins.protocol import PluginInfo

from bt_api_bequant import __version__
from bt_api_bequant.registry_registration import register_bequant

if TYPE_CHECKING:
    from bt_api_base.registry import ExchangeRegistry


def get_plugin_info() -> PluginInfo:
    return PluginInfo(
        name="bt_api_bequant",
        version=__version__,
        core_requires=">=0.15,<1.0",
        supported_exchanges=("BEQUANT___SPOT",),
        supported_asset_types=("SPOT",),
        plugin_module="bt_api_bequant.plugin",
    )


def register_plugin(registry: ExchangeRegistry, runtime_factory: Any) -> PluginInfo:
    del runtime_factory
    register_bequant(registry)
    return get_plugin_info()
