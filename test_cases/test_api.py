import allure
import pytest
import pytest_check as check

from API.base_page.base_page import BasePage
from API.page_object.login_and_logout import OnelapLogin
from API.page_object.data_analysis_page import DataAnalysis

onelap_account_dict = BasePage().onelap_account_dict


@allure.feature("账号相关")
class TestOnelapLogin:
    @allure.story("正常登录")
    @allure.title("输入正确的账号密码，登录成功")
    @pytest.mark.parametrize("account_num", onelap_account_dict)
    def test_login_pass(self, account_num):
        account = onelap_account_dict[account_num]
        res = OnelapLogin().login(account['username'], account['password'])

        check.equal(res['code'], 200)

    @allure.story("登录失败")
    @allure.title("输入错误的账号密码，登录失败")
    def test_login_fail(self):
        res = OnelapLogin().login(onelap_account_dict['account_1']['username'], '123')

        check.not_equal(res['code'], 200)

    @allure.story("密码核验接口")
    @allure.title("密码核验成功")
    def test_check_passwd(self):
        res = OnelapLogin().check_passwd(onelap_account_dict['account_1']['password'])

        check.equal(res['code'], 200)

    @allure.story("密码核验接口")
    @allure.title("账号注销成功")
    def test_account_cancellation(self):
        res = OnelapLogin().account_cancellation()

        check.equal(res['code'], 200)


@allure.feature("数据分析与数据记录")
class TestOnelapDataAnalysis:
    @allure.story("数据分析")
    @allure.title("查看一周、四周、十二周、一年的统计数据")
    @pytest.mark.parametrize('date', [7 * 1, 7 * 4, 7 * 12, 1])
    def test_data_analysis_api(self, date):
        res = DataAnalysis().data_analysis(date)

        check.equal(res['code'], 200)

    @allure.story("数据分析")
    @allure.title("查看账号全部的统计数据")
    def test_total_data_analysis(self):
        res = DataAnalysis().total_data_analysis()

        check.equal(res['code'], 200)

    @allure.story("数据记录")
    @allure.title("查看一周、四周、十二周、一年的骑行记录")
    @pytest.mark.parametrize('date', [7 * 1, 7 * 4, 7 * 12, 1])
    def test_data_detail_api(self, date):
        res = DataAnalysis().detail_analysis(date)

        check.equal(res['code'], 200)

    @allure.story("数据记录")
    @allure.title("查看账号全部的骑行记录")
    def test_total_detail_analysis(self):
        res = DataAnalysis().total_detail_analysis()

        check.equal(res['code'], 200)
