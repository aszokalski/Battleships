def uuid_generator():
    """Simple unique id generator. Id's are just consecutive numbers.

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
