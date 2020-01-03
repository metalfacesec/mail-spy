import time
from .logger import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from urllib.parse import urlparse, parse_qs

def doesTwitterAccountExist(email):
    # TODO: Add firefox support
    driver = webdriver.Chrome() 
    driver.get('https://twitter.com/account/begin_password_reset')

    emailBox = driver.find_element_by_name('account_identifier')
    emailBox.send_keys(email)

    buttons = driver.find_elements_by_class_name('EdgeButton')[0].click()

    time.sleep(4)

    strongElements = driver.find_elements_by_xpath("//strong")
    maskedInfo = []
    for elem in strongElements:
        if '**' in elem.text:
            maskedInfo.append(elem.text)

        if len(elem.text) is 2 and elem.text.isnumeric():
            maskedInfo.append("***-***-**" + elem.text)
    return maskedInfo