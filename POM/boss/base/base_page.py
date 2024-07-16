import json
import selenium.common.exceptions
from loguru import logger
from selenium import webdriver
from common.get_path import project_path
from common.find_ele import find_ele
from common.get_yaml import GetYamlData
from common.get_boss_login_cookies import get_login_cookies
from selenium.webdriver.chrome.service import Service
import requests


class BossBasePage(GetYamlData):
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(project_path() + "/conf/chromedriver_126.0.6478.126.exe"))
        self.boss_element = GetYamlData.get_boss_element_data()

        self.test_onelap_account_dict = GetYamlData().get_login_accounts()['onelap_account']
        self.test_boss_account_dict = GetYamlData().get_login_accounts()['boss_account']
        self.onelap_api_param = GetYamlData.get_onelap_api_param_data()

    def get_url(self, page_name):
        login_url = self.boss_element[page_name]['url']
        self.driver.get(login_url)
        logger.info(f'{page_name}页面跳转')

    def save_boss_cookies_to_json(self):
        dict_cookies = self.driver.get_cookies()
        logger.info("读取Cookies成功")

        json_cookies = json.dumps(dict_cookies)
        with open(project_path() + "/POM/boss/test_data/boss_login_cookies.json", 'w') as file:
            file.write(json_cookies)
            logger.info("保存cookies至boss_login_cookies.json")

        # self.driver.delete_all_cookies()

    def login_with_cookie(self):
        self.get_url('login')

        self.driver.delete_all_cookies()
        logger.info("清理Cookies")

        cookies = get_login_cookies()
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        logger.info("导入cookies")

        self.driver.refresh()

        if self.driver.current_url == self.boss_element['home']['url']:
            logger.info(f"跳转{self.driver.current_url}")
        else:
            logger.error(f"跳转{self.boss_element['home']['url']}失败")

    def element_locator(self, page_name, element_name):
        locator_message = self.boss_element[page_name][element_name]

        find_type = locator_message['type']
        find_key = locator_message['key']
        element_locator = find_ele(self.driver, find_type, find_key)
        if element_locator:
            logger.info(f'{page_name}_{element_name}定位成功')
            return element_locator

    def element_locator_sendkeys(self, page_name, element_name, input_data=None):
        locator_message = self.boss_element[page_name][element_name]

        find_type = locator_message['type']
        find_key = locator_message['key']

        element_locator = find_ele(self.driver, find_type, find_key)
        if element_locator:
            logger.info(f'{page_name}_{element_name}定位成功')
        else:
            logger.error(f'{page_name}_{element_name}定位失败')
            return

        element_locator_sendkeys = element_locator.send_keys(input_data)
        logger.info(f'{page_name}_{element_name}输入数据：{input_data}成功')

        return element_locator_sendkeys

    def switch_to_alert_accept(self):
        try:
            self.driver.switch_to.alert.accept()
            logger.info("alert弹窗处理")
        except selenium.common.exceptions.NoAlertPresentException as error:
            logger.error(f"切换alert弹窗失败：{error}")

        # 顺应开发实现
        self.driver.refresh()

    def add_report_message_with_request_post(self, page_name, headers, data):
        report_url = self.onelap_api_param[page_name]['url']

        response = requests.post(report_url, headers=headers, data=data)

        try:
            assert response.status_code == 200
        except AssertionError as error:
            logger.error(f"添加举报信息失败,错误信息为:{error}")

        report_id = response.json()['data']['report_id']
        self.login_with_cookie()

        try:
            assert self.driver.current_url == 'https://boss-informal.rfsvr.net/'
            logger.info("跳转home页")
        except AssertionError as error:
            logger.error(f"跳转home页失败：{error}")

        # report_id = self.add_report_message_with_request_post('report', self.headers, self.data)

        report_id_url = self.boss_element['report']['url'] + f'?report_id={report_id}'

        try:
            self.driver.get(report_id_url)
            assert (self.driver.current_url ==
                    f"https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id={report_id}")
            logger.info(f'跳转{report_id_url}')
        except AssertionError as error:
            logger.error(f"跳转{report_id_url}失败：{error}")


if __name__ == '__main__':
    print(BossBasePage().test_boss_account_dict)
