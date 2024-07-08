import json

import requests

from common.get_yaml import GetYamlData
from common.get_token import GetToken
from common.handle_md5 import md5_encrypt
from loguru import logger

comment_api_data = GetYamlData().get_onelap_api_param_data()['send_comment']


def send_comment(account, password):
    try:
        url = comment_api_data['url']
        comment_api_data['headers']['Authorization'] = GetToken().onelap_login(account, password)['data']['token']
        headers = comment_api_data['headers']
        body = json.dumps(comment_api_data['data'])

        response = requests.post(url=url, headers=headers, data=body)
        if response.json()['code'] == 440:
            logger.error("账号被禁言, 无法评论")
            return response.json()
        else:
            return response.json()
    except KeyError as error:
        logger.error(f"账号状态异常，无法评论,错误信息:{error}")


if __name__ == '__main__':
    res = send_comment('13001723386', md5_encrypt('zhang107.'))
    print(res)
