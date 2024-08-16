import time

import requests
from loguru import logger
import json
from POM.api.base_page.base_page import BasePage
from common.logger import log_decorator


class RouteLibrary(BasePage):
    def __init__(self):
        super().__init__()
        self.page_name = 'route_library'
        self.headers = {'Authorization': self.onelap_login_res['data']['token']}
        self.test_route_id = self.get_route_library()['data']['list'][0]['book_id']

    @log_decorator
    def get_route_library(self):
        # 提供数据，无需测试
        api_name = 'route_list'
        params = self.api_params[self.page_name][api_name]['params']
        res = self.get_request(page_name=self.page_name, api_name=api_name, headers=self.headers, params=params)
        return res.json()

    @log_decorator
    def route_share(self, platform):
        # 路线分享,1~4
        api_name = 'route_share'
        data = self.api_params[self.page_name][api_name]['data']
        data['platform'] = platform
        res = self.post_request(page_name=self.page_name, api_name=api_name, headers=self.headers, data=data)
        return res.json()

    @log_decorator
    def route_filter(self):
        api_name = 'route_filter'
        params = self.api_params[self.page_name][api_name]['params']
        res = self.get_request(page_name=self.page_name, api_name=api_name, headers=self.headers, params=params)
        return res.json()

    @log_decorator
    def route_like(self):
        route_id = self.test_route_id
        url = f"http://rfs-fitness-informal.rfsvr.net/indoor/api/road_book/{route_id}/like"
        res = requests.post(url=url, headers=self.headers)
        return res.json()

    @log_decorator
    def route_favor(self):
        route_id = self.test_route_id
        url = f"http://rfs-fitness-informal.rfsvr.net/indoor/api/road_book/{route_id}/favor"
        res = requests.post(url=url, headers=self.headers)
        return res.json()

    @log_decorator
    def save_gpx_to_route_library(self):
        # 返回nid
        api_name = 'save_gpx'
        headers = self.headers
        headers['Content-Type'] = 'application/xml'
        gpx_file_path = '../test_data/test.gpx'

        with open(gpx_file_path, 'rb') as f:
            data = f.read()

        res = self.post_request(page_name=self.page_name, api_name=api_name, headers=headers, data=data)
        return res.json()

    @log_decorator
    def check_gpx_route(self):
        # 返回我创建的路线第一条路线的nid
        api_name = 'check_gpx_route'
        headers = self.headers
        res = self.get_request(page_name=self.page_name, api_name=api_name, headers=headers)
        return res.json()['data'][0]['nid']

    @log_decorator
    def get_record_id(self):
        # 查看支持转路线的记录列表，取第一条记录的id
        api_name = 'record_id'
        params = self.api_params[self.page_name][api_name]['params']
        res = self.get_request(page_name=self.page_name, api_name=api_name, headers=self.headers, params=params)
        return res.json()['data'][0]['id']

    @log_decorator
    def record_to_route(self):
        # 记录转路线
        api_name = 'record_to_route'
        data = self.api_params[self.page_name][api_name]['data']
        data['id'] = self.get_record_id()
        res = self.post_request(page_name=self.page_name, api_name=api_name, headers=self.headers, data=data)
        self.test_route_id = res.json()['data']['nid']
        return res.json()

    @log_decorator
    def send_comment_img_text(self):
        # 发送评论，带图片和文字
        # 测试时，评论和回复可以放一起
        route_id = self.test_route_id

        api_name = 'send_comment'
        data = self.api_params[self.page_name][api_name]['data']
        data['id'] = route_id

        headers = self.headers
        headers['Content-Type'] = 'application/json'

        res = self.post_request(page_name=self.page_name, api_name=api_name, headers=self.headers,
                                data=json.dumps(data))
        # 函数 send_comment_img_text 执行完成，函数返回结果：{'code': 200, 'error': 'Success', 'data': {'id': 771}}
        return res.json()['data']['id']

    @log_decorator
    def reply_comment_img_text(self):
        # 回复评论，带图片和文字
        comment_id = self.send_comment_img_text()
        # 间隔两s，否则无法回复成功
        time.sleep(2)
        url = f"http://rfs-fitness-informal.rfsvr.net/indoor/v1/app/comments/{comment_id}/replies"
        # url = "http://rfs-fitness-informal.rfsvr.net/indoor/v1/app/comments/779/replies"

        data = {"img": "uploads/20240816/files/1723792069165IMG_20240703141127997.jpg",
                "to_reply_id": 0,
                "to_uid": 0,
                "id": self.test_route_id,
                "text": "测试asd123.",
                "type": 1}

        headers = self.headers
        headers['Content-Type'] = 'application/json'

        res = requests.post(url=url, headers=headers, data=json.dumps(data))
        logger.info(f"发送POST请求{url}")
        return res.json()

    @log_decorator
    def map_to_route(self):
        # 地图创建路线
        with open("../test_data/test_map_route_data.json", encoding='utf-8') as file:
            data = json.load(file)

        api_name = 'map_to_route'
        headers = self.headers
        headers['Content-Type'] = 'application/json'
        res = self.post_request(page_name=self.page_name, api_name=api_name, headers=headers, data=json.dumps(data))
        return res.json()['data']['nid']

    @log_decorator
    def long_gpx(self):
        # 返回nid
        api_name = 'save_gpx'
        headers = self.headers
        headers['Content-Type'] = 'application/xml'
        gpx_file_path = '../test_data/350km.gpx'

        with open(gpx_file_path, 'rb') as f:
            data = f.read()

        res = self.post_request(page_name=self.page_name, api_name=api_name, headers=headers, data=data)
        return res.json()['error']


if __name__ == '__main__':
    x = RouteLibrary()
    x.long_gpx()
