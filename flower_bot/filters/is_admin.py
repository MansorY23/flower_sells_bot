from aiogram.filters import Filter
from aiogram.types import Message


class IsAdminFilter(Filter):

    def __init__(self):
        self.admin_ids = None

    async def __call__(self, message: Message, admin_ids: list) -> bool:
        return message.from_user.id in admin_ids