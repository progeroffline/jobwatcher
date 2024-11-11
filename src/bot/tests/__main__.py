import asyncio
from . import (
    services_artstation,
    services_workua,
    services_jobsua,
    services_rabotaua,
    services_olx,
)


async def run_tests():
    # await services_artstation.test()
    # await services_workua.test()
    # await services_jobsua.test()
    # await services_rabotaua.test()
    await services_olx.test()


if __name__ == "__main__":
    asyncio.run(run_tests())
