# coding: utf-8
from utils.error import TaskStopError


class Counter():
    """
    计数器
    """

    maxReuqestNum = 0  # 0 标识不做限制，直到请求队列中的所有任务结束
    realRequestNum = 0

    @classmethod
    def need_continue(cls):
        """
        当超过了最大的请求数量设置，会抛出taskStopError
        """
        if not cls.maxReuqestNum:
            return True
        cls.realRequestNum += 1

        if cls.realRequestNum > cls.maxReuqestNum:
            raise TaskStopError()
        return True


if __name__ == '__main__':
    Counter.maxReuqestNum = 10
    for i in range(100):
        if Counter.need_continue():
            print(i)
