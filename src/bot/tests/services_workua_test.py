from rich import print
from bot.services.workua.parser import WorkUAParser


async def test():
    service = WorkUAParser()
    response = await service.search("")
    print(response)
