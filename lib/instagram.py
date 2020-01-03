import time
from .logger import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from urllib.parse import urlparse, parse_qs

def doesInstagramAccountExist(email):
    # TODO: Add firefox support
    driver = webdriver.Chrome() 
    driver.get('https://www.instagram.com/accounts/password/reset/')

    emailOrPhone = driver.find_element_by_name('cppEmailOrUsername')
    emailOrPhone.send_keys(email)

    buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Send Login Link')]")
    for button in buttons:
        button.click()

    time.sleep(1)

    usersFound = driver.find_elements_by_xpath("//*[contains(text(), 'No users found')]")
    if len(usersFound) is 0:
        return True
    return False