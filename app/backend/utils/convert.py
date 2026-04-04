from decimal import Decimal, ROUND_HALF_UP

import httpx


async def converted_currency(
    base: str, quote: str, amount: Decimal | int | float = 1.0
) -> float:
    base = base.upper()
    quote = quote.upper()

    url = f"https://open.er-api.com/v6/latest/{base}"

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()

    if data.get("result") != "success" or quote not in data.get("rates", {}):
        raise ValueError(f"Cannot convert {base} to {quote}")

    decimal_amount = amount if isinstance(amount, Decimal) else Decimal(str(amount))
    rate = Decimal(str(data["rates"][quote]))
    converted = (decimal_amount * rate).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    return float(converted)


