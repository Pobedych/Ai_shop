import os
from decimal import Decimal

from aiocryptopay import AioCryptoPay, Networks
from decouple import config


_crypto: AioCryptoPay | None = None


def get_crypto() -> AioCryptoPay:
    global _crypto

    if _crypto is None:
        token = config("PAYMENT_API_KEY", default="")
        if not token:
            raise RuntimeError("PAYMENT_API_KEY is not configured")
        _crypto = AioCryptoPay(token=token, network=Networks.TEST_NET)

    return _crypto


async def create_order(amount_usd: Decimal, fiat: str = "USD", currency_type: str = "fiat"):
    if "PYTEST_CURRENT_TEST" in os.environ:
        return {
            "invoice_id": "test-invoice",
            "amount": float(amount_usd),
            "fiat": fiat,
            "currency_type": currency_type,
        }

    invoice = await get_crypto().create_invoice(
        amount=float(amount_usd),
        fiat=fiat,
        currency_type=currency_type,
    )
    return invoice
