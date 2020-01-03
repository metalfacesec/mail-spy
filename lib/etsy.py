import time
from .logger import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from urllib.parse import urlparse, parse_qs

def doesEtsyAccountExist(email):
    # TODO: Add firefox support
    driver = webdriver.Chrome() 
    driver.get('https://www.etsy.com/forgot_password?email=')

    emailOrPhone = driver.find_elements_by_name('email')
    for emailBtn in emailOrPhone:
        try:
            emailBtn.send_keys(email)
        except:
            pass

    buttons = driver.find_element_by_name("submit").click()

    time.sleep(1)

    usersFound = driver.find_elements_by_xpath("//*[contains(text(), 'no account associated with that email address')]")
    if len(usersFound) is 0:
        return True
    return False