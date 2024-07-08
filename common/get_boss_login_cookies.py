import json

from common.get_path import project_path


def get_login_cookies():
    with open(project_path() + "/POM/boss/test_data/boss_login_cookies.json", 'r') as file:
        dict_cookies = json.load(file)
    return dict_cookies


if __name__ == '__main__':
    print(get_login_cookies())
