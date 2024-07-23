import time

from loguru import logger
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from POM.boss.base_page.base_page import BossBasePage
from common.logger import log_decorator
from common.report_publish_message import append_data_key_to_json
from common.submit_comment import send_comment
from common.get_token import GetToken


class Report(BossBasePage):

    def __init__(self):
        # 启动浏览器，进入boss_home页
        super().__init__()
        self.login_with_cookie()
        # 添加举报记录的必备数据
        self.source_id = 714
        self.reason_id = 1
        self.source_type = 1
        self.desc = "测试"
        self.imgs = None

    def get_headers_and_data(self):
        onelap_login_res = GetToken().onelap_login(self.test_onelap_account_dict['account_1']['username'],
                                                   self.test_onelap_account_dict['account_1']['password'])
        if onelap_login_res['code'] == 204:
            logger.error("账号被封禁，请撤销处罚后再试")
            return
        elif onelap_login_res['code'] == 200:
            headers = {'Authorization': onelap_login_res['data']['token']}
            data = {"desc": self.desc,
                    "source_id": self.source_id,
                    "reason_id": self.reason_id,
                    "source_type": self.source_type,
                    "imgs": self.imgs}
            return headers, data

    @log_decorator
    def report_review_failure(self):
        if self.get_headers_and_data() is None:
            # 流程阻塞，退出函数
            return
        else:
            headers, data = self.get_headers_and_data()

        # 添加一条举报记录，在列表中筛选report_id
        self.add_report_message_with_request_post('add_report', headers, data)
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
        return status

        # self.element_locator('report', 'table_review_reason').text
        # self.element_locator('report', 'table_review_method').text
        # self.element_locator('report', 'table_review_message').text

    @log_decorator
    def report_review_pass_warning(self):
        if self.get_headers_and_data() is None:
            # 流程阻塞，退出函数
            return
        else:
            headers, data = self.get_headers_and_data()

        # 添加一条举报记录，在列表中筛选report_id
        self.add_report_message_with_request_post('add_report', headers, data)

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

        return status, method

    """ try:
         assert status == "审核通过"
         logger.info(f"{status}断言成功")
         assert method == "通知警告"
         logger.info(f"{method}断言成功")
     except AssertionError as error:
         logger.error(f"断言失败{error}")"""

    @log_decorator
    def report_review_pass_forbid_speak_hours(self):
        if self.get_headers_and_data() is None:
            # 流程阻塞，退出函数
            return
        else:
            headers, data = self.get_headers_and_data()

        # 添加一条举报记录，在列表中筛选report_id
        self.add_report_message_with_request_post('add_report', headers, data)
        # self.driver.get('https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id=158')

        # 自动同步举报记录中的违规原因，无需更改
        # reason_select = self.element_locator('report', 'reason_select')
        # Select(reason_select).select_by_value('4')

        data_key = self.element_locator('report', 'report_tr').get_attribute('data-key')
        logger.info(f"读取data-key：{data_key}")

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
        try:
            self.driver.switch_to.alert.accept()
            logger.info("更新惩罚时间弹窗")
        except NoAlertPresentException:
            pass

        # 访问评论接口（被禁言账号），读取禁言的开始时间和截止时间
        response_json = send_comment(username=self.test_onelap_account_dict['account_1']['username'],
                                     password=self.test_onelap_account_dict['account_1']['password'])

        data_key_dict = {
            'data_key': data_key,
            'start_time': response_json['data']['start_time'],
            'end_time': response_json['data']['end_time']
        }
        append_data_key_to_json(publish='is_forbid_speak', key_dict=data_key_dict)

        # 回到审核管理页做断言
        status = self.element_locator('report', 'table_review_status').text
        method = self.element_locator('report', 'table_review_method').text
        return status, method

    """    try:
            assert status == "审核通过"
            logger.info(f"{status}断言成功")
            assert method == "禁言1小时"
            logger.info(f"{method}断言成功")
        except AssertionError as error:
            logger.error(f"断言失败{error}")"""

    @log_decorator
    def report_review_pass_forbid_login_hours(self):
        if self.get_headers_and_data() is None:
            # 流程阻塞，退出函数
            return
        else:
            headers, data = self.get_headers_and_data()

        # 添加一条举报记录，在列表中筛选report_id
        self.add_report_message_with_request_post('add_report', headers, data)
        # self.driver.get('https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id=162')
        # self.element_locator('report', 'table')

        # 自动同步举报记录中的违规原因，无需更改
        # reason_select = self.element_locator('report', 'reason_select')
        # Select(reason_select).select_by_value('4')

        # 定位到目标举报记录
        data_key = self.element_locator('report', 'report_tr').get_attribute('data-key')
        logger.info(f"读取data-key：{data_key}")

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
        try:
            self.driver.switch_to.alert.accept()
            logger.info("更新惩罚时间弹窗")
        except NoAlertPresentException:
            pass

        # 重新访问登录接口（被禁言账号），读取封号的的开始时间和截止时间
        login_response = GetToken().onelap_login(self.test_onelap_account_dict['account_1']['username'],
                                                 self.test_onelap_account_dict['account_1']['password'])
        data_key_dict = {
            'data_key': data_key,
            'start_time': login_response['data']['start_time'],
            'end_time': login_response['data']['end_time']
        }
        append_data_key_to_json(publish='is_forbid_login', key_dict=data_key_dict)

        status = self.element_locator('report', 'table_review_status').text
        method = self.element_locator('report', 'table_review_method').text

        return status, method

    """    try:
            assert status == "审核通过"
            logger.info(f"{status}断言成功")
            assert method == "封号1小时"
            logger.info(f"{method}断言成功")
        except AssertionError as error:
            logger.error(f"断言失败{error}")"""


if __name__ == '__main__':
    a = Report()
    # a.report_review_failure()
    # a.report_review_pass_forbid_speak_hours()
    # a.report_review_pass_forbid_login_hours()
    a.driver.quit()
