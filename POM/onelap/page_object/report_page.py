import time

from common.connect_device import connect_device_later
from POM.onelap.base_page.base_page import OnelapBasePage
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from loguru import logger
from common.logger import log_decorator


class OnelapReport(OnelapBasePage):
    def __init__(self):
        super().__init__()
        self.driver = connect_device_later()
        self.action = ActionChains(self.driver)

    @log_decorator
    def get_review_page(self):
        self.element_locator(self.driver, 'report', 'include_planet_bottom_navigation').click()
        try:
            self.element_locator(self.driver, 'report', 'tv_confirm_common_dialog').click()
        except TimeoutException:
            logger.info("非初次打开路线页面")

        self.element_locator(self.driver, 'report', 'tv_search').click()
        self.element_locator_sendkeys(self.driver, 'report', 'key_input', 253)
        # 回车键
        self.driver.keyevent(66)

        self.element_locator(self.driver, 'report', 'only_one_route_cards').click()

    @log_decorator
    def submit_report(self):
        # 页面跳转，否则会报错
        time.sleep(3)

        self.element_locator(self.driver, 'report', 'route_comment').click()
        content = self.element_locator(self.driver, 'report', 'specify_comment')

        self.action.click_and_hold(content).pause(2).release().perform()

        self.element_locator(self.driver, 'report', 'report_button').click()

        time.sleep(1)

        self.element_locator(self.driver, 'report', 'report_source').click()
        self.element_locator_sendkeys(self.driver, 'report', 'report_content', '测试')
        self.element_locator(self.driver, 'report', 'btn_submit').click()

        if self.element_locator(self.driver, 'report', 'submit_success_toast'):
            return True
        else:
            return False


if __name__ == '__main__':
    x = OnelapReport()
    x.get_review_page()
    x.submit_report()
