import pytest
from websocket import create_connection
from websocket import _exceptions as ws_exception
from lib.setup_logger import logger


def pytest_addoption(parser):
    """ TODO"""
    parser.addoption("--url", action="store")
    parser.addoption("--port", action="store")


@pytest.fixture(name="url", scope="class")
def url_fixture(request):
    """ TODO """
    logger.info("url() fixture is being called")
    logger.info("-----------------------------\n")
    # if option does not exist, None value will be returned.
    _url = request.config.getoption("--url")
    logger.info("url() fixture : url={}".format(_url))
    request.cls.url = _url
    logger.info("url() fixture is done")
    logger.info("---------------------")
    return request.cls.url


@pytest.fixture(name="port", scope="class")
def port_fixture(request):
    """ TODO """
    logger.info("port() fixture is being called")
    logger.info("------------------------------\n")
    # if option does not exist, None value will be returned.
    _port = request.config.getoption("--port")
    logger.info("url() fixture : url={}".format(_port))
    request.cls.port = _port
    logger.info("port() fixture is done")
    logger.info("----------------------")
    return request.cls.port


@pytest.fixture(scope="function")
def connect(request, url, port):
    """ TODO"""
    expected_greeting = f"Greetings, friend! Type <tt>help</tt> to get started."
    ws_url = f"{url}:{port}"
    try:
        # create websocket connection
        logger.info(f"Creating websocket connection to {ws_url}")
        _connect = create_connection(ws_url)
        actual_greeting = _connect.recv()
        assert expected_greeting == actual_greeting, f"ERROR: Actual greeting: \"{actual_greeting}\" differs from " \
                                                     f"Expected greeting : {expected_greeting}"
    except (ws_exception.WebSocketAddressException, ValueError):
        _connect = None
    assert _connect is not None, f"Failed to establish websocket connection"
    request.cls.connect = _connect

    def fin():
        logger.info(f"Closing websocket connection.")
        if _connect:
            _connect.close()
    request.addfinalizer(fin)
    return request.cls.connect
