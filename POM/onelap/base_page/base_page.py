from common.get_yaml import GetYamlData
from common.find_ele import find_ele
from loguru import logger
from common.connect_device import connect_device_later, connect_device_first

class OnelapBasePage(GetYamlData):
    def __init__(self):
        self.test_onelap_account_dict = GetYamlData().get_login_accounts()['onelap_account']
        self.driver_first = connect_device_first()

    @staticmethod
    def element_locator(driver, page_name, module_name, element_name):
        locator_message = GetYamlData().get_onelap_element_data(page_name)[module_name][element_name]

        find_type = locator_message['type']
        find_key = locator_message['key']
        element_locator = find_ele(driver, find_type, find_key)
        if element_locator:
            logger.info(f'{page_name}_{element_name}定位成功')
            return element_locator

    @staticmethod
    def element_locator_sendkeys(driver, page_name, module_name, element_name, input_data=None):
        locator_message = GetYamlData().get_onelap_element_data(page_name)[module_name][element_name]

        find_type = locator_message['type']
        find_key = locator_message['key']
        element_locator = find_ele(driver, find_type, find_key)
        if element_locator:
            logger.info(f'{page_name}_{element_name}定位成功')
        else:
            logger.error(f'{page_name}_{element_name}定位失败')
            return

        element_locator_sendkeys = element_locator.send_keys(input_data)
        logger.info(f'{page_name}_{element_name}输入数据：{input_data}成功')
        return element_locator_sendkeys
