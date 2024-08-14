import json

from loguru import logger

from POM.api.base_page.base_page import BasePage
from common.logger import log_decorator


class HomePage(BasePage):
    def __init__(self):
        super().__init__()
        self.onelap_token = self.onelap_login_res['data']['token']
        self.page_name = "home_page"

    @log_decorator
    def personal_info(self):
        api_name = 'max_user_info'
        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.onelap_token

        response = self.get_request(page_name=self.page_name, api_name=api_name, headers=headers)
        if response.json()['code'] == 200:
            logger.info("账号信息读取成功")
        return response.json()['data']['experience_info'], response.json()['data']['social_info']

    @log_decorator
    def accrued_data(self):
        api_name = "accrued_data"
        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.onelap_token

        response = self.get_request(page_name=self.page_name, api_name=api_name, headers=headers)
        return response.json()['data']['record_stats']

    @log_decorator
    def medal_share(self, platform):
        api_name = "medal_record_share"
        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.onelap_token

        data = self.api_params[self.page_name][api_name]['data']
        data['platform'] = platform
        response = self.post_request(page_name=self.page_name, api_name=api_name, headers=headers, data=data)
        logger.info("勋章分享")

        return response.json()

    @log_decorator
    def best_record_share(self, platform):
        api_name = "medal_record_share"
        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.onelap_token

        data = self.api_params[self.page_name][api_name]['data']
        data['platform'] = platform
        data['category'] = 3

        response = self.post_request(page_name=self.page_name, api_name=api_name, headers=headers, data=data)
        logger.info("最佳记录分享")

        return response.json()


if __name__ == '__main__':
    x = HomePage()
    x.personal_info()
    x.accrued_data()
    x.medal_share(platform=1)
    x.best_record_share(platform=1)
