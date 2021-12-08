# coding: utf-8
import time
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
        print("开始输入用户名")
        element.fill('123123')

    def _password(self, element):
        """

        :return:
        """
        print("开始输入密码")
        element.fill('123123')

    def _submit(self, element):
        """
        提交按钮
        :return:
        """
        print("开始点击提交按钮")
        element.click()

    def analyze_element(self):
        all_input = self.page.query_selector_all("input")
        for input in all_input:
            type = input.get_attribute("type")

            if not type:
                continue
            text = type.strip()
            print(f"{text} is_hidden:{input.is_hidden()} is_visible:{input.is_visible()} is_enable:{input.is_enabled()} is_editable:{input.is_editable()} is_disable:{input.is_disabled()}")
            if input.is_hidden():
                print(f"标签隐藏{text}")
                continue
            if not input.is_enabled():
                print(f"输入框不可用:{text}")
                continue
            func = self.func_dispatch.get(text)
            if not func:
                print(f"未添加解析的方法:{text}")
                continue
            input.hover()
            func(input)
            time.sleep(3)
