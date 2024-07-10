import requests
from common.get_yaml import GetYamlData
from common.find_ele import find_ele
from loguru import logger
from common.handle_md5 import md5_encrypt


class GetToken(GetYamlData):
    def __init__(self):
        self.boss_element = self.get_boss_element_data()
        self.onelap_api = self.get_onelap_api_param_data()

    def onelap_login(self, username, password):
        data = self.onelap_api['onelap_login']['data']
        data['account'] = username
        data['password'] = md5_encrypt(password)

        response = requests.post(url=self.onelap_api['onelap_login']['url'],
                                 headers=self.onelap_api['onelap_login']['headers'],
                                 data=data)

        if response.json()['code'] == 200:
            logger.info("获取onelap登录token")
            return response.json()
        elif response.json()['code'] == 204:
            logger.info("账号被限制登录")
            return response.json()

    def get_boss_login_button_token(self, driver):
        login_token_data = self.boss_element['login']['hidden_token']

        find_type = login_token_data['type']
        find_key = login_token_data['key']

        element_locator = find_ele(driver, find_type, find_key)
        boss_login_button_token = element_locator.get_attribute("value")

        logger.info('获取boss_login_button_token获取成功')

        return boss_login_button_token


if __name__ == '__main__':
    print(GetToken().onelap_login('13001723386', 'zhang107.'))
