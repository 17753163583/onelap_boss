from loguru import logger
import json
from POM.api.base_page.base_page import BasePage
from common.logger import log_decorator


class PlantPage(BasePage):
    def __init__(self):
        super().__init__()
        self.page_name = 'plat_workshop'
        self.headers = {'Authorization': self.onelap_login_res['data']['token']}

    @log_decorator
    def plant_sweepstakes(self):
        api_name = 'plant_sweepstakes'

        res = self.post_request(page_name=self.page_name, api_name=api_name, headers=self.headers)
        # code = 411 , 星币不足
        return res.json()

    @log_decorator
    def show_my_submission(self):
        api_name = 'show_submission_list'

        res = self.get_request(page_name=self.page_name, api_name=api_name, headers=self.headers)
        return res.json()['data']['info']

    @log_decorator
    def add_submission(self):
        api_name = 'add_submission'

        data = self.api_params[self.page_name][api_name]['data']
        res = self.post_request(page_name=self.page_name, api_name=api_name, headers=self.headers,
                                data=json.dumps(data))
        if res.json()['code'] == 200:
            logger.info(f"add submission success")
            return res.json()['data']['id']
        else:
            logger.error(f"add submission failed")
            return res.json()

    @log_decorator
    def remove_submission(self):
        api_name = 'remove_submission'

        data = self.api_params[self.page_name][api_name]['data']
        data['pid'] = self.add_submission()

        res = self.post_request(page_name=self.page_name, api_name=api_name, headers=self.headers, data=data)
        return res.json()

    @log_decorator
    def show_rank_list(self):
        api_name = 'Q_plant_rank'

        res = self.get_request(page_name=self.page_name, api_name=api_name, headers=self.headers)
        return res.json()['data']

    @log_decorator
    def show_rank_record_list(self):
        api_name = 'rank_record'

        res = self.get_request(page_name=self.page_name, api_name=api_name, headers=self.headers)
        return res.json()['data']

    @log_decorator
    def show_radio_list(self):
        api_name = 'show_radio_station'

        res = self.get_request(page_name=self.page_name, api_name=api_name, headers=self.headers)
        return res.json()['data']

    @log_decorator
    def add_radio_station(self):
        api_name = 'add_radio_interaction'
        data = self.api_params[self.page_name][api_name]['data']

        data['pid'] = self.show_radio_list()['info'][0]['id']
        res = self.post_request(page_name=self.page_name, api_name=api_name, headers=self.headers, data=data)
        return res.json()

    @log_decorator
    def remove_radio_station(self):
        api_name = 'remove_radio_interaction'
        data = self.api_params[self.page_name][api_name]['data']

        data['pid'] = self.show_radio_list()['info'][0]['id']
        res = self.post_request(page_name=self.page_name, api_name=api_name, headers=self.headers, data=data)
        return res.json()

    @log_decorator
    def add_submission_text_img(self):
        api_name = 'img_text_submission'
        data = self.api_params[self.page_name][api_name]['data']
        res = self.post_request(page_name=self.page_name, api_name=api_name, headers=self.headers,
                                data=json.dumps(data))
        return res.json()

    # {'code': 200, 'error': 'Success', 'data': {'id': '66b48b020715501d967302d6'}}
    @log_decorator
    def rank_list(self, is_week, is_national):
        api_name = 'rank_list'
        params = self.api_params[self.page_name][api_name]['params']
        params['is_week'] = is_week
        params['is_national'] = is_national

        res = self.get_request(page_name=self.page_name, api_name=api_name, headers=self.headers, params=params)
        return res.json()['data']['rankList']

    @log_decorator
    def rank_list_share(self, platform):
        page_name = 'home_page'
        api_name = 'medal_record_share'
        data = self.api_params[page_name][api_name]['data']
        data['platform'] = platform
        res = self.post_request(page_name=page_name, api_name=api_name, headers=self.headers, data=data)
        return res.json()


if __name__ == '__main__':
    x = PlantPage()
    x.rank_list_share(1)
"""
        # 审核状态分类
        # 1:审核中 2:审核不通过 4:已发布

        list_dict = x.show_my_submission()
        a = {1: [], 2: [], 4: []}
        for dict_data in list_dict:
            a[dict_data['status']].append(dict_data['id'])
        print(a)
"""
"""
    print(x.remove_radio_station())
    print(x.show_radio_list()['info'][0]['expressions']['front_user'][0]['uid'])
    print(x.add_radio_station())
    print(x.show_radio_list()['info'][0]['expressions']['front_user'][0]['uid'])

"""
