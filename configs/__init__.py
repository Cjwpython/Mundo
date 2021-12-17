# coding: utf-8
from configs.browser import BrowserController
from configs.context import ContextController
from configs.logging import LoggingController
from configs.page import PageController
from configs.task import TaskController


class ConfigController(BrowserController, ContextController, PageController, LoggingController, TaskController):
    @classmethod
    def dict(cls):
        return {
            "browser_configs": {
                "headless": cls.headless,
                "executable_path": cls.executable_path,
                "proxy": cls.proxy
            },
            "context_configs": {
                "user_agent": cls.user_agent,
                "java_script_enabled": cls.java_script_enabled,
                "ignore_https_errors": cls.ignore_https_errors
            },
            "page_configs": {
                "waitTime": cls.waitTime,
                "wait_until": cls.wait_until
            },
            "logging_config": {
                "level": cls.level
            },
            "task_configs": {
                "task_id": cls.task_id,
                "base_url": cls.base_url
            }
        }


if __name__ == '__main__':
    C = ConfigController()
    print(C.dict())
