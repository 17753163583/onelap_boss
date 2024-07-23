# 导入selenium模块
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By


# 函数名格式test_**()
def test_chrome():
    # 启动浏览器驱动
    session

    driver = webdriver.Chrome(service=Service(project_path() + "/conf/chromedriver_126.0.6478.126.exe"))
    cooikie_dict = driver.get_cookies()


    for cookie in cooikie_dict:
        driver.add_cookie(cookie)


    # 最大化窗口
    driver.maximize_window()
    # 访问url
    driver.get('https://www.baidu.com')
    # 定位元素
    el = driver.find_element(By.ID, 'kw')
    # 执行自动化操作
    el.send_keys('NBA头条')
    driver.find_element(By.ID, 'su').click()
    # 休眠1秒
    sleep(1)
    # 关闭浏览器并释放进程资源
    driver.quit()


if __name__ == '__main__':
    test_chrome()
