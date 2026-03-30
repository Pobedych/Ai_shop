import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config

raw_admins = config("ADMINS", default="")
admins = [
    int(admin_id.strip()) for admin_id in raw_admins.split(",") if admin_id.strip()
]

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


bot = Bot(token=config("TOKEN"))
dp = Dispatcher(storage=MemoryStorage())
