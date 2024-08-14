import requests
from loguru import logger

from POM.api.base_page.base_page import BasePage
from common.logger import log_decorator


class PersonalHomePage(BasePage):
    def __init__(self):
        super().__init__()
        self.page_name = "personal_homepage"
        self.token = self.onelap_login_res['data']['token']
        self.user_id = self.onelap_login_res['data']['uid']

    @log_decorator
    def user_info(self):
        url = f'http://rfs-fitness-informal.rfsvr.net/indoor/v1/app/social/homePage/{self.user_id}?is_refresh=0&from=self'
        headers = {'Authorization': self.token}

        res = requests.get(url=url, headers=headers)
        if res.json()['code'] == 200:
            logger.info("获取用户信息成功")

        return res.json()

    @log_decorator
    def follow_others(self):
        api_name = "follow_others"
        url = self.api_params[self.page_name][api_name]['url']
        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.token
        data = self.api_params[self.page_name][api_name]['data']
        data['type'] = 1

        res_1 = requests.put(url=url, headers=headers, data=data)

        if res_1.json()['code'] == '411':
            logger.error("已经关注/已经取消")
            data['type'] = 2
            requests.put(url=url, headers=headers, data=data)
            logger.info("提交取消关注请求")
            data['type'] = 1
            res_2 = requests.put(url=url, headers=headers, data=data)
            if res_2:
                logger.info("重新提交关注请求")

            return res_2.json()
        else:
            return res_1.json()

    @log_decorator
    def like_others(self):
        api_name = "like_others"
        url = self.api_params[self.page_name][api_name]['url']
        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.token

        res = requests.put(url=url, headers=headers)
        if res.json()['code'] == 403 and res.json()['error'] == "Forbidden":
            logger.error("已经为uid:238493点过赞了")

        return res.json()

    @log_decorator
    def change_area_and_ftp(self):
        api_name = 'change_person_home_info'
        headers = self.api_params[self.page_name][api_name]['headers']
        headers['Authorization'] = self.token

        data_area = {"province": "山东省", "city": "青岛市"}
        data_ftp = {"FTP": 120, "ftp_type": 2}
        res_area = self.post_request(page_name=self.page_name, api_name=api_name, headers=headers, data=data_area)
        if res_area.json()['code'] == 403:
            logger.error("每个自然月只能修改一次地区")

        res_ftp = self.post_request(page_name=self.page_name, api_name=api_name, headers=headers, data=data_ftp)
        return res_area.json(), res_ftp.json()

    @log_decorator
    def check_ride_data(self):
        u = f'http://rfs-fitness-informal.rfsvr.net/indoor/v1/app/social/homePage/{self.user_id}?is_refresh=0&from=self'
        headers = {'Authorization': self.token}

        res = requests.get(url=u, headers=headers)
        if res.json()['code'] == 200:
            logger.info("读取骑行数据")
        else:
            logger.error("读取失败")

        return res.json()['data']['dataRelated'], res.json()['data']['dataAnalysis']


if __name__ == '__main__':
    x = PersonalHomePage()
    x.user_info()
    x.follow_others()
    x.like_others()
    x.change_area_and_ftp()
    x.check_ride_data()
