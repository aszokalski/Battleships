import pytest
import os


@pytest.fixture(scope="session", autouse=True)
def do_something(request):
    try:
        os.remove("app/configs/user_config.json")
    except FileNotFoundError:
        pass
