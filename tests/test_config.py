from config import config


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


def test_config_default_ship_set():
    pre_val = config.DEFAULT_SHIP_SET

    config.DEFAULT_SHIP_SET = {}
    assert config.DEFAULT_SHIP_SET == {}

    # setting it back to default because other tests use it
    config.DEFAULT_SHIP_SET = pre_val


def test_config_default_player_side():
    pre_val = config.DEFAULT_PLAYER_SIDE

    config.DEFAULT_PLAYER_SIDE = 1
    assert config.DEFAULT_PLAYER_SIDE == 1

    # setting it back to default because other tests use it
    config.DEFAULT_PLAYER_SIDE = pre_val


def test_config_load_from_user_config():
    pre_val = config.BOARD_SIZE

    config.BOARD_SIZE = 11
    config.save()
    config.BOARD_SIZE = 10
    config.__init__()
    assert config.BOARD_SIZE == 11

    # setting it back to default because other tests use it
    config.BOARD_SIZE = pre_val
    config.save()


def test_config_restore_to_default():
    config.BOARD_SIZE = 11
    config.save()
    config.__init__()
    config.restore_defaults()
    assert config.BOARD_SIZE == 10
