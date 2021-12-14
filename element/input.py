# coding: utf-8
import time
from utils.log import setup_logger

logger = setup_logger(__name__)


class Inputer():
    """
    输入框控制器
    """

    def __init__(self, page):
        self.page = page
        self.func_dispatch = {
            "text": self._username,
            "password": self._password,
            "submit": self._submit
        }

    def _username(self, element):
        """
        处理用户名输入框
        :return:
        """
        logger.debug("开始输入用户名")
        element.fill('123123')

    def _password(self, element):
        """

        :return:
        """
        logger.debug("开始输入密码")
        element.fill('123123')

    def _submit(self, element):
        """
        提交按钮
        :return:
        """
        logger.debug("开始点击提交按钮")
        element.click()

    def analyze_element(self):
        all_input = self.page.query_selector_all("input")
        print(all_input)
        for input in all_input:
            type = input.get_attribute("type")
            if not type:
                continue
            text = type.strip()
            # 标签被隐藏
            if input.is_hidden():
                logger.debug(f"标签隐藏{text}")
                continue
            # 标签不可用
            if not input.is_enabled():
                logger.debug(f"输入框不可用:{text}")
                continue

            func = self.func_dispatch.get(text)
            if not func:
                logger.debug(f"未添加解析的方法:{text}")
                continue
            logger.debug_json(f"{text}的属性", {
                "is_hidden": input.is_hidden(),
                "is_visible": input.is_visible(),
                "is_enable": input.is_enabled(),
                "is_editable": input.is_editable(),
                "is_disable": input.is_disabled()
            })

            input.hover()
            func(input)
            # time.sleep(3)
