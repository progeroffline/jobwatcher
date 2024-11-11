from rich import print
from bot.services.workua.parser import WorkUAParser


async def test():
    service = WorkUAParser()

    for i in range(10):
        response = await service.search("developer", i + 1)
        print(response)
