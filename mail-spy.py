import sys
import time
import socket
from selenium import webdriver 
from selenium.webdriver.support.ui import Select
import dns.resolver
from urllib.parse import urlparse, parse_qs
from pydnsbl import DNSBLChecker

def facebookRegistationRequest(email):
    driver = webdriver.Chrome() 
    driver.get('https://www.facebook.com/')

    firstName = driver.find_element_by_name('firstname')
    firstName.send_keys("John")

    lastName = driver.find_element_by_name('lastname')
    lastName.send_keys("Doel")

    emailField = driver.find_element_by_name('reg_email__')
    emailField.send_keys(email)

    passwordField = driver.find_element_by_name('reg_passwd__')
    passwordField.send_keys('testThisIsMyLockdown135')

    monthSelect = Select(driver.find_element_by_id('month'))
    monthSelect.select_by_visible_text('Jul')

    daySelect = Select(driver.find_element_by_id('day'))
    daySelect.select_by_visible_text('12')

    yearSelect = Select(driver.find_element_by_id('year'))
    yearSelect.select_by_visible_text('1982')

    genderOption = driver.find_elements_by_name('sex')
    genderOption[1].click()

    emailConfirm = driver.find_element_by_name('reg_email_confirmation__')
    emailConfirm.send_keys(email)

    submitBtn = driver.find_element_by_name('websubmit')
    submitBtn.click()

    time.sleep(60)

    print(driver.current_url)

    if 'facebook.com/confirmemail.php' in  driver.current_url:
        print("This email does NOT have a facebook account")
        return False
    elif 'facebook.com/recover/initiate/' in driver.current_url:
        print("Found facebook account for email address with initiate recovery")
        #print(driver.current_url)

        parsed_url = urlparse(driver.current_url)
        test = parse_qs(parsed_url.query)

        print(test)

        #time.sleep(10)
        return True
    elif 'facebook.com/recover/code' in driver.current_url:
        print("Found facebook account for email address")
        #print(driver.current_url)

        parsed_url = urlparse(driver.current_url)
        test = parse_qs(parsed_url.query)

        print(test)

        #time.sleep(10)
        return True
    else:
        print("Unknown facebook acount status, check method is still working")
        return False

class bcolors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERL = '\033[4m'
    ENDC = '\033[0m'
    backBlack = '\033[40m'
    backRed = '\033[41m'
    backGreen = '\033[42m'
    backYellow = '\033[43m'
    backBlue = '\033[44m'
    backMagenta = '\033[45m'
    backCyan = '\033[46m'
    backWhite = '\033[47m'

def print_status(message):
    print((bcolors.GREEN) + (bcolors.BOLD) + \
        ("[*] ") + (bcolors.ENDC) + (str(message)))


def print_info(message):
    print((bcolors.BLUE) + (bcolors.BOLD) + \
        ("[-] ") + (bcolors.ENDC) + (str(message)))

def print_warning(message):
    print((bcolors.YELLOW) + (bcolors.BOLD) + \
        ("[!] ") + (bcolors.ENDC) + (str(message)))


def print_error(message):
    print((bcolors.RED) + (bcolors.BOLD) + \
        ("[!] ") + (bcolors.ENDC) + (bcolors.RED) + \
        (str(message)) + (bcolors.ENDC))



# checker = DNSBLChecker()

email_address = sys.argv[1]
email_domain = email_address.split('@')[1]

facebookRegistationRequest(email_address)

# print_status("Pulling MX records from DNS")
# for address in dns.resolver.query(email_domain, 'MX'):
#     raw_addr = address.to_text()
#     clean_addr = raw_addr[:-1].split(" ")[1]
#     ip_addr = socket.gethostbyname(clean_addr)

#     print_info(ip_addr + " " + raw_addr)

#     blacklist_check = checker.check_ip(socket.gethostbyname(clean_addr))

#     if blacklist_check.blacklisted:
#         print_warning(clean_addr + " is blacklisted!")
#     else:
#         print_info(clean_addr + " not found on blacklist")