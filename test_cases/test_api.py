import allure
import pytest
import pytest_check as check

from POM.api.base_page.base_page import BasePage
from POM.api.page_object.account_page import OnelapLogin
from POM.api.page_object.stats_pmc_page import Status, PMC
from POM.api.page_object.home_page import HomePage
from POM.api.page_object.personal_homepage import PersonalHomePage
from POM.api.page_object.data_record_page import DataRecordPage

onelap_account_dict = BasePage().onelap_account_dict


@allure.feature("账号相关")
class TestOnelapAccount:
    def setup_class(self):
        self.login_page = OnelapLogin()

    @allure.story("账号登录")
    @allure.title("输入正确的账号密码，登录成功")
    @pytest.mark.parametrize("account_num", onelap_account_dict)
    def test_login_pass(self, account_num):
        account = onelap_account_dict[account_num]
        res = self.login_page.login(account['username'], account['password'])

        check.equal(res['code'], 200)

    @allure.story("账号登录")
    @allure.title("输入错误的账号密码，登录失败")
    def test_login_fail(self):
        res = self.login_page.login(onelap_account_dict['account_1']['username'], '123')

        check.is_false(res)

    @allure.story("账号注销")
    @allure.title("密码核验接口")
    def test_check_passwd(self):
        res = self.login_page.check_passwd(onelap_account_dict['account_1']['password'])

        check.equal(res['code'], 200)

    @allure.story("账号注销")
    @allure.title("账号注销接口")
    def test_account_cancellation(self):
        res = self.login_page.account_cancellation()

        check.equal(res['code'], 200)


@allure.feature("首页")
class TestOnelapHome:
    def setup_class(self):
        self.home_page = HomePage()

    @allure.story("个人信息")
    @allure.title("个人信息数据")
    def test_personal_info(self):
        experience_info, social_info = self.home_page.personal_info()

        with allure.step("等级经验值"):
            check.is_true([experience_info['experience'], experience_info['level']])
        with allure.step("粉丝、关注、获赞"):
            check.is_true([social_info['fans_count'], social_info['friend_count'], social_info['like_count']])

    @allure.story("个人信息")
    @allure.title("累计数据")
    def test_cumulative_data(self):
        cumulative_data = self.home_page.accrued_data()
        with allure.step("累计骑行"):
            check.is_true(cumulative_data['days'])
        with allure.step("累计消耗"):
            check.is_true(cumulative_data['cal'])

    @allure.story("分享")
    @allure.title("最佳记录分享")
    @pytest.mark.parametrize('platform', range(1, 5))
    def test_share_best_record(self, platform):
        res = self.home_page.best_record_share(platform)

        check.equal(res['code'], 200)

    @allure.story("分享")
    @allure.title("勋章分享")
    @pytest.mark.parametrize('platform', range(1, 5))
    def test_medal_share(self, platform):
        res = self.home_page.medal_share(platform)

        check.equal(res['code'], 200)


@allure.feature("个人主页")
class TestOnelapPersonHome:
    def setup_class(self):
        self.person_page = PersonalHomePage()

    @allure.story("个人信息")
    @allure.title("等级、社交、地区、ftp、功体比")
    def test_person_info(self):
        user_info = self.person_page.user_info()['data']

        area_info = user_info['area']['data']
        experience_info = user_info['experience_info']
        home_info = user_info['userInfo']
        ftp_info = user_info['FTP']['data']
        wkg_info = user_info['wkg']['data']

        with allure.step("地区"):
            check.is_true([area_info['city'], area_info['province']])
        with allure.step("等级、经验"):
            check.is_true([experience_info['experience'], experience_info['level']])
        with allure.step("关注、粉丝、访问、获赞"):
            check.is_true([home_info['friend_count'],
                           home_info['fans_count'],
                           home_info['views_count'],
                           home_info['like_count']])
        with allure.step("ftp"):
            check.is_true(ftp_info)
        with allure.step("功体比"):
            check.is_true(wkg_info)

    @allure.story("个人信息")
    @allure.title("关注")
    def test_follow_others(self):
        res = self.person_page.follow_others()

        check.equal(res['code'], 200)

    @allure.story("个人信息")
    @allure.title("点赞")
    def test_like_others(self):
        res = self.person_page.like_others()

        check.equal(res['code'], 200)

    @allure.story("个人信息")
    @allure.title("修改地区和ftp")
    def test_change_area_and_ftp(self):
        res_area, res_ftp = self.person_page.change_area_and_ftp()

        check.equal(res_area['code'], 200)
        check.equal(res_ftp['code'], 200)

    @allure.story("个人数据")
    @allure.title("近七天的骑行数据")
    def test_7_days_ride(self):
        seven_data, _ = self.person_page.check_ride_data()

        check.equal(len(seven_data['data']['days']), 7)

    @allure.story("个人数据")
    @allure.title("总骑行数据分析")
    def test_total_analysis(self):
        _, total_data_analysis = self.person_page.check_ride_data()

        check.is_true(total_data_analysis['data'])


