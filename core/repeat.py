# coding: utf-8

class RepeatHandler():
    """
    整体去重的逻辑
    """
    cache = set()

    @classmethod
    def add_cache(self, url):
        """
        添加缓存
        :return:
        """
        self.cache.add(url)

    @classmethod
    def remove_cache(self, url):
        """
        去除缓存
        :return:
        """
        self.cache.remove(url)

    @classmethod
    def in_cache(self, url):
        """
        判断目标是否在缓存中
        :param url:
        :return:
        """
        if url in self.cache:
            return True
        return False


if __name__ == '__main__':
    for i in range(10):
        RepeatHandler.add_cache(i)
    print(RepeatHandler.cache)
