from POM.boss.base_page.base_page import BossBasePage
from common.logger import log_decorator
from common.report_publish_message import get_publish_data_key_list, remove_data_key_to_json
from loguru import logger
from common.find_ele import find_ele
from common.get_path import project_path
from common.submit_comment import send_comment
from selenium.common.exceptions import TimeoutException
from common.get_token import GetToken


class ReportResult(BossBasePage):
    def __init__(self):
        super().__init__()
        self.login_with_cookie()
        self.publish_message_path = project_path() + '/POM/boss/test_data/publish_data.json'

    @log_decorator
    def check_report_result_sheet(self, publish):
        forbid_data_key_list = get_publish_data_key_list(publish=publish)

        self.get_url('report_result')
        # 对json已记录的惩罚信息循环定位
        for data_key in forbid_data_key_list:
            try:
                find_ele(self.driver, 'xpath', f'//*[@data-key="{data_key}"]')
                logger.info(f"{publish}惩罚记录定位成功，data-key:{data_key}")
            except TimeoutException:
                logger.error(f"{publish}惩罚记录定位失败，data-key:{data_key}")
                return False
        return True

    @log_decorator
    def cancel_forbid_publish(self, publish):
        forbid_data_key_list = get_publish_data_key_list(publish=publish)

        self.get_url('report_result')

        for data_key in forbid_data_key_list:
            # 操作按钮
            find_ele(self.driver, 'xpath', f'//*[@data-key="{data_key}"]/td[12]/div/a').click()
            # 撤销
            find_ele(self.driver, 'xpath', f'//*[@data-key="{data_key}"]/td[12]/div/ul/li/a').click()

            if remove_data_key_to_json(publish, data_key):
                logger.info(f"撤销{publish}处罚{data_key}")

        if publish == 'is_forbid_speak':
            # 访问评论接口，查看评论功能是否恢复
            response_json = send_comment(self.test_onelap_account_dict['account_1']['username'],
                                         self.test_onelap_account_dict['account_1']['password'])
            return response_json

        elif publish == 'is_forbid_login':
            # 访问登录接口，查看登录功能是否恢复
            response_json = GetToken().onelap_login(self.test_onelap_account_dict['account_1']['username'],
                                                    self.test_onelap_account_dict['account_1']['password'])
            return response_json


if __name__ == '__main__':
    x = ReportResult()
    x.check_report_result_sheet('is_forbid_speak')
    x.cancel_forbid_publish('is_forbid_speak')
    x.driver.quit()
