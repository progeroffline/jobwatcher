import asyncio
from . import services_artstation_test, services_workua_test, services_jobsua


async def run_tests():
    # await services_artstation_test.test()
    # await services_workua_test.test()
    await services_jobsua.test()


if __name__ == "__main__":
    asyncio.run(run_tests())
