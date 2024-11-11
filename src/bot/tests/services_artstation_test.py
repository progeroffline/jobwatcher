from rich import print
from bot.services.artstation import ArtStationParser


async def test():
    service = ArtStationParser()
    response = await service.search(size=30)
    print(response)
