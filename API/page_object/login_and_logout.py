from API.base_page.base_page import BasePage
from common.handle_md5 import md5_encrypt
from loguru import logger


class OnelapLogin(BasePage):
    def __init__(self):
        super().__init__()
        self.login_token = 0

    def login(self, username, passwd):
        api_name = 'onelap_login'
        passwd_md5 = md5_encrypt(passwd)
        body = {"account": str(username), "password": str(passwd_md5)}
        headers = self.api_params[api_name]['headers']
        response = self.post_request(api_name=api_name, headers=headers, data=body)

        self.login_token = str(response.json()['data']['token'])
        logger.info(f"记录token：{self.login_token}")
        return response

    def check_passwd(self, passwd):
        api_name = 'check_passwd'
        passwd_md5 = md5_encrypt(passwd)

        headers = self.api_params[api_name]['headers']
        headers['Authorization'] = self.login_token
        headers['UserId'] = '23842'
        body = {"password": passwd_md5}

        response = self.post_request(api_name, headers=headers, data=body)

        return response

    def account_cancellation(self):
        api_name = 'account_cancellation'
        headers = self.api_params['account_cancellation']['headers']
        headers['Authorization'] = self.login_token
        headers['UserId'] = '23842'

        response = self.get_request(api_name=api_name, headers=headers)

        return response
