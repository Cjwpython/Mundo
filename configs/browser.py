# coding: utf-8
from settings import browser_configs


class BrowserController():
    """
    浏览器的设置
    """
    headless = browser_configs.get("headless", True)
    executable_path = browser_configs.get("executable_path")
    proxy = {
        "server": "",
        "username": "",
        "password": ""
    }

    @classmethod
    def set_headless(cls, headless: bool):
        cls.headless = headless

    @classmethod
    def set_executable_path(cls, executable_path: str):
        cls.executable_path = executable_path

    @classmethod
    def set_proxy(cls, server, username, password):
        cls.proxy["server"] = server
        cls.proxy["username"] = username
        cls.proxy["password"] = password

    @classmethod
    def browser_configs(cls):
        return {
                "headless": cls.headless,
                "executable_path": cls.executable_path,
                # "proxy": cls.proxy
            }



if __name__ == '__main__':
    b = BrowserController()
    print(b.dict())
