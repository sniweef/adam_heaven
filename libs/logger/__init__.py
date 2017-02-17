import logging


def set_up_def_logger():
    global logger
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()

    # create formatter
    fmt = "%(asctime)-12s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    datefmt = "%a %d %b %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

logger = logging.getLogger(__name__)
set_up_def_logger()


def replace_logger_with(new_logger):
    assert isinstance(new_logger, logging.Logger)
    global logger
    logger = new_logger
