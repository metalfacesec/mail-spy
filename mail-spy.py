import sys
import socket
import dns.resolver
from lib import logger
from lib import facebook
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

    # Check for facebook account
    facebook_emails = facebook.doesFacebookAccountExist(email_address)