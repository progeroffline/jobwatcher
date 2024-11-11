from rich import print
from bot.services.olx import OlxParser


async def test():
    service = OlxParser()

    for i in range(10):
        response = await service.search("developer", page=i + 1)
        print(response)
