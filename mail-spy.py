import sys
import socket
import dns.resolver
from lib import logger
from lib import paypal
from lib import facebook
from lib import instagram
from pydnsbl import DNSBLChecker
from model.MXRecord import MXRecord

masked_contact_info = {
    'emails': [],
    'phone': []
}

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
    if len(facebook_emails) > 0:
        logger.print_warning("Found facebook account for " + email_address)
        for email in facebook_emails:
            if '**' in email:
                masked_contact_info['emails'].append(email)

    # Check instagram
    instaTest = instagram.doesInstagramAccountExist(email_address)
    if instaTest:
        logger.print_warning("Instagram account found")
    

    # Check PayPal
    payPalCheck = paypal.doesPPAccountExist(email_address)
    if len(payPalCheck) is not 0:
        logger.print_warning("PayPal account found, pulling masked phone number from account")
        logger.print_warning("Found masked number " + payPalCheck[0] + " from PayPal")
        masked_contact_info['phone'].append(payPalCheck[0])