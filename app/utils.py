def uuid_generator():
    """Unique id generator

    Yields:
        int: uuid
    """
    current = 0
    while True:
        yield current
        current += 1


# global generator
uuid = uuid_generator()


def get_uuid():
    """Returns unique id

    Returns:
        int: uuid
    """
    return next(uuid)
