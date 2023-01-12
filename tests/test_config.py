import config


def test_config_board_size():
    pre_val = config.BOARD_SIZE

    config.BOARD_SIZE = 11
    assert config.BOARD_SIZE == 11

    # setting it back to default because other tests use it
    config.BOARD_SIZE = pre_val


def test_config_default_orientation():
    pre_val = config.DEFAULT_ORIENTATION

    config.DEFAULT_ORIENTATION = "DOWN"
    assert config.DEFAULT_ORIENTATION == "DOWN"

    # setting it back to default because other tests use it
    config.DEFAULT_ORIENTATION = pre_val


def test_config_boat_sizes():
    pre_val = config.BOAT_SIZES

    config.BOAT_SIZES = {}
    assert config.BOAT_SIZES == {}

    # setting it back to default because other tests use it
    config.BOAT_SIZES = pre_val