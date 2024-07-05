import time

from loguru import logger
from pytest_check import check_func
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from common.get_token import GetToken
from common.logger import log_decorator
from POM.boss.base.base_page import BossBasePage

get_token = GetToken()


class ReportPageBoss(BossBasePage):

    def __init__(self):
        # 启动浏览器，进入boss_home页
        super().__init__()
        self.login_with_cookie()

        # 添加举报记录的必备数据
        self.user_id = 238492
        self.report_token = get_token.get_onelap_login_token()

        self.source_id = 714
        self.reason_id = 1
        self.source_type = 1
        self.desc = "测试"
        self.imgs = None

        self.headers = {'Authorization': self.report_token, 'UserId': str(self.user_id)}
        self.data = {"desc": self.desc,
                     "source_id": self.source_id,
                     "reason_id": self.reason_id,
                     "source_type": self.source_type,
                     "imgs": self.imgs}

    @log_decorator
    @check_func
    def report_review_failure(self):
        # 添加一条举报记录，在列表中筛选report_id
        self.add_report_message_with_request_post('add_report', self.headers, self.data)
        # self.driver.get('https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id=140')
        # self.element_locator('report', 'table')

        self.element_locator('report', 'report_tr')
        self.element_locator('report', 'open_report_review_button').click()

        # 等待审核窗口
        time.sleep(0.5)

        self.element_locator('report', 'review_failure_button').click()
        self.element_locator('report', 'review_success_button').click()

        # 等待alert
        time.sleep(0.5)

        self.switch_to_alert_accept()
        status = self.element_locator('report', 'table_review_status').text
        assert status == "审核未通过"

        # self.element_locator('report', 'table_review_reason').text
        # self.element_locator('report', 'table_review_method').text
        # self.element_locator('report', 'table_review_message').text

    @log_decorator
    @check_func
    def report_review_pass_warning(self):
        # 添加一条举报记录，在列表中筛选report_id
        self.add_report_message_with_request_post('add_report', self.headers, self.data)

        # self.driver.get('https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id=139')
        # 自动同步举报记录中的违规原因，无需更改
        # reason_select = self.element_locator('report', 'reason_select')
        # Select(reason_select).select_by_value('4')

        self.element_locator('report', 'report_tr')
        self.element_locator('report', 'open_report_review_button').click()

        time.sleep(0.5)
        self.element_locator('report', 'review_pass_button').click()
        method_select = self.element_locator('report', 'method_select')
        Select(method_select).select_by_value('is_notice_warning')

        self.element_locator('report', 'review_success_button').click()

        time.sleep(0.5)
        self.switch_to_alert_accept()

        status = self.element_locator('report', 'table_review_status').text
        method = self.element_locator('report', 'table_review_method').text

        try:
            assert status == "审核通过"
            logger.info(f"{status}断言成功")
            assert method == "通知警告"
            logger.info(f"{method}断言成功")
        except AssertionError as error:
            logger.error(f"断言失败{error}")

    @log_decorator
    @check_func
    def report_review_pass_forbid_speak_hours(self):
        # 添加一条举报记录，在列表中筛选report_id
        self.add_report_message_with_request_post('add_report', self.headers, self.data)
        # self.driver.get('https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id=138')

        # 自动同步举报记录中的违规原因，无需更改
        # reason_select = self.element_locator('report', 'reason_select')
        # Select(reason_select).select_by_value('4')

        self.element_locator('report', 'report_tr')
        self.element_locator('report', 'open_report_review_button').click()

        time.sleep(0.5)
        self.element_locator('report', 'review_pass_button').click()
        method_select = self.element_locator('report', 'method_select')

        Select(method_select).select_by_value('is_forbid_speak')

        input_box = self.element_locator('report', 'publish_time_input_hours')

        # 全选+删除+输入
        input_box.send_keys(Keys.CONTROL + 'a')
        input_box.send_keys(Keys.BACKSPACE)
        input_box.send_keys(1)

        self.element_locator('report', 'review_success_button').click()

        time.sleep(0.5)
        self.switch_to_alert_accept()

        status = self.element_locator('report', 'table_review_status').text
        method = self.element_locator('report', 'table_review_method').text

        try:
            assert status == "审核通过"
            logger.info(f"{status}断言成功")
            assert method == "禁言1小时"
            logger.info(f"{method}断言成功")
        except AssertionError as error:
            logger.error(f"断言失败{error}")

    @log_decorator
    @check_func
    def report_review_pass_forbid_login_hours(self):
        # 添加一条举报记录，在列表中筛选report_id
        self.add_report_message_with_request_post('add_report', self.headers, self.data)
        # self.driver.get('https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id=138')
        # self.element_locator('report', 'table')

        # 自动同步举报记录中的违规原因，无需更改
        # reason_select = self.element_locator('report', 'reason_select')
        # Select(reason_select).select_by_value('4')

        self.element_locator('report', 'report_tr')
        self.element_locator('report', 'open_report_review_button').click()

        time.sleep(0.5)
        self.element_locator('report', 'review_pass_button').click()
        method_select = self.element_locator('report', 'method_select')

        Select(method_select).select_by_value('is_forbid_login')

        input_box = self.element_locator('report', 'publish_time_input_hours')

        # 全选+删除+输入
        input_box.send_keys(Keys.CONTROL + 'a')
        input_box.send_keys(Keys.BACKSPACE)
        input_box.send_keys(1)

        self.element_locator('report', 'review_success_button').click()

        time.sleep(0.5)
        self.switch_to_alert_accept()

        status = self.element_locator('report', 'table_review_status').text
        method = self.element_locator('report', 'table_review_method').text

        try:
            assert status == "审核通过"
            logger.info(f"{status}断言成功")
            assert method == "封号1小时"
            logger.info(f"{method}断言成功")
        except AssertionError as error:
            logger.error(f"断言失败{error}")


if __name__ == '__main__':
    a = ReportPageBoss()
    a.report_review_failure()
    a.report_review_pass_warning()
    a.report_review_pass_forbid_speak_hours()
    a.report_review_pass_forbid_login_hours()
    a.driver.quit()
