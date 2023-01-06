from utils import (
    get_uuid,
    uuid_generator
)


def test_uuid_generator():
    generator = uuid_generator()
    assert next(generator) == 0
    assert next(generator) == 1


def test_get_uuid(monkeypatch):
    monkeypatch.setattr("utils.uuid", uuid_generator())
    assert get_uuid() == 0
    assert get_uuid() == 1
