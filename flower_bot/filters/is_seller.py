from aiogram.filters import Filter
from aiogram.types import Message


class IsSellerFilter(Filter):

    def __init__(self):
        self.seller_ids = None

    async def __call__(self, message: Message, seller_ids: list) -> bool:
        return message.from_user.id in seller_ids