import json

from Common.get_path import project_path


def get_login_cookies():
    with open(project_path() + "/Test_Data/boss_login_cookies.json", 'r') as file:
        dict_cookies = json.load(file)
    return dict_cookies
