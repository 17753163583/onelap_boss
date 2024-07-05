import time

from POM.boss.base.base_page import BossBasePage
from common.logger import log_decorator
from loguru import logger
from pytest_check import check_func


class LoginPageBoss(BossBasePage):
    def __init__(self):
        super().__init__()

    @log_decorator
    @check_func
    def get_onelap_url(self):
        self.get_url('login')

    def enter_username_and_password(self):
        self.element_locator_sendkeys(page_name='login', element_name='input_username', input_data='onelap')
        self.element_locator_sendkeys(page_name='login', element_name='input_password', input_data='onelap@123')

    def login_and_save_cookies(self):
        self.element_locator(page_name='login', element_name='login_button').click()

        self.save_boss_cookies_to_json()

    def assert_login(self):
        home_page_title = self.element_locator(page_name='home', element_name='page_title')

        try:
            assert home_page_title.text == 'Welcome to Onelap Management System.'
            logger.info("登录操作完成")
        except AssertionError as error:
            logger.error(f"home_page_title断言失败，错误信息为：{error}")


if __name__ == '__main__':
    a = LoginPageBoss()
    a.get_onelap_url()
    a.enter_username_and_password()
    a.login_and_save_cookies()
    a.assert_login()
    a.driver.quit()
