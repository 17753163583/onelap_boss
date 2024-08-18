from appium import webdriver
from appium.options.android import UiAutomator2Options
from loguru import logger


def connect_device_first():
    capabilities = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "platformVersion": "12",
        "deviceName": "127.0.0.1:16384",
        "appPackage": "com.onelap.bls.dear",
        "appActivity": "com.onelap.bls.dear.activity.riding_splash.SplashActivity",
        # 设置为False，对app重置全部数据（调试登录可用）
        "noReset": False
    }

    # 创建driver对象
    appium_server_url = 'http://127.0.0.1:4723'
    driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
    logger.info("连接设备成功")
    return driver


def connect_phone_first():
    capabilities = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "platformVersion": "14",
        "deviceName": "f93e6749",
        "appPackage": "com.onelap.bls.dear",
        "appActivity": "com.onelap.bls.dear.activity.riding_splash.SplashActivity",
        # 300s无动作后，退出session
        'newCommandTimeout': "300",
        # 设置为False，对app重置全部数据（调试登录可用）
        "noReset": False
    }

    # 创建driver对象
    appium_server_url = 'http://127.0.0.1:4723'
    driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
    logger.info("连接设备成功")
    return driver


def connect_device_later():
    capabilities = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "platformVersion": "12",
        "deviceName": "127.0.0.1:16384",
        # 300s无动作后，退出session
        'newCommandTimeout': "300",
        # 设置为False，对app重置全部数据（调试登录可用）
        "noReset": True
    }

    # 创建driver对象
    appium_server_url = 'http://127.0.0.1:4723'
    driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
    logger.info("连接设备成功")
    return driver


if __name__ == '__main__':
    connect_device_later()
