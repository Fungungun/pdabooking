from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import random
import time
import logging
import requests


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_log_via_mail():
    msg = MIMEMultipart()
    msg["From"] = "mysendnotif2012@gmail.com"
    msg["To"] = "21558188@student.uwa.edu.au"
    msg["Subject"] = "Mail from python"
    part = MIMEText(open("run.log", 'r').read())
    part.add_header('Content-Disposition', "attachment; filename= run.log")
    msg.attach(part)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("mysendnotif2012@gmail.com", "Z5tl&IeY4q7x")
    server.sendmail(
    "Notification from Python", 
    "21558188@student.uwa.edu.au", 
    msg.as_string())
    server.quit()
def send_msg_via_mail(msg):
    msg = 'Subject: {}\n\n{}'.format(msg, ' ')
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("mysendnotif2012@gmail.com", "Z5tl&IeY4q7x")
    server.sendmail(
    "Notification from Python", 
    "21558188@student.uwa.edu.au", 
    msg)
    server.quit()


logging.basicConfig(
    handlers=[logging.FileHandler("run.log", mode='a'),
                logging.StreamHandler()
    ],
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%d/%m/%y %H:%M:%S')

def random_wait(a=1, b=2):
    t = 1000
    time.sleep(random.randint(a*t,b*t) / 1.0 / t)

def wait(n):
    time.sleep(n)


options = webdriver.ChromeOptions()
# options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
# driver = webdriver.PhantomJS()
driver.get(('https://online.transport.wa.gov.au/pdabooking/manage/?0'))

logging.info('Filling form')
driver.find_element_by_name("clientDetailsPanel:overseasClientType").click()
wait(2)

elem = driver.find_element_by_name("clientDetailsPanel:licenceNumber")
elem.send_keys("7983449")

elem = driver.find_element_by_name("clientDetailsPanel:applicationNumber")
elem.send_keys("510166")

elem = driver.find_element_by_name("clientDetailsPanel:receiptNumber")
elem.send_keys("104217960")

elem = driver.find_element_by_name("clientDetailsPanel:firstName")
elem.send_keys("Hui")

elem = driver.find_element_by_name("clientDetailsPanel:lastName")
elem.send_keys("Cao")

elem = driver.find_element_by_name("clientDetailsPanel:dateOfBirth")
elem.send_keys("04/12/1985")

logging.info('Continue')
# Continue
driver.find_element_by_id("id5").click()
wait(2)

logging.info('Search Availability')
# Search Availability
driver.find_element_by_id("id12").click()
wait(2)

logging.info('Get Sites')
# Select site
elem = Select(driver.find_element_by_id("id1c"))
avail_booking = {elem.options[i].text:[] for i in range(1, 10)}

logging.info('Start Scanning')
while True:
    for i in range(1, 10):
        site = elem.options[i].text
        elem.select_by_index(i)

        # Search
        driver.find_element_by_name("searchBookingContainer:search").click()
        random_wait(1, 5)

        # Check results
        elem_res = None
        try:
            elem_res = driver.find_element_by_name("searchBookingContainer:searchResults:searchResultGroup")
        except:
            pass

        if elem_res is not None:
            elem_booking = driver.find_elements_by_id("searchResultRadioLabel")
            avail_booking[site] = [x.text for x in elem_booking]

        random_wait(1, 5)
    logging.info(avail_booking)
    
    if len(avail_booking['West Perth']) > 0:
        msg = ', '.join(avail_booking['West Perth'])
        send_msg_via_mail(msg)
        # exit()
    
    random_wait(1500, 1600)


