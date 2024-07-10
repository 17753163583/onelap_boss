from API.base_page.base_page import BasePage

from common.get_time_stamp import get_pre_days_time_stamp, get_pre_year_time_stamp, get_total_time_stamp
from common.logger import log_decorator


class DataAnalysis(BasePage):
    def __init__(self):
        super().__init__()
        self.data_api_name = 'data_analysis'
        self.detail_api_name = 'detail_analysis'
        self.more_info_api_name = 'more_user_info'

    @log_decorator
    def data_analysis(self, nums):
        headers = self.api_params[self.data_api_name]['headers']
        headers['Authorization'] = self.onelap_login_res['data']['token']

        params = self.api_params[self.data_api_name]['params']

        if nums == 1:
            params['start_time'], params['end_time'] = get_pre_year_time_stamp()
            print(params)
        else:
            params['start_time'], params['end_time'] = get_pre_days_time_stamp(nums)

        response_analysis = self.get_request(api_name=self.data_api_name, headers=headers, param=params)

        return response_analysis.json()

    @log_decorator
    def detail_analysis(self, nums):
        headers = self.api_params[self.detail_api_name]['headers']
        headers['Authorization'] = self.onelap_login_res['data']['token']

        params = self.api_params[self.detail_api_name]['params']

        if nums == 1:
            params['type'] = 'm'
            params['start_time'], params['end_time'] = get_pre_year_time_stamp()
            print(params)
        else:
            params['type'] = 'd'
            params['start_time'], params['end_time'] = get_pre_days_time_stamp(nums)

        response_records = self.get_request(api_name=self.detail_api_name, headers=headers,
                                            param=params)

        return response_records.json()

    @log_decorator
    def total_data_analysis(self):
        headers = self.api_params[self.detail_api_name]['headers']
        headers['Authorization'] = self.onelap_login_res['data']['token']

        params = self.api_params[self.detail_api_name]['params']
        params['start_time'], params['end_time'] = (0, 0)

        response_analysis = self.get_request(api_name=self.data_api_name, headers=headers,
                                             param=params)

        return response_analysis.json()

    @log_decorator
    def total_detail_analysis(self):
        headers = self.api_params[self.more_info_api_name]['headers']
        headers['Authorization'] = self.onelap_login_res['data']['token']
        response_more_info = self.get_request(self.more_info_api_name, headers=headers).json()
        start_ride_time_stamp = response_more_info['data']['start_ride_at']

        params = self.api_params[self.data_api_name]['params']
        params['start_time'], params['end_time'] = get_total_time_stamp(start_ride_time_stamp)
        response_records = self.get_request(api_name=self.detail_api_name, headers=headers,
                                            param=params)

        return response_records.json()


if __name__ == '__main__':
    x = DataAnalysis()
    print(x.data_analysis(7))
    print(x.data_analysis(7*4))
    print(x.data_analysis(7*12))
    print(x.data_analysis(1))
    print(x.detail_analysis(1))
    print(x.total_data_analysis())
    print(x.total_detail_analysis())
