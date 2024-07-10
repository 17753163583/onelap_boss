from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def find_ele(driver, find_type, find_key):
    try:
        # 显示等待
        # 元素是否存在，不一定可见（toast）
        ele = WebDriverWait(driver, 3, 0.25).until(ec.presence_of_element_located((find_type, find_key)))
        return ele
    except Exception as e:
        raise e
