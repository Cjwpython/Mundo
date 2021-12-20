# coding: utf-8

class TaskStopError(Exception):
    """
    任务停止异常
    """
    pass


class LoginElementNotFound(Exception):
    """
    登录元素未发现
    """
    pass


class LoginError(Exception):
    """
    登录失败
    """
    pass
