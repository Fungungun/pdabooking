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


logging.basicConfig(
    handlers=[logging.FileHandler("run.log", mode='a'),
                logging.StreamHandler()
    ],
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%d/%m/%y %H:%M:%S')


def send_log_via_mail():
    msg = MIMEMultipart()
    msg["From"] = "mysendnotif2012@gmail.com"
    msg["To"] = "cliu4677@gmail.com"
    msg["Subject"] = "Mail from python"
    part = MIMEText(open("run.log", 'r').read())
    part.add_header('Content-Disposition', "attachment; filename= run.log")
    msg.attach(part)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("mysendnotif2012@gmail.com", "Z5tl&IeY4q7x")
    server.sendmail(
    "Notification from Python", 
    "cliu4677@gmail.com", 
    msg.as_string())
    server.quit()
def send_msg_via_mail(msg):
    msg = 'Subject: {}\n\n{}'.format(msg, ' ')
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("mysendnotif2012@gmail.com", "Z5tl&IeY4q7x")
    server.sendmail(
    "Notification from Python", 
    "cliu4677@gmail.com", 
    msg)
    server.quit()



def random_wait(a=1, b=2):
    t = 1000
    time.sleep(random.randint(a*t,b*t) / 1.0 / t)

def wait(n):
    time.sleep(n)


options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
# driver = webdriver.PhantomJS()
driver.get(('https://online.transport.wa.gov.au/tso/selfservice/public/login.jsf'))

elem = driver.find_element_by_name("loginForm:userId")
elem.send_keys("caohui2")

elem = driver.find_element_by_name("loginForm:password")
elem.send_keys("vrGR479wFokc")

driver.find_element_by_name("loginForm:loginButton").click()
wait(10)
driver.find_element_by_id("menuForm:menubar_licence").click()
wait(10)
driver.find_element_by_id("form:bookPDA").click()
wait(10)

# Search Availability
driver.find_element_by_name("manageBookingContainer:search").click()
wait(5)

logging.info('Get Sites')
# Select site
elem = Select(driver.find_element_by_name("searchBookingContainer:siteCode"))
num_of_site = len(elem.options)
avail_booking = {elem.options[i].text:[] for i in range(num_of_site)}

logging.info('Start Scanning')
while True:
    for i in range(num_of_site):
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
    
    if len(avail_booking['Cannington']) > 0:
        msg = ', '.join(avail_booking['Cannington'])
        send_msg_via_mail(msg)
        logging.info("Email sent")
    else:
        logging.info("Nothing available. Waiting for the next run.")
        
    
    random_wait(1500, 1600)
