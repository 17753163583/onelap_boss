import json
import os
from common.get_path import project_path
from loguru import logger

data_key_json_file_name = project_path() + '/POM/boss/test_data/publish_data.json'


def check_publish_json_exist():
    if os.path.exists(data_key_json_file_name):
        logger.info("惩罚信息json文件已存在，无需创建")
    else:
        json_data_dict = {
            'is_forbid_speak': [],
            'is_forbid_speak_list': [],
            'is_forbid_login': [],
            'is_forbid_login_list': []
        }
        with open(data_key_json_file_name, 'w', encoding='utf-8') as f:
            json.dump(json_data_dict, f)
            logger.info("惩罚信息json文件创建成功")


def get_publish_data_key_list(publish):
    with open(data_key_json_file_name, 'r', encoding='utf-8') as file_read:
        json_data_dict = json.load(file_read)
        publish_data_key_list = json_data_dict[publish + '_list']
        return publish_data_key_list


def append_data_key_to_json(publish, key_dict):
    check_publish_json_exist()
    new_data_key = str(key_dict['data_key'])
    with open(data_key_json_file_name, 'r', encoding='utf-8') as file_read:
        json_data_dict = json.load(file_read)
        publish_dict = json_data_dict[publish]
        publish_data_key_list = json_data_dict[publish + '_list']

    with open(data_key_json_file_name, 'w', encoding='utf-8') as file_write:
        publish_dict.append(key_dict)
        logger.info("惩罚信息已在文件中创建")
        publish_data_key_list.append(new_data_key)
        logger.info("惩罚信息的data-key已添加进列表")

        json.dump(json_data_dict, file_write)


def remove_data_key_to_json(publish, data_key):
    tar_data_key = str(data_key)
    with open(data_key_json_file_name, 'r', encoding='utf-8') as file_read:
        json_data_dict = json.load(file_read)
        publish_dict = json_data_dict[publish]
        publish_data_key_list = json_data_dict[publish + '_list']

    with open(data_key_json_file_name, 'w', encoding='utf-8') as file_write:
        list_index = publish_data_key_list.index(tar_data_key)
        # 按索引删除，后续元素索引前移
        publish_dict.pop(list_index)
        # 按值删除
        publish_data_key_list.remove(tar_data_key)

        json.dump(json_data_dict, file_write)
        logger.info("惩罚信息删除成功")


if __name__ == '__main__':
    check_publish_json_exist()
    dict_1 = {
        "data_key": 123,
        "start_time": 1,
        "end_time": 1
    }
    dict_2 = {
        "data_key": 123,
        "start_time": 1,
        "end_time": 5
    }
    append_data_key_to_json('is_forbid_speak', dict_1)
    append_data_key_to_json('is_forbid_speak', dict_2)
    remove_data_key_to_json('is_forbid_speak', 123)
