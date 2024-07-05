import json

from common.get_path import project_path


def get_login_cookies():
    with open(project_path() + "/test_data/boss_login_cookies.json", 'r') as file:
        dict_cookies = json.load(file)
    return dict_cookies
