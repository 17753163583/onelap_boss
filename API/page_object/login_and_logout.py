from API.base_page.base_page import BasePage
from common.handle_md5 import md5_encrypt
from loguru import logger
from common.logger import log_decorator


class OnelapLogin(BasePage):
    def __init__(self):
        super().__init__()

    @log_decorator
    def login(self, username, passwd):
        api_name = 'onelap_login'
        passwd_md5 = md5_encrypt(passwd)
        body = {"account": str(username), "password": str(passwd_md5)}
        headers = self.api_params[api_name]['headers']
        response = self.post_request(api_name=api_name, headers=headers, data=body)

        if response.json()['code'] == 200:
            logger.info(f'登录成功，获取{username}用户信息成功')
        else:
            logger.error(f'登录失败，用户名为：{username}，密码为：{passwd}')

        login_token = str(response.json()['data']['token'])
        logger.info(f"记录token：{login_token}")
        return response.json()

    @log_decorator
    def check_passwd(self, passwd):
        api_name = 'check_passwd'
        passwd_md5 = md5_encrypt(passwd)

        headers = self.api_params[api_name]['headers']
        headers['Authorization'] = self.onelap_login_res['data']['token']
        body = {"password": passwd_md5}

        response = self.post_request(api_name, headers=headers, data=body)

        if response.json()['code'] == 200:
            logger.info("密码校验成功")

        return response.json()

    @log_decorator
    # 注销账号的GET请求
    def account_cancellation(self):
        api_name = 'account_cancellation'
        headers = self.api_params['account_cancellation']['headers']
        headers['Authorization'] = self.onelap_login_res['data']['token']

        response = self.get_request(api_name=api_name, headers=headers)
        if response.json()['code'] == 200:
            logger.info("账号注销申请提交成功，七天内无登录，则注销成功。")
        return response.json()


if __name__ == '__main__':
    x = OnelapLogin()
    x.login('13001723386', 'zhang107.')
    x.check_passwd(x.onelap_account_dict['account_1']['password'])
    x.account_cancellation()
