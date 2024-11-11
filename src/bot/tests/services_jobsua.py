from rich import print
from bot.services.jobsua import JobsUAParser


async def test():
    service = JobsUAParser()

    for i in range(10):
        response = await service.search("developer", page=i + 1)
        print(response)
