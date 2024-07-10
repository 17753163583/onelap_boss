from loguru import logger

from POM.boss.base.base_page import BossBasePage
from common.logger import log_decorator
from selenium.common.exceptions import TimeoutException


class LoginPageBoss(BossBasePage):
    def __init__(self):
        super().__init__()

    @log_decorator
    def login(self, username, password):
        self.get_url('login')
        self.element_locator_sendkeys(page_name='login', element_name='input_username', input_data=username)
        self.element_locator_sendkeys(page_name='login', element_name='input_password', input_data=password)

        self.element_locator(page_name='login', element_name='login_button').click()

        try:
            self.element_locator(page_name='login', element_name='account_input_error')
            logger.error("账号密码不匹配")
            return
        except TimeoutException:
            logger.info("账号密码匹配成功")

        self.save_boss_cookies_to_json()
        try:
            self.element_locator(page_name='home', element_name='page_title')
            logger.info("登录调整home页成功")
        except TimeoutException:
            logger.error("登录调整home页失败")


if __name__ == '__main__':
    a = LoginPageBoss()
    a.login('onelap', 'onelap@123')

    a.driver.quit()
