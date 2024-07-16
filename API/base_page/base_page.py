import requests
from common.get_yaml import GetYamlData
from common.get_token import GetToken
from loguru import logger


class BasePage(GetYamlData):
    def __init__(self):
        self.api_params = self.get_onelap_api_param_data()
        self.onelap_account_dict = self.get_login_accounts()['onelap_account']
        self.onelap_login_res = GetToken().onelap_login(self.onelap_account_dict['account_1']['username'],
                                                        self.onelap_account_dict['account_1']['password'])

    def post_request(self, api_name, headers=None, data=None):
        url = self.api_params[api_name]['url']
        try:
            response = requests.post(url=url, headers=headers, data=data)
            logger.info(f"发送POST请求{url}成功")
            return response
        except Exception as error:
            logger.error(f"发送POST请求{url}失败:{error}")

    def get_request(self, api_name, param=None, headers=None):
        url = self.api_params[api_name]['url']
        try:
            response = requests.get(url, params=param, headers=headers)
            logger.info(f"发送GET请求{url}成功")
            return response
        except Exception as error:
            logger.error(f"发送GET请求{url}失败:{error}")


if __name__ == '__main__':
    print(BasePage().onelap_login_res['data']['token'])
