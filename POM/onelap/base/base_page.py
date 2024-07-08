from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium import webdriver
from common.get_yaml import GetYamlData


class OnelapBasePage(GetYamlData):
    def __init__(self):
        self.onelap_element = GetYamlData.get_onelap_element_data()
        self.onelap_api = GetYamlData.get_onelap_api_param_data()

    @staticmethod
    def connect_device_first():
        capabilities = dict(
            platformName='Android',
            platformVersion='12',
            automationName='uiautomator2',
            deviceName='127.0.0.1:16384',
            appPackage='com.onelap.bls.dear',
            appActivity='com.onelap.bls.dear.activity.riding_splash.SplashActivity',

            # 设置为False，对app重置全部数据（调试登录可用）
            noReset=False
        )

        # 创建driver对象
        appium_server_url = 'http://127.0.0.1:4723'
        driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
        return driver

    @staticmethod
    def connect_device_later():
        capabilities = dict(
            platformName='Android',
            platformVersion='12',
            automationName='uiautomator2',
            deviceName='127.0.0.1:16384',

            # 设置为False，对app重置全部数据（调试登录可用）
            noReset=True
        )

        # 创建driver对象
        appium_server_url = 'http://127.0.0.1:4723'
        driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
        return driver
