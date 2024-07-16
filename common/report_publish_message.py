import json

from loguru import logger

from common.get_path import publish_json_path

json_path = publish_json_path()


def get_publish_data_key_list(publish):
    with open(json_path, 'r', encoding='utf-8') as file_read:
        json_data_dict = json.load(file_read)
        publish_data_key_list = json_data_dict[publish + '_list']
        logger.info("读取文件中的data-key列表")
        return publish_data_key_list


def append_data_key_to_json(publish, key_dict):
    new_data_key = str(key_dict['data_key'])
    with open(json_path, 'r', encoding='utf-8') as file_read:
        json_data_dict = json.load(file_read)
        publish_dict = json_data_dict[publish]
        publish_data_key_list = json_data_dict[publish + '_list']

    with open(json_path, 'w', encoding='utf-8') as file_write:
        if publish_dict.append(key_dict):
            logger.info("惩罚信息已在文件中创建")

        if publish_data_key_list.append(new_data_key):
            logger.info("惩罚信息的data-key已添加进列表")

        json.dump(json_data_dict, file_write)


def remove_data_key_to_json(publish, data_key):
    tar_data = str(data_key)
    with open(json_path, 'r', encoding='utf-8') as file_read:
        json_data_dict = json.load(file_read)
        publish_data_key_list = json_data_dict[publish + '_list']
        publish_index = publish_data_key_list.index(tar_data)

    with open(json_path, 'w', encoding='utf-8') as file_write:
        # 删除字典中对应的
        json_data_dict[publish].pop(publish_index)
        # 删除列表中对于的
        publish_data_key_list.remove(tar_data)

        if json.dump(json_data_dict, file_write):
            logger.info("惩罚信息删除成功")


if __name__ == '__main__':
    remove_data_key_to_json('is_forbid_login', '6695d9cb3dc8d43dab3372e6')
