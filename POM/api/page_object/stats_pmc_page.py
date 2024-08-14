import json

from POM.api.base_page.base_page import BasePage

from common.get_time_stamp import get_today_start_stamp, get_pre_days_time_stamp, get_pre_year_time_stamp, \
    get_total_time_stamp
from common.logger import log_decorator
from loguru import logger


class Status(BasePage):
    def __init__(self):
        super().__init__()
        self.page_name = 'stats_pmc_page'
        self.onelap_token = self.onelap_login_res['data']['token']

    @log_decorator
    def data_analysis(self, nums):
        api_name = 'data_analysis'
        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.onelap_token

        params = self.api_params[self.page_name][api_name]['params']

        if nums == 1:
            params['start_time'], params['end_time'] = get_pre_year_time_stamp()
            print(params)
        else:
            params['start_time'], params['end_time'] = get_pre_days_time_stamp(nums)

        response_analysis = self.get_request(page_name=self.page_name, api_name=api_name, headers=headers,
                                             params=params)

        return response_analysis.json()

    @log_decorator
    def detail_analysis(self, nums):
        api_name = 'detail_analysis'
        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.onelap_token

        params = self.api_params[self.page_name][api_name]['params']

        if nums == 1:
            params['type'] = 'm'
            params['start_time'], params['end_time'] = get_pre_year_time_stamp()
            print(params)
        else:
            params['type'] = 'd'
            params['start_time'], params['end_time'] = get_pre_days_time_stamp(nums)

        response_records = self.get_request(page_name=self.page_name, api_name=api_name, headers=headers,
                                            params=params)

        return response_records.json()

    @log_decorator
    def total_data_analysis(self):
        api_name = 'detail_analysis'
        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.onelap_token

        params = self.api_params[self.page_name][api_name]['params']
        params['start_time'], params['end_time'] = (0, 0)

        response_analysis = self.get_request(page_name=self.page_name, api_name=api_name, headers=headers,
                                             params=params)

        return response_analysis.json()

    @log_decorator
    def total_detail_analysis(self):
        api_name = 'more_user_info'
        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.onelap_token

        response_more_info = self.get_request(page_name=self.page_name, api_name=api_name, headers=headers).json()
        start_ride_time_stamp = response_more_info['data']['start_ride_at']

        params = self.api_params[self.page_name][api_name]['params']
        params['start_time'], params['end_time'] = get_total_time_stamp(start_ride_time_stamp)
        response_records = self.get_request(page_name=self.page_name, api_name=api_name, headers=headers, params=params)

        return response_records.json()

    @log_decorator
    def best_record(self):
        api_name = 'max_user_info'
        headers = self.api_params['home_page'][api_name]['headers']
        headers['Authorization'] = self.onelap_token

        response = self.get_request(page_name='home_page', api_name=api_name, headers=headers)
        if response.json()['code'] == 200:
            logger.info("账号信息读取成功")
            if response.json()['data']['record']:
                logger.info("账号最佳记录获取成功")
        else:
            logger.error("账号信息读取失败")
        return response.json()


class PMC(BasePage):
    def __init__(self):
        super().__init__()
        self.page_name = 'stats_pmc_page'
        self.onelap_token = self.onelap_login_res['data']['token']

    def calendar_interact(self):
        api_name = "exercise_plan"
        params = self.api_params[self.page_name][api_name]['params']
        headers = self.api_params[self.page_name][api_name]['headers']

        headers['Authorization'] = self.onelap_token

        response = self.get_request(page_name=self.page_name, api_name=api_name, params=params, headers=headers)
        return response.json()

    def pmc_data(self):
        api_name = "pmc_data_show"
        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.onelap_token

        response = self.get_request(page_name=self.page_name, api_name=api_name, headers=headers)
        return response.json()

    def create_personal_plan(self):
        api_name = "pmc_add_plan"
        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.onelap_token
        data = {"date": get_today_start_stamp(), "type": 2, "wid": 51451}

        response = self.post_request(page_name=self.page_name, api_name=api_name, headers=headers,
                                     data=json.dumps(data))
        return response.json()


if __name__ == '__main__':
    print(PMC().create_personal_plan())
