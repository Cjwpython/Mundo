# coding: utf-8
import time

from configs import ConfigController
from utils.error import LoginElementNotFound, LoginError

from utils.log import setup_logger

logger = setup_logger(__name__)


class Loginer():
    """
    登录器
    """
    login_status = False

    def set_config(self, login_configs):
        self.login_url = login_configs.get("login_url")  # 登录的url
        self.login_select_type = login_configs.get("login_select_type", "auto")  # 会自动匹配用户名的输入框
        self.username_selector = login_configs.get("username_selector")  # 自定义的用户名输入框
        self.username_locator = None
        self.username_input = login_configs.get("username_input")  # 用户名输入的参数
        self.password_selector = login_configs.get("password_selector")  # 自定义的密码输入框
        self.password_locator = None
        self.password_input = login_configs.get("password_input")  # 密码的输入参数
        self.submit_selector = login_configs.get("submit_selector")  # 登录的按钮
        self.submit_locator = None
        self.login_error_raise = login_configs.get("login_error_raise", False)  # 登录失败不进行爬虫任务
        self.confirm_login_meta_url = login_configs.get("confirm_login_meta_url")  # 确认登录状态的url  会将登录的信息返回

    def get_selecotr(self, selector, type):
        """
        获取标签选择器
        """
        if type == "username":
            self.username_locator = self.page.locator(selector)
        if type == "password":
            self.password_locator = self.page.locator(selector)
        if type == "submit":
            self.submit_locator = self.page.locator(selector)

    def get_auto_input_selector(self):
        # 解析页面
        all_input = self.page.query_selector_all("input")
        for input in all_input:
            type = input.get_attribute("type")
            if not type:
                continue
            text = type.strip()
            # 标签被隐藏
            if input.is_hidden():
                logger.debug(f"标签隐藏{text}")
                continue
            # 标签不可用
            if not input.is_enabled():
                logger.debug(f"输入框不可用:{text}")
                continue
            if type == "text":
                self.username_locator = input
            elif type == "password":
                self.password_locator = input

    def login(self, login_configs):
        """
        进行登录设置
        """
        self.set_config(login_configs)
        self.page = self.new_page()
        self.page.goto(self.login_url, wait_until=ConfigController.wait_until)
        if self.login_select_type == "auto":
            self.get_auto_input_selector()
        else:
            self.get_selecotr(self.username_selector, "username")
            self.get_selecotr(self.password_selector, "password")
        self.get_selecotr(self.submit_selector, "submit")
        if not all([self.username_locator, self.password_locator, self.submit_locator]):
            if self.login_error_raise:
                raise LoginElementNotFound
            return
        self.username_locator.fill(self.username_input)
        self.password_locator.fill(self.password_input)
        self.submit_locator.click()
        time.sleep(1)
        self.confirm_login_status()
        if self.login_status:
            logger.info("登录成功")
        else:
            if self.login_error_raise:
                logger.error("登录失败")
                raise LoginError
            logger.error("登录失败，账号密码错误")
        self.page.close()

    def confirm_login_status(self):
        """
        判断登录是否成功
        1，登录框是否存在
        """
        submit_locator = self.page.locator(self.submit_selector)
        if not submit_locator:
            self.login_status = True
