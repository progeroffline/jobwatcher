import asyncio
from . import services_artstation_test, services_workua_test


async def run_tests():
    # await services_artstation_test.test()
    await services_workua_test.test()


if __name__ == "__main__":
    asyncio.run(run_tests())
