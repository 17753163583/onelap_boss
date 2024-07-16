import time
import pytest_check as check
from common.logger import log_decorator
from POM.onelap.base.base_page import OnelapBasePage
from POM.onelap.page_object.login_page import OnelapLogin
from POM.onelap.page_object.report_page import OnelapReport

account_dict = OnelapBasePage().test_onelap_account_dict


class TestOnelap:
    def test_login(self):
        OnelapLogin().open_onelap_app(account_dict['account_1']['username'], account_dict['account_1']['password'])
        text = OnelapLogin().get_app_name()

        check.equal(text, '顽鹿运动（预发布服）')

    def test_report(self):
        OnelapReport().get_review_page()
        res_bool = OnelapReport().submit_report

        check.is_true(res_bool)
