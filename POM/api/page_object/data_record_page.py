import requests
from loguru import logger

from POM.api.base_page.base_page import BasePage
from common.get_time_stamp import get_month_last_day
from common.logger import log_decorator


class DataRecordPage(BasePage):
    def __init__(self):
        super().__init__()
        self.page_name = 'data_record_page'
        self.onelap_token = self.onelap_login_res['data']['token']
        self.type_list = list(self.api_params['type_list'].keys())

        self.data_record = self.get_data_record_list(type_num=0)
        self.days_list = list(self.data_record['data']['days'].keys())
        # 删除当前列表中最后一天的第一天记录
        self.del_record_id = self.data_record['data']['days'][self.days_list[-1]]['info'][0]['did']
        self.record_id = self.data_record['data']['days'][self.days_list[0]]['info'][0]['did']

    @log_decorator
    def get_data_record_list(self, type_num):
        api_name = 'data_record_list'
        params = self.api_params[self.page_name][api_name]['params']
        params['from'] = get_month_last_day()
        params['data_type'] = self.type_list[type_num]

        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.onelap_token

        res = self.get_request(page_name=self.page_name, api_name=api_name, params=params, headers=headers).json()

        try:
            record_record_days_list = list(res['data']['days'].keys())
            tag_list = []
            for day in record_record_days_list:
                for info in res['data']['days'][day]['info']:
                    tag_list.append(info['tag'])

        except AttributeError:
            logger.error(f"当前类型下，数据记录为空")
            return None

        return res

    @log_decorator
    def change_record_name_and_type(self, name, data_type):
        api_name = 'change_data_name_type'
        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.onelap_token

        name_data = self.api_params[self.page_name][api_name]['name_data']
        name_data['alias_name'] = name
        name_data['did'] = self.record_id

        type_data = self.api_params[self.page_name][api_name]['type_data']
        type_data['custom_type'] = data_type
        type_data['did'] = self.record_id

        res_name = self.post_request(page_name=self.page_name, api_name=api_name, headers=headers, data=name_data)
        logger.info(f"修改记录名称：{res_name.json()}")

        res_type = self.post_request(page_name=self.page_name, api_name=api_name, headers=headers, data=type_data)
        logger.info(f"修改记录类型：{res_type.json()}")

        return res_name.json(), res_type.json()

    @log_decorator
    def del_data_record(self):
        if self.del_record_id:
            logger.info(f"读取待删除记录id：{self.del_record_id}")
        url = f'http://rfs-fitness-informal.rfsvr.net/indoor/v1/app/record/del/{self.del_record_id}'
        headers = {
            'Authorization': self.onelap_token,
            'Content-Type': 'application/json'
        }
        res = requests.post(url=url, headers=headers)
        logger.info(f"删除记录结果：{res.json()['error']}")
        return res.json()


if __name__ == '__main__':
    x = DataRecordPage()
    x.del_data_record()
    # x.change_record_name_and_type(name='测试修改', data_type=x.type_list[3])

    # print(DataRecordPage().get_data_record_list(BasePage().api_params['data_record_list']['data_type'][0]))
