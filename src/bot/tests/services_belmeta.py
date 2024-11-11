from rich import print
from bot.services.belmeta import BelmetaParser


async def test():
    service = BelmetaParser()

    for i in range(10):
        response = await service.search(page=i + 1)
        print(response)
