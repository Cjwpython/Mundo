# coding: utf-8
import time
from element.a import handle_a
from element.input import Inputer


class ElementHandler():
    def analyze(self, page):
        """
        解析元素
        """
        print("开始解析input标签")
        self.analyze_input(page)
        print("开始解析a标签")
        self.analyze_a(page)

    def analyze_a(self, page):
        """
        处理a标签
        """
        handle_a(page)

    def analyze_input(self, page):
        """
        处理input标签
        :param page:
        :return:
        """
        inputer = Inputer(page)
        inputer.analyze_element()
