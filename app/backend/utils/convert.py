import httpx


async def converted_currency(base: str, quote: str, amount: float = 1.0) -> dict:
    base = base.upper()
    quote = quote.upper()

    url = f"https://open.er-api.com/v6/latest/{base}"

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()

    if data.get("result") != "success" or quote not in data.get("rates", {}):
        raise ValueError(f"Cannot convert {base} to {quote}")

    rate = float(data["rates"][quote])
    converted = round(amount * rate, 2)

    return converted
