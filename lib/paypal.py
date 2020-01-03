import time
from .logger import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from urllib.parse import urlparse, parse_qs

def doesPPAccountExist(email):
    # TODO: Add firefox support
    driver = webdriver.Chrome() 
    driver.get('https://www.paypal.com/authflow/password-recovery/?country.x=US&locale.x=en_US&redirectUri=%252Fsignin%252F')

    emailBox = driver.find_element_by_name('email')
    emailBox.send_keys(email)

    driver.find_element_by_name('submitForgotPasswordForm').click()

    time.sleep(4)

    if 'https://www.paypal.com/authflow/password-recovery' in driver.current_url:
        return []
    
    phoneNumbers = driver.find_elements_by_class_name('forceLtr')
    for div in phoneNumbers:
        if '••' in div.text:
            return [ div.text ]