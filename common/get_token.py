import requests
from common.get_yaml import GetYamlData
from common.find_ele import find_ele

from loguru import logger


class GetToken:
    def __init__(self):
        self.onelap_login_url = 'https://rfs-fitness-informal.rfsvr.net/api/account/v1/login'
        self.onelap_login_body = {"account": "17753163583", "password": "dc158e485dba3cb7a6cfc9063568ac9e"}

    def get_onelap_login_token(self):
        response = requests.post(self.onelap_login_url, data=self.onelap_login_body)
        onelap_login_token = response.json()['data']['token']
        logger.info("获取onelap登录token")
        return onelap_login_token

    @staticmethod
    def get_boss_login_button_token(driver):
        login_token_data = GetYamlData.get_boss_element_data()['login']['hidden_token']

        find_type = login_token_data['type']
        find_key = login_token_data['key']

        element_locator = find_ele(driver, find_type, find_key)
        boss_login_button_token = element_locator.get_attribute("value")

        logger.info('获取boss_login_button_token获取成功')

        return boss_login_button_token
