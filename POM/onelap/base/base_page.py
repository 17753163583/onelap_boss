from common.get_yaml import GetYamlData
from common.find_ele import find_ele
from loguru import logger


class OnelapBasePage(GetYamlData):
    def __init__(self):

        self.onelap_element = GetYamlData.get_onelap_element_data()
        self.onelap_api = GetYamlData.get_onelap_api_param_data()
        self.test_onelap_account_dict = GetYamlData().get_login_accounts()['onelap_account']

    def element_locator(self, driver, page_name, element_name):
        locator_message = self.onelap_element[page_name][element_name]

        find_type = locator_message['type']
        find_key = locator_message['key']
        element_locator = find_ele(driver, find_type, find_key)
        if element_locator:
            logger.info(f'{page_name}_{element_name}定位成功')
            return element_locator

    def element_locator_sendkeys(self, driver, page_name, element_name, input_data=None):
        locator_message = self.onelap_element[page_name][element_name]

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
