import pytest
from fastapi.testclient import TestClient
from typing import Generator
from tortoise.contrib.test import finalizer, initializer

from main import test_app as app
from settings import TORTOISE_ORM_TEST
from tests.shortcuts import Client


@pytest.fixture
def client() -> Generator:
    initializer(
        TORTOISE_ORM_TEST['apps']['models']['models'],
        TORTOISE_ORM_TEST['connections']['default']
    )
    with TestClient(app) as client:
        yield Client(client)
    finalizer()
