# coding: utf-8
import logging
from types import MethodType

from colorlog import ColoredFormatter

from configs import ConfigController
import json


def log_debug_json(self, msg='', data={}):
    if self.isEnabledFor(logging.DEBUG):
        if isinstance(data, dict):
            try:
                self.debug('{} \n{}'.format(msg, json.dumps(data, indent=4)))
            except TypeError:
                self.debug('{} \n{}'.format(msg, data))
        else:
            self.debug('{} {}'.format(msg, data))


def log_info_json(self, msg='', data={}):
    if self.isEnabledFor(logging.INFO):
        if isinstance(data, dict):
            try:
                self.info('{} \n{}'.format(msg, json.dumps(data, indent=4)))
            except TypeError:
                self.info('{} \n{}'.format(msg, data))
        else:
            self.info('{} {}'.format(msg, data))


def setup_logger(name='Mundo'):
    LOGFORMAT = "[%(asctime)s]] [%(log_color)s**%(levelname)s**%(reset)s] [%(filename)s:%(funcName)s:%(log_color)s%(lineno)d%(reset)s] %(log_color)s%(message)s%(reset)s"
    formatter = ColoredFormatter(LOGFORMAT)

    logger = logging.getLogger(name)
    logger.setLevel(ConfigController.level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(ConfigController.level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.debug_json = MethodType(log_debug_json, logger)
    # logger.info_json = MethodType(log_info_json, logger)
    return logger


if __name__ == '__main__':
    logger = setup_logger(__name__)
    logger.debug_json("a", {"a": 1})
