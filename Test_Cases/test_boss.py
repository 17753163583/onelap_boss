from POM.boss.page_object.login_page import LoginPageBoss
from POM.boss.page_object.report_page import Report
from POM.boss.page_object.report_result_page import ReportResult
from common.get_yaml import GetYamlData

from POM.boss import page_object
import pytest_check as check

account_dict = GetYamlData().get_login_accounts()['boss_account']


class TestLogin(LoginPageBoss):

    def test_login_right(self):
        account_1 = account_dict['account_1']
        self.login(username=account_1['username'],
                   password=account_1['password'])

    def test_login_error(self):
        account_2 = account_dict['account_2']
        self.login(username=account_2['username'],
                   password=account_2['password'])


class TestReport(Report):
    def review_failure(self):
        res = self.report_review_failure()

        check.equal(res, "审核未通过")

    def review_warning(self):
        status, method = self.report_review_pass_warning()

        check.equal(status, "审核通过")
        check.equal(method, "通知警告")

    def review_forbid_speak_hours(self):
        status, method = self.report_review_pass_forbid_speak_hours()

        check.equal(status, "审核通过")
        check.equal(method, "禁言1小时")

    def review_forbid_login_hours(self):
        status, method = self.report_review_pass_forbid_login_hours()

        check.equal(status, "审核通过")
        check.equal(method, "封号1小时")
