import time

from POM.onelap.base_page.base_page import OnelapBasePage
from common.connect_device import connect_device_first, connect_device_later, connect_phone_first
from common.logger import log_decorator
from common.get_verification_code import get_verification_code
from common.find_ele import find_ele
from selenium.common.exceptions import TimeoutException
from loguru import logger


class OnelapLogin(OnelapBasePage):
    def __init__(self):
        super().__init__()
        # self.driver_current = connect_device_later()

    @log_decorator
    def open_login(self, username, password):
        driver = connect_device_first()
        self.element_locator(driver, 'login', 'tv_agree_privacy_dialog').click()
        self.element_locator(driver, 'login', 'btn_login_index').click()
        self.element_locator(driver, 'login', 'et_username_login').send_keys(username)
        self.element_locator(driver, 'login', 'et_password_login').send_keys(password)
        self.element_locator(driver, 'login', 'btn_check_out_login').click()
        self.element_locator(driver, 'login', 'btn_login_login').click()

    def forget_passwd(self):
        driver = connect_phone_first()
        self.element_locator(driver, 'login', 'tv_agree_privacy_dialog').click()
        self.element_locator(driver, 'login', 'btn_login_index').click()
        driver.tap([(700, 400)])

        self.element_locator(driver, 'forget_password', 'btn_forget_password_login').click()
        self.element_locator_sendkeys(driver, 'forget_password', 'et_account_find_pwd', '15794579615')
        self.element_locator(driver, 'forget_password', 'btn_over_find_pwd').click()

        time.sleep(5)

        phone_code = get_verification_code()

        for num in range(1, 7):
            find_ele(driver, find_type='id', find_key=f'com.onelap.bls.dear:id/et_{num}').send_keys(phone_code[num - 1])

        self.element_locator(driver, 'forget_password', 'btn_over_register_code').click()
        self.element_locator_sendkeys(driver, 'forget_password', 'et_pwd_register_pwd', 'zhang107')
        self.element_locator(driver, 'forget_password', 'btn_check_out_register_pwd').click()
        self.element_locator(driver, 'forget_password', 'btn_over_register_pwd').click()
        try:
            success = self.element_locator(driver, 'forget_password', 'md_content')
            logger.info("密码修改成功")
            return success
        except TimeoutException:
            logger.error("密码修改失败")

    # @log_decorator
    # def get_app_name(self):
    #     self.element_locator(self.driver_current, 'login', 'tv_agree_privacy_dialog').click()
    #
    #     home_title = self.element_locator(self.driver_current, 'login', 'tv_app_name_main_fragment').text
    #     return home_title


if __name__ == '__main__':
    OnelapLogin().forget_passwd()
