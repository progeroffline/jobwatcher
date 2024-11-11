from rich import print
from bot.services.artstation import ArtStationParser


async def test():
    service = ArtStationParser()

    for i in range(10):
        response = await service.search(page=i + 1)
        print(response)
