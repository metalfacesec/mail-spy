import socket
import dns.resolver
from pydnsbl import DNSBLChecker

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

checker = DNSBLChecker()

print_status("Pulling MX records from DNS")
for address in dns.resolver.query('gmail.com', 'MX'):
    raw_addr = address.to_text()
    clean_addr = raw_addr[:-1].split(" ")[1]
    ip_addr = socket.gethostbyname(clean_addr)

    print_info(ip_addr + " " + raw_addr)

    blacklist_check = checker.check_ip(socket.gethostbyname(clean_addr))

    if blacklist_check.blacklisted:
        print_warning(clean_addr + " is blacklisted!")
    else:
        print_info(clean_addr + " not found on blacklist")

