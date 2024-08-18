import time

from loguru import logger

from POM.onelap.base_page.base_page import OnelapBasePage

from common.find_ele import find_ele


class OnelapLogin(OnelapBasePage):
    def __init__(self):
        super().__init__()

        self.username = "17753163583"
        self.passwd = "zhang107"

    def login(self):

        self.element_locator(self.driver_first, 'account_page', 'login', 'tv_agree_privacy_dialog').click()
        self.element_locator(self.driver_first, 'account_page', 'login', 'btn_login_index').click()
        self.element_locator(self.driver_first, 'account_page', 'login', 'et_username_login').send_keys(self.username)
        self.element_locator(self.driver_first, 'account_page', 'login', 'et_password_login').send_keys(self.passwd)
        self.element_locator(self.driver_first, 'account_page', 'login', 'btn_check_out_login').click()
        self.element_locator(self.driver_first, 'account_page', 'login', 'btn_login_login').click()
        self.element_locator(self.driver_first, 'account_page', 'login', 'tv_agree_privacy_dialog').click()

    def check_fields(self):
        time.sleep(2)
        self.element_locator(self.driver_first, "data_record_page", 'check_fields',
                             'include_data_bottom_navigation').click()
        # later_driver = connect_device_later
        time.sleep(2)
        for num in range(1, 11):
            key = f'(//android.widget.TextView[@resource-id="com.onelap.bls.dear:id/tv_origin_riding_record_item"])[{num}]'
            txt = find_ele(driver=self.driver_first, find_type='xpath', find_key=key).text
            if "来自 C" in txt:
                logger.info("读取码表标签文本成功")
                break
            else:
                logger.error("近10条数据中，没有来自码表的数据")


if __name__ == '__main__':
    x = OnelapLogin()
    x.login()
    x.check_fields()
