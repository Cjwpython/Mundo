# coding: utf-8
from settings import logging_configs


class LoggingController():
    level = logging_configs.get("level", "INFO")

    @classmethod
    def set_logging_level(cls, level: str):
        cls.level = level
