# content of conftest.py or a tests file (e.g. in your tests or root directory)
import pytest
import os


@pytest.fixture(scope="session", autouse=True)
def do_something(request):
    try:
        os.remove("app/configs/user_config.json")
    except FileNotFoundError:
        pass
    # prepare something ahead of all tests
    # request.addfinalizer(finalizer_function)
