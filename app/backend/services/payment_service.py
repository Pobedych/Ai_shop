from aiocryptopay import AioCryptoPay, Networks
from decouple import config
from decimal import Decimal


crypto = AioCryptoPay(token=config('PAYMENT_API_KEY'), network=Networks.TEST_NET)

async def create_order(amount_usd: Decimal, fiat='USD', currency_type='fiat'):
    invoice = await crypto.create_invoice(
        amount=float(amount_usd),
        fiat='USD',
        currency_type='fiat'
    )
    return invoice