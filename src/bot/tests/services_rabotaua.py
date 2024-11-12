from rich import print
from bot.services.rabotaua import RabotaUAParser


async def test():
    service = RabotaUAParser()

    response = await service.search()
    print(response)
