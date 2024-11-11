from rich import print
from bot.services.rabotaua import RabotaUAParser


async def test():
    service = RabotaUAParser()

    for i in range(10):
        response = await service.search("developer", page=i + 1)
        print(response)
