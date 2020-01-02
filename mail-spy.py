import sys
import socket
import dns.resolver
from lib import logger
from pydnsbl import DNSBLChecker
from model.MXRecord import MXRecord

if __name__ == '__main__':
    email_address = sys.argv[1]
    email_domain = email_address.split('@')[1]
    logger.print_status("Pulling info on address " + email_address)

    # Grab MX records and get IP for each server
    mx_records = []
    logger.print_status("Pulling MX records from DNS")
    for address in dns.resolver.query(email_domain, 'MX'):
        raw_addr = address.to_text()
        clean_addr = raw_addr[:-1].split(" ")[1]
        ip_addr = socket.gethostbyname(clean_addr)
        mx_records.append(MXRecord(clean_addr, ip_addr))

    # Blacklist check
    blacklistChecker = DNSBLChecker()
    for record in mx_records:
        blacklist_check = blacklistChecker.check_ip(record.ip)
        if blacklist_check.blacklisted:
            logger.print_warning(record.url + " is blacklisted!")


# from selenium import webdriver 
# from selenium.webdriver.support.ui import Select
# from urllib.parse import urlparse, parse_qs

# def facebookRegistationRequest(email):
#     driver = webdriver.Chrome() 
#     driver.get('https://www.facebook.com/')

#     firstName = driver.find_element_by_name('firstname')
#     firstName.send_keys("John")

#     lastName = driver.find_element_by_name('lastname')
#     lastName.send_keys("Doel")

#     emailField = driver.find_element_by_name('reg_email__')
#     emailField.send_keys(email)

#     passwordField = driver.find_element_by_name('reg_passwd__')
#     passwordField.send_keys('testThisIsMyLockdown135')

#     monthSelect = Select(driver.find_element_by_id('month'))
#     monthSelect.select_by_visible_text('Jul')

#     daySelect = Select(driver.find_element_by_id('day'))
#     daySelect.select_by_visible_text('12')

#     yearSelect = Select(driver.find_element_by_id('year'))
#     yearSelect.select_by_visible_text('1982')

#     genderOption = driver.find_elements_by_name('sex')
#     genderOption[1].click()

#     emailConfirm = driver.find_element_by_name('reg_email_confirmation__')
#     emailConfirm.send_keys(email)

#     submitBtn = driver.find_element_by_name('websubmit')
#     submitBtn.click()

#     time.sleep(10)

#     print(driver.current_url)

#     if 'facebook.com/confirmemail.php' in  driver.current_url:
#         print("This email does NOT have a facebook account")
#         return False
#     elif 'facebook.com/recover/initiate/' in driver.current_url:
#         print("Found facebook account for email address with initiate recovery")
#         #print(driver.current_url)

#         parsed_url = urlparse(driver.current_url)
#         test = parse_qs(parsed_url.query)

#         print(test)

#         #time.sleep(10)
#         return True
#     elif 'facebook.com/recover/code' in driver.current_url:
#         print("Found facebook account for email address")
#         #print(driver.current_url)

#         parsed_url = urlparse(driver.current_url)
#         test = parse_qs(parsed_url.query)

#         emailsFound = []
#         for key, value in test.items():
#             if 'em' in key:
#                 emailsFound.append(value[0])
#         print(emailsFound)
#         return emailsFound
#     else:
#         print("Unknown facebook acount status, check method is still working")
#         return False
