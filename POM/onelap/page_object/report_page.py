import time

from POM.onelap.base.base_page import OnelapBasePage
from selenium.webdriver import ActionChains


class OnelapReport(OnelapBasePage):
    def __init__(self):
        super().__init__()
        self.driver = self.connect_device_later()
        self.action = ActionChains(self.driver)

    def get_review_page(self):
        self.element_locator(self.driver, 'report', 'include_planet_bottom_navigation').click()
        self.element_locator(self.driver, 'report', 'tv_confirm_common_dialog').click()
        self.element_locator(self.driver, 'report', 'tv_search').click()
        self.element_locator_sendkeys(self.driver, 'report', 'key_input', 304)
        # 回车键
        self.driver.keyevent(66)

        self.element_locator(self.driver, 'report', 'only_one_route_cards').click()

    def submit_report(self):
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
