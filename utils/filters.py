from aiogram.filters import BaseFilter
from aiogram.types import Message

from utils import data


class IsLogged(BaseFilter):
    def __init__(self) -> None:
        pass
    
    async def __call__(self, message: Message) -> bool:
        return await data.get_logged_user(message.from_user.id)

class IsPDF(BaseFilter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        if message.document:
            if message.document.file_name.endswith(".pdf"):
                return True
        return False