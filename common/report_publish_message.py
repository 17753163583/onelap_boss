import json
import os

from logger import logger
import numpy as np

data_key_json_file_name = '../POM/boss/test_data/publish_data.json'


def check_publish_json_exist():
    if os.path.exists(data_key_json_file_name):
        logger.info("惩罚信息json文件已存在，无需创建")
    else:
        json_data_dict = {
            'is_forbid_speak': [],
            'forbid_speak_key_list': [],
            'is_forbid_login': [],
            'forbid_login_key_list': []
        }
        with open(data_key_json_file_name, 'w', encoding='utf-8') as f:
            json.dump(json_data_dict, f)
            logger.info("惩罚信息json文件创建成功")


def append_data_key_to_json(publish, key_dict):
    with open(data_key_json_file_name, 'r+', encoding='utf-8') as f:
        json_data_dict = json.load(f)
        publish_value = json_data_dict[publish]

        array_publish = np.array(publish_value)
        # 查找重复字典的index
        dub_index = np.where(array_publish == key_dict)[0].tolist()
        print(dub_index)

        if len(dub_index) == 0:
            publish_value.append(key_dict)
            json.dump(json_data_dict, f)
            logger.info("惩罚信息已在文件中创建")
        else:
            publish_value[dub_index][0]['end_time'] = key_dict['end_time']
            logger.info("惩罚信息已更新")


def remove_data_key_to_json(publish, data_key_value):
    with open(data_key_json_file_name, 'r+', encoding='utf-8') as f:
        json_data_dict = json.load(f)
        publish_value_dict_list = json_data_dict[publish]
        for publish_dict in publish_value_dict_list:
            if publish_dict['data_key'] == data_key_value:
                publish_value_dict_list.remove(publish_dict)

                json.dump(json_data_dict, f)
                logger.info("惩罚信息已在文件中删除")


if __name__ == '__main__':
    check_publish_json_exist()
    dict_1 = {
        "data_key": 123,
        "start_time": 1,
        "end_time": 2
    }
    append_data_key_to_json('is_forbid_speak', dict_1)
    append_data_key_to_json('is_forbid_speak', dict_1)
    # remove_data_key_to_json('is_forbid_speak', '1')
