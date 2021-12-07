# coding: utf-8

class RepeatHandler():
    """
    整体去重的逻辑
    """
    request_cache = set()
    click_cache = set()

    @classmethod
    def request_add(self, url):
        """
        添加缓存
        :return:
        """
        self.request_cache.add(url)

    @classmethod
    def request_remove(self, url):
        """
        去除缓存
        :return:
        """
        self.request_cache.remove(url)

    @classmethod
    def request_in(self, url):
        """
        判断目标是否在缓存中
        :param url:
        :return:
        """
        if url in self.request_cache:
            return True
        return False

    @classmethod
    def click_add(self, page, element_name):
        """
        点击缓存，点击过后的元素不再点击
        :param page:
        :param element_name:
        :return:
        """
        url = page.url
        _str = f"{url}:{element_name}"
        self.click_cache.add(_str)

    @classmethod
    def click_remove(self, page, element_name):
        """
        去除点击缓存 这个方式一般调用不到
        :param page:
        :param element_name:
        :return:
        """
        url = page.url
        _str = f"{url}:{element_name}"
        self.click_cache.remove(_str)

    @classmethod
    def click_in(self, page, element_name):
        """
        判断点击元素是否在缓存中
        :param page:
        :param element_name:
        :return:
        """
        url = page.url
        _str = f"{url}:{element_name}"
        if _str in self.click_cache:
            return True
        return False


if __name__ == '__main__':
    for i in range(10):
        RepeatHandler.request_add(i)
    print(RepeatHandler.request_cache)
