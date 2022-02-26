import pytest_asyncio
import pytest

import asyncio
from tortoise import Tortoise
from settings import TORTOISE_ORM_TEST


# function: the default scope, the fixture is destroyed at the end of the test.
# class: the fixture is destroyed during teardown of the last test in the class.
# module: the fixture is destroyed during teardown of the last test in the module.
# package: the fixture is destroyed during teardown of the last test in the package.
# session: the fixture is destroyed at the end of the test session.
@pytest_asyncio.fixture(scope="module", autouse=True)
async def init():
    await Tortoise.init(
        config=TORTOISE_ORM_TEST
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope="module")
def event_loop():
    return asyncio.get_event_loop()
