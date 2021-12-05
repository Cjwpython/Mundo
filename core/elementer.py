# coding: utf-8
import time


class ElementHandler():
    def analyze(self, page):
        """
        解析元素
        """
        # self.analyze_a(page)
        self.analyze_input(page)

    def analyze_a(self, page):
        """
        处理a标签
        """
        all_a = page.query_selector_all("a")
        for a in all_a:
            text = a.inner_text().strip()
            print(f"开始点击:{text}")
            a.hover()
            time.sleep(1)
            a.click()

    def analyze_input(self, page):
        """
        处理input标签
        """
        user = page.query_selector("#app > div > section > form > div:nth-child(1) > div > div > input")
        user.type("arsadmin")
        passd = page.query_selector("#app > div > section > form > div.el-form-item.psd-box > div > div > input")
        passd.type("arsadmin2016")
        page.click("#app > div > section > button > span")
