import json

import requests

from common.get_yaml import GetYamlData
from common.get_token import GetToken

from loguru import logger

comment_api_data = GetYamlData().get_onelap_api_param_data()['send_comment']


def send_comment(username, password):
    try:
        url = comment_api_data['url']
        headers = comment_api_data['headers']
        login_res = GetToken().onelap_login(username, password)
        print(login_res)
        print(type(login_res))
        headers['Authorization'] = login_res['data']['token']

        body = json.dumps(comment_api_data['data'])

        response = requests.post(url=url, headers=headers, data=body)
        if response.json()['code'] == 440:
            logger.error("账号被禁言, 无法评论")
            return response.json()
        else:
            return response.json()
    except KeyError:
        logger.error(f"账号状态异常，无法评论")


if __name__ == '__main__':
    res = send_comment('13001723386', 'zhang107.')
    print(res)
