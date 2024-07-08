from loguru import logger
from common.find_ele import find_ele
from selenium import webdriver
from common.get_yaml import GetYamlData


class OnelapBasePage(GetYamlData):
    def __init__(self):
        self.onelap_element = GetYamlData.get_onelap_element_data()
