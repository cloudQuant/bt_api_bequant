from __future__ import annotations

from typing import Any

from bt_api_base.error import ErrorCategory, ErrorTranslator, UnifiedError, UnifiedErrorCode


class BeQuantErrorTranslator(ErrorTranslator):
    @classmethod
    def translate(cls, raw_error: dict[str, Any], venue: str) -> UnifiedError | None:
        message = str(raw_error.get("message", raw_error.get("error", "")))
        lower = message.lower()
        code = raw_error.get("code", raw_error.get("errorCode"))

        if code in (401, 403) or "auth" in lower or "api key" in lower or "signature" in lower:
            error_code = UnifiedErrorCode.INVALID_SIGNATURE
            category = ErrorCategory.AUTH
        elif code == 429 or "rate" in lower or "too many requests" in lower:
            error_code = UnifiedErrorCode.RATE_LIMIT_EXCEEDED
            category = ErrorCategory.RATE_LIMIT
        elif code == 404 or "not found" in lower:
            error_code = UnifiedErrorCode.ORDER_NOT_FOUND
            category = ErrorCategory.BUSINESS
        elif code == 20001 or "symbol" in lower:
            error_code = UnifiedErrorCode.INVALID_SYMBOL
            category = ErrorCategory.BUSINESS
        elif code == 20002 or "balance" in lower or "insufficient" in lower:
            error_code = UnifiedErrorCode.INSUFFICIENT_BALANCE
            category = ErrorCategory.BUSINESS
        else:
            error_code = UnifiedErrorCode.INTERNAL_ERROR
            category = ErrorCategory.SYSTEM

        return UnifiedError(
            code=error_code,
            category=category,
            venue=venue,
            message=message or "Unknown error",
            original_error=str(raw_error),
            context={"raw_response": raw_error},
        )


__all__ = ["BeQuantErrorTranslator"]
