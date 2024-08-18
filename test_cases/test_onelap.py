import pytest_check as check
import allure
from POM.onelap.base_page.base_page import OnelapBasePage
from POM.onelap.page_object.account_page import OnelapLogin
from POM.onelap.page_object.report_page import OnelapReport

account_dict = OnelapBasePage().test_onelap_account_dict


class TestOnelap:
    @allure.feature("登录模块")
    def test_login(self):
        OnelapLogin().open_login(account_dict['account_1']['username'], account_dict['account_1']['password'])
        text = OnelapLogin().get_app_name()

        check.equal(text, '顽鹿运动（预发布服）')

    @allure.feature("举报模块")
    def test_report(self):
        OnelapReport().get_review_page()
        res_bool = OnelapReport().submit_report()

        check.is_true(res_bool)
