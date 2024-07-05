from pathlib import Path
from loguru import logger
import os
import json


class CheckExist:
    def __init__(self):
        self.data_key_json_file_name = '../POM/boss/test_data/publish_data.json'
        self.log_dir = Path(__file__).resolve().parent.parent.joinpath("Logs")

    def check_logs(self):
        # 日志目录的创建
        if os.path.exists(self.log_dir):
            logger.info("Logs目录已存在，无需创建")
        else:
            try:
                self.log_dir.mkdir(parents=True)
            except PermissionError:
                logger.error("没有权限创建日志目录")
            except Exception as e:
                logger.error(f"创建日志目录时发生错误: {e}")

    def check_publish_message(self):
        if os.path.exists(self.data_key_json_file_name):
            logger.info("惩罚信息json文件已存在，无需创建")
        else:
            json_data_dict = {'is_forbid_speak': [], 'is_forbid_login': []}
            with open(self.data_key_json_file_name, 'w', encoding='utf-8') as f:
                json.dump(json_data_dict, f)
                logger.info("惩罚信息json文件创建成功")


if __name__ == '__main__':
    a = CheckExist()
    a.check_publish_message()
    a.check_logs()
