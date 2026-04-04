from decimal import Decimal

import httpx
import pytest

from app.backend.utils import convert


class DummyResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self.payload


class DummyAsyncClient:
    def __init__(self, response: DummyResponse) -> None:
        self.response = response
        self.requested_urls: list[str] = []

    async def __aenter__(self) -> "DummyAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None

    async def get(self, url: str) -> DummyResponse:
        self.requested_urls.append(url)
        return self.response


@pytest.mark.asyncio
async def test_converted_currency_returns_rounded_amount(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = DummyAsyncClient(
        DummyResponse({"result": "success", "rates": {"USD": 0.011}})
    )
    monkeypatch.setattr(convert.httpx, "AsyncClient", lambda timeout: client)

    result = await convert.converted_currency("rub", "usd", 150)

    assert result == 1.65
    assert client.requested_urls == ["https://open.er-api.com/v6/latest/RUB"]


@pytest.mark.asyncio
async def test_converted_currency_accepts_decimal_amount(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = DummyAsyncClient(
        DummyResponse({"result": "success", "rates": {"USD": 0.011}})
    )
    monkeypatch.setattr(convert.httpx, "AsyncClient", lambda timeout: client)

    result = await convert.converted_currency("rub", "usd", Decimal("150.00"))

    assert result == 1.65


@pytest.mark.asyncio
async def test_converted_currency_raises_on_missing_quote(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = DummyAsyncClient(
        DummyResponse({"result": "success", "rates": {"EUR": 1.0}})
    )
    monkeypatch.setattr(convert.httpx, "AsyncClient", lambda timeout: client)

    with pytest.raises(ValueError, match="Cannot convert RUB to USD"):
        await convert.converted_currency("rub", "usd", 100)


@pytest.mark.asyncio
async def test_converted_currency_propagates_http_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FailingClient(DummyAsyncClient):
        async def get(self, url: str) -> DummyResponse:
            raise httpx.ConnectError("network down")

    monkeypatch.setattr(
        convert.httpx,
        "AsyncClient",
        lambda timeout: FailingClient(DummyResponse({})),
    )

    with pytest.raises(httpx.ConnectError):
        await convert.converted_currency("rub", "usd", 100)
