# coding: utf-8
from urllib.parse import urljoin

from utils.target import is_same_netloc


class Analysis():
    """
    页面解析类
    """

    def __init__(self, queue, base_target):
        self.base_target = base_target
        self.queue = queue

    def analysis_a(self, base_url, page):
        try:
            a = page.query_selector_all("a")
            for i in a:
                real_url = urljoin(base_url, i.get_attribute("href"))
                if is_same_netloc(self.base_target,real_url):
                    self.queue.put(real_url)
                    # print("队列添加：{}".format(real_url))
        except Exception as e:
            print(e)
