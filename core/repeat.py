# coding: utf-8
from urllib.parse import urljoin, urlparse

from configs import ConfigController
from utils.log import setup_logger

logger = setup_logger(__name__)


class RepeatHandler():
    """
    整体的去重
    """
    request_cache = set()
    click_cache = set()

    @classmethod
    def request_add(self, url, method):
        """
        添加缓存
        :return:
        """
        _str = f"{url}:{method}"
        if _str not in self.request_cache:
            self.request_cache.add(_str)
            logger.debug(f">>>>>>request cache add {_str}<<<<<<<")

    @classmethod
    def request_remove(self, url, method):
        """
        去除缓存
        :return:
        """
        _str = f"{url}:{method}"
        self.request_cache.remove(_str)

    @classmethod
    def request_in(self, url, method):
        """
        判断目标是否在缓存中
        :param url:
        :return:
        """
        _str = f"{url}:{method}"
        if _str in self.request_cache:
            return True
        return False

    @classmethod
    def can_request(cls, url, method):
        """
        判断目标是否可以请求
        """

        # 判断页面是否完全加载(静态资源不做去重处理)
        def _t(url, method):
            _str = f"{url}:{method}"
            if _str in cls.request_cache:
                return False
            return True

        if ConfigController.static_repeat:  # 说明静态资源去重
            return _t(url, method)
        else:
            path = urlparse(url).path
            path_suffix = path.split(".")[-1]
            if path_suffix in ConfigController.static_suffix:
                return True
            else:
                return _t(url, method)

    @classmethod
    def click_add(self, page, element):
        """
        点击缓存，点击过后的元素不再点击
        :param page:
        :param element:
        :return:
        """
        url = page.url
        href = element.get_attribute("href")
        _str = urljoin(url, href)
        self.click_cache.add(_str)

    @classmethod
    def click_remove(self, page, element):
        """
        去除点击缓存 这个方式一般调用不到
        :param page:
        :param element:
        :return:
        """
        url = page.url
        href = element.get_attribute("href")
        _str = urljoin(url, href)
        self.click_cache.remove(_str)

    @classmethod
    def click_in(self, page, element):
        """
        判断点击元素是否在缓存中
        :param page:
        :param element:
        :return:
        """
        url = page.url
        href = element.get_attribute("href")
        _str = urljoin(url, href)
        if _str in self.click_cache:
            return True
        return False
