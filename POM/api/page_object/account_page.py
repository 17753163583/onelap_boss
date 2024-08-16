from POM.api.base_page.base_page import BasePage
from common.handle_md5 import md5_encrypt
from loguru import logger
from common.logger import log_decorator


class OnelapLogin(BasePage):
    def __init__(self):
        super().__init__()
        self.page_name = 'account_page'

    @log_decorator
    def login(self, username, passwd):
        # 登录
        api_name = 'onelap_login'
        passwd_md5 = md5_encrypt(passwd)
        body = {"account": str(username), "password": str(passwd_md5)}
        headers = self.api_params[self.page_name][api_name]['headers']
        response = self.post_request(page_name=self.page_name, api_name=api_name, headers=headers, data=body)

        if response.json()['code'] == 200:
            logger.info(f'登录成功，获取{username}用户信息成功')
        else:
            logger.error(f'登录失败，用户名为：{username}，密码为：{passwd}')
            return False

        login_token = str(response.json()['data']['token'])
        logger.info(f"记录token：{login_token}")
        return response.json()

    @log_decorator
    def check_passwd(self, passwd):
        api_name = 'check_passwd'
        passwd_md5 = md5_encrypt(passwd)

        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.onelap_login_res['data']['token']
        body = {"password": passwd_md5}

        response = self.post_request(page_name=self.page_name, api_name=api_name, headers=headers, data=body)

        if response.json()['code'] == 200:
            logger.info("密码校验成功")

        return response.json()

    @log_decorator
    # 注销账号的GET请求
    def account_cancellation(self):
        api_name = 'account_cancellation'
        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.onelap_login_res['data']['token']

        response = self.get_request(page_name=self.page_name, api_name=api_name, headers=headers)
        if response.json()['code'] == 200:
            logger.info("账号注销申请提交成功，七天内无登录，则注销成功。")
        return response.json()


if __name__ == '__main__':
    x = OnelapLogin()
    x.login('17753163583', 'zhang107')

    x.check_passwd('zhang107.')
    x.account_cancellation()
    x.login('17753163583', 'zhang107')
