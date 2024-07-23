import json

import os

import allure
import pytest
import pytest_check as check
from loguru import logger

from common.get_yaml import GetYamlData
from POM.boss.page_object.login_page import LoginPageBoss
from POM.boss.page_object.report_page import Report
from POM.boss.page_object.report_result_page import ReportResult
from common.get_path import publish_json_path

boss_login_account_dict = GetYamlData().get_login_accounts()["boss_account"]


@allure.feature("Boss账号相关")
class TestLogin:
    @allure.story("登录成功")
    @pytest.mark.parametrize("boss_account_dict", boss_login_account_dict)
    def test_login_right(self, boss_account_dict):
        with allure.step("输入账号密码并点击登录"):
            login_url, current_url = LoginPageBoss().enter_account(
                username=boss_login_account_dict[boss_account_dict]["username"],
                password=boss_login_account_dict[boss_account_dict]["password"])

            with allure.step("对地址断言，判断页面是否跳转"):
                check.not_equal(login_url, current_url, "登录成功")

    @allure.story("登录失败")
    def test_login_error(self):
        login_url, current_url = LoginPageBoss().enter_account_error()

        check.equal(login_url, current_url, "登录失败")


@allure.feature("Boss举报功能")
class TestReport:
    @staticmethod
    def setup_class():
        json_path = publish_json_path()
        if os.path.exists(json_path):
            os.remove(json_path)
            logger.info("检测到惩罚json文件已存在，删除成功")

        json_data_dict = {
            "is_forbid_speak": [],
            "is_forbid_speak_list": [],
            "is_forbid_login": [],
            "is_forbid_login_list": []
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data_dict, f)
            logger.info("惩罚信息json文件新建成功")

    @allure.story("举报失败")
    @allure.title("审核不通过")
    def test_review_failure(self):
        res = Report().report_review_failure()

        check.equal(res, "审核未通过")

    @allure.story("举报成功")
    @allure.title("通知警告")
    def test_review_warning(self):
        status, method = Report().report_review_pass_warning()

        check.equal(status, "审核通过")
        check.equal(method, "通知警告")

    @allure.story("举报成功")
    @allure.title("禁言1小时")
    def test_review_forbid_speak_hours(self):
        status, method = Report().report_review_pass_forbid_speak_hours()

        check.equal(status, "审核通过")
        check.equal(method, "禁言1小时")

    @allure.story("举报成功")
    @allure.title("封号1小时")
    def test_review_forbid_login_hours(self):
        status, method = Report().report_review_pass_forbid_login_hours()

        check.equal(status, "审核通过")
        check.equal(method, "封号1小时")


@allure.feature("Boss举报结果处理功能")
class TestReportResult:
    @allure.story("惩罚记录同步")
    @allure.title("检查禁言的惩罚记录同步到举报处理结果页面")
    def test_is_forbid_speak_exist(self):
        res = ReportResult().check_report_result_sheet("is_forbid_speak")

        check.is_true(res, "检查禁言惩罚记录是否添加到处理结果列表页")

    @allure.story("惩罚记录同步")
    @allure.title("检查封号的惩罚记录同步到举报处理结果页面")
    def test_is_forbid_login_exist(self):
        res = ReportResult().check_report_result_sheet("is_forbid_speak")

        check.is_true(res, "检查封号惩罚记录是否添加到处理结果列表页")

    @allure.story("撤销惩罚")
    @allure.title("撤销封号惩罚")
    def test_cancel_speak_publish(self):
        res = ReportResult().cancel_forbid_publish("is_forbid_login")

        check.equal(res["code"], 200)

    @allure.story("撤销惩罚")
    @allure.title("撤销禁言惩罚")
    def test_cancel_login_publish(self):
        res = ReportResult().cancel_forbid_publish("is_forbid_speak")

        check.equal(res["code"], 200)
