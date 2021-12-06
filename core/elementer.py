# coding: utf-8
import time


class ElementHandler():
    def analyze(self, page):
        """
        解析元素
        """
        self.analyze_a(page)
        self.analyze_input(page)

    def analyze_a(self, page):
        """
        处理a标签
        """
        all_a = page.query_selector_all("a")
        for a in all_a:
            text = a.inner_text().strip()
            if not a.is_visible():
                # print(f"元素不可见:{text}")
                continue
            if text:
                # print(f"开始点击:{text}")
                a.hover()
                # time.sleep(1)
                a.click()

    def analyze_input(self, page):
        all_input = page.query_selector_all("input")
        for input in all_input:
            text = input.get_attribute("text")
            if not input.is_visible():
                # print(f"输入框{text}不可见")
                continue
