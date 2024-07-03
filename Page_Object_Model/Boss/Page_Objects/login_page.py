import time

from Page_Object_Model.Boss.Base.Base_Page import BasePage
from Common.logger import log_decorator
from loguru import logger
from pytest_check import check_func


class LoginPage(BasePage):
    """
    def __init__(self):
        super().__init__()
    """

    @log_decorator
    @check_func
    def login(self):
        self.get_url('login')

        self.element_locator_sendkeys(page_name='login', element_name='input_username', input_data='onelap')
        self.element_locator_sendkeys(page_name='login', element_name='input_password', input_data='onelap@123')
        self.element_locator(page_name='login', element_name='login_button').click()

        self.save_boss_cookies_to_json()

        home_page_title = self.element_locator(page_name='home', element_name='page_title')

        try:
            assert home_page_title.text == 'Welcome to Onelap Management System.'
            logger.info("登录操作完成")
        except AssertionError as error:
            logger.error(f"home_page_title断言失败，错误信息为：{error}")


if __name__ == '__main__':
    a = LoginPage()
    a.login()
