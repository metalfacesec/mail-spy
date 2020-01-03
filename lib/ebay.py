import time
from .logger import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from urllib.parse import urlparse, parse_qs

def doesEbayAccountExist(email):
    # TODO: Add firefox support
    driver = webdriver.Firefox()
    driver.get('https://ebay.com')
    time.sleep(1)
    driver.get('https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&ru=https%3A%2F%2Fwww.ebay.com%2F')

    time.sleep(30)

    textCode = driver.find_element_by_id('otpanch').click()

    time.sleep(30)

    emailBox = driver.find_element_by_id('userid_otp').send_keys(email)
    submitBtn = driver.find_element_by_id('otp-btn').click()
    
    time.sleep(1)

    
    usersFound = driver.find_element_by_id("OTP_STATUS_1")
    if '-xxx-' in usersFound.text:
        return [usersFound.text.split(" is ")[1][:-1]]
    return []