import time

from loguru import logger
from selenium.common.exceptions import TimeoutException

from POM.onelap.base_page.base_page import OnelapBasePage
from common.connect_device import connect_device_first, connect_phone_first
from common.find_ele import find_ele
from common.get_verification_code import get_verification_code
from common.logger import log_decorator


class OnelapLogin(OnelapBasePage):
    def __init__(self):
        super().__init__()
        # self.driver_current = connect_device_later()

    @log_decorator
    def open_login(self, username, password):
        # 获取cookie使用
        driver = connect_device_first()
        self.element_locator(driver, 'account_page', 'login', 'tv_agree_privacy_dialog').click()
        self.element_locator(driver, 'account_page', 'login', 'btn_login_index').click()
        self.element_locator(driver, 'account_page', 'login', 'et_username_login').send_keys(username)
        self.element_locator(driver, 'account_page', 'login', 'et_password_login').send_keys(password)
        self.element_locator(driver, 'account_page', 'login', 'btn_check_out_login').click()
        self.element_locator(driver, 'account_page', 'login', 'btn_login_login').click()

    @log_decorator
    def sign_up(self, phone):
        driver = connect_device_first()
        page_name = 'account_page'
        module_name = 'sign_up'
        self.element_locator(driver, page_name, 'login', 'tv_agree_privacy_dialog').click()
        self.element_locator(driver, page_name, module_name, 'btn_register_index').click()
        self.element_locator_sendkeys(driver, page_name, module_name, 'et_username_register', phone)
        self.element_locator(driver, page_name, module_name, 'btn_check_out_register').click()
        # 获取验证码
        self.element_locator(driver, page_name, module_name, 'btn_over_register').click()

        # 读取并输入验证码
        time.sleep(10)
        phone_code = get_verification_code()
        for num in range(1, 7):
            find_ele(driver, find_type='id', find_key=f'com.onelap.bls.dear:id/et_{num}').send_keys(phone_code[num - 1])
        pass


    def forget_passwd(self, username, passwd):
        driver = connect_phone_first()
        self.element_locator(driver, 'account_page', 'login', 'tv_agree_privacy_dialog').click()
        self.element_locator(driver, 'account_page', 'login', 'btn_login_index').click()
        driver.tap([(700, 400)])

        self.element_locator(driver, 'account_page', 'forget_password', 'btn_forget_password_login').click()
        self.element_locator_sendkeys(driver, 'forget_password', 'et_account_find_pwd', username)
        self.element_locator(driver, 'account_page', 'forget_password', 'btn_over_find_pwd').click()

        # 读取并输入验证码
        time.sleep(10)
        phone_code = get_verification_code()
        for num in range(1, 7):
            find_ele(driver, find_type='id', find_key=f'com.onelap.bls.dear:id/et_{num}').send_keys(phone_code[num - 1])

        self.element_locator(driver, 'account_page', 'forget_password', 'btn_over_register_code').click()
        self.element_locator_sendkeys(driver, 'forget_password', 'et_pwd_register_pwd', passwd)
        self.element_locator(driver, 'account_page', 'forget_password', 'btn_check_out_register_pwd').click()
        self.element_locator(driver, 'account_page', 'forget_password', 'btn_over_register_pwd').click()
        try:
            success = self.element_locator(driver, 'account_page', 'forget_password', 'md_content')
            logger.info("密码修改成功")
            return success
        except TimeoutException:
            logger.error("密码修改失败")


if __name__ == '__main__':
    OnelapLogin().open_login('17753163583', 'zhang107')
