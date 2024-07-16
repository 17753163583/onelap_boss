from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium import webdriver
from common.get_yaml import GetYamlData
from common.find_ele import find_ele
from loguru import logger


class OnelapBasePage(GetYamlData):
    def __init__(self):
        self.onelap_element = GetYamlData.get_onelap_element_data()
        self.onelap_api = GetYamlData.get_onelap_api_param_data()
        self.test_onelap_account_dict = GetYamlData().get_login_accounts()['onelap_account']

    @staticmethod
    def connect_device_first():
        capabilities = {
            "platformName": "Android",
            "automationName": "UiAutomator2",
            "platformVersion": "12",
            "deviceName": "127.0.0.1:16384",
            "appPackage": "com.onelap.bls.dear",
            "appActivity": "com.onelap.bls.dear.activity.riding_splash.SplashActivity",
            # 设置为False，对app重置全部数据（调试登录可用）
            "noReset": "false"
        }

        dic = {
            "platformName": "Android",
            "platformVersion": "8.1.0",
            "deviceName": "127.0.0.1:16384",
            "appPackage": "com.android.settings",
            "appActivity": ".Settings",
            "resetKeyboard": True,
            "noReset": True
        }

        # 创建driver对象
        appium_server_url = 'http://127.0.0.1:4723'
        driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(dic))
        logger.info("连接设备成功")
        return driver

    @staticmethod
    def connect_device_later():
        capabilities = {
            "platformName": "Android",
            "appium:options": {
                "automationName": "UiAutomator2",
                "platformVersion": "12",
                "deviceName": "127.0.0.1:16384",
                # 设置为False，对app重置全部数据（调试登录可用）
                "noReset": True
            }
        }

        # 创建driver对象
        appium_server_url = 'http://127.0.0.1:4723'
        driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
        logger.info("连接设备成功")
        return driver

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


if __name__ == '__main__':
    OnelapBasePage().connect_device_first()
