# coding: utf-8
import logging
from types import MethodType

from colorlog import ColoredFormatter

from settings import logging_level
import json


def log_debug_json(self, msg='', data={}):
    if self.isEnabledFor(logging.DEBUG):
        if isinstance(data, dict):
            try:
                self.debug('{} \n{}'.format(msg, json.dumps(data, indent=2)))
            except TypeError:
                self.debug('{} \n{}'.format(msg, data))
        else:
            self.debug('{} {}'.format(msg, data))


def setup_logger(name='Mundo'):
    LOGFORMAT = "[%(asctime)s]] [%(log_color)s**%(levelname)s**%(reset)s] [%(filename)s:%(funcName)s:%(log_color)s%(lineno)d%(reset)s] %(log_color)s%(message)s%(reset)s"
    formatter = ColoredFormatter(LOGFORMAT)

    logger = logging.getLogger(name)
    logger.setLevel(logging_level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.debug_json = MethodType(log_debug_json, logger)
    return logger


if __name__ == '__main__':
    logger = setup_logger(__name__)
    logger.json("a", {"a": 1})