@allure.feature("统计+PMC")
class TestOnelapAnalysisPMC:
    def setup_class(self):
        self.analysis_page = Status()
        self.pmc_page = PMC()

    @allure.story("数据分析")
    @allure.title("查看一周、四周、十二周、一年的统计数据")
    @pytest.mark.parametrize('date', [7 * 1, 7 * 4, 7 * 12, 1])
    def test_data_analysis_api(self, date):
        res = self.analysis_page.data_analysis(date)

        check.equal(res['code'], 200)

    @allure.story("数据分析")
    @allure.title("查看账号全部的统计数据")
    def test_total_data_analysis(self):
        res = self.analysis_page.total_data_analysis()

        check.equal(res['code'], 200)

    @allure.story("数据记录")
    @allure.title("查看一周、四周、十二周、一年的骑行记录")
    @pytest.mark.parametrize('date', [7 * 1, 7 * 4, 7 * 12, 1])
    def test_data_detail_api(self, date):
        res = self.analysis_page.detail_analysis(date)

        check.equal(res['code'], 200)

    @allure.story("数据记录")
    @allure.title("查看账号全部的骑行记录")
    def test_total_detail_analysis(self):
        res = self.analysis_page.total_detail_analysis()

        check.equal(res['code'], 200)

    @allure.story("最佳记录")
    @allure.title("最佳记录数据")
    def test_best_record(self):
        res = self.analysis_page.best_record()['data']['record']
        best_record_keys = res.keys()

        check.equal(len(best_record_keys), 6)

    @allure.story("PMC")
    @allure.title("日历板块交互")
    def test_calendar_interact(self):
        res = self.pmc_page.calendar_interact()

        check.equal(res['code'], 200)

    @allure.story("PMC")
    @allure.title("PMC页面数据展示")
    def test_data_show(self):
        res = self.pmc_page.pmc_data()

        check.equal(res['code'], 200)

    @allure.story("PMC")
    @allure.title("创建个人计划")
    def test_create_personal_plan(self):
        res = self.pmc_page.create_personal_plan()

        check.equal(res['code'], 200)


@allure.feature("数据记录")
class TestDataRecord:
    def setup_class(self):
        self.data_page = DataRecordPage()

    @allure.story("数据筛选")
    @allure.title("分类型筛选")
    @pytest.mark.parametrize("type_num", range(1, 7))
    def test_record_filter(self, type_num):
        type_text = ['比赛', '骑行训练', '路线训练', '通勤', '测试']
        res = self.data_page.get_data_record_list(type_num)

        if res is not None:
            record_record_days_list = list(res['data']['days'].keys())
            tag_list = []
            for day in record_record_days_list:
                for info in res['data']['days'][day]['info']:
                    tag_list.append(info['tag'])
            for tag in tag_list:
                if type_num == 6:
                    check.is_not_in(tag, type_text)
                else:
                    check.equal(tag, type_text[type_num - 1])
        else:
            check.is_none(res)

    @allure.story("删除数据")
    @allure.title("删除一条数据")
    def test_delete_one_record(self):
        res = self.data_page.del_data_record()
        check.equal(res['error'], 'success')
