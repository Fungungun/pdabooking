from selenium import webdriver
from selenium.webdriver.support.ui import Select

import logging
from datetime import date, time

from utils import *

logging.basicConfig(
    handlers=[logging.FileHandler("run.log", mode='a'),
                logging.StreamHandler()
    ],
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%d/%m/%y %H:%M:%S')

start_date = date(2021, 5, 28)
end_date = date(2021, 6, 3)
start_time = time(7, 0, 0)
end_time = time(18, 0, 0)


if __name__ == "__main__":

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    # driver = webdriver.PhantomJS()

    driver.implicitly_wait(30)

    driver.get(('https://online.transport.wa.gov.au/tso/selfservice/public/login.jsf'))

    elem = driver.find_element_by_name("loginForm:userId")
    elem.send_keys("caohui2")

    elem = driver.find_element_by_name("loginForm:password")
    elem.send_keys("vrGR479wFokc")

    driver.find_element_by_name("loginForm:loginButton").click()
    wait(10)
    driver.find_element_by_id("menuForm:menubar_licence").click()
    wait(10)
    try:
        driver.find_element_by_id("form:bookPDA").click()
    except:
        driver.find_element_by_id("form:j_idt219").click() # manage booking
        driver.find_element_by_xpath("//*[@id='id6']").click() # manage booking
    wait(5)

    # Search Availability
    try:
        driver.find_element_by_name("manageBookingContainer:search").click()
        wait(5)
    except:
        logging.info('Change booking')    

    logging.info('Get Sites')
    # Select site
    elem = Select(driver.find_element_by_name("searchBookingContainer:siteCode"))
    num_of_site = len(elem.options)


    logging.info('Start Scanning')
    while True:
        avail_booking = {elem.options[i].text:[] for i in range(num_of_site)}

        for i in range(num_of_site):
            
            site = elem.options[i].text
            if site != "Cannington":
                continue

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
                logging.info([x.text for x in elem_booking])
                for i in range(len(elem_booking)):
                    if check_if_expected_datetime(elem_booking[i].text, start_date, end_date, start_time, end_time):
                        msg = f"Make booking {elem_booking[i].text}"
                        logging.info(msg)
                        driver.find_element_by_id(f"searchResultRadio{i}").click() # select booking
                        wait(1)
                        driver.find_element_by_xpath("//*[@id='id1a']").click() # confirm booking 
                        send_msg_via_mail(msg)
                        logging.info("Email sent")
                        exit()
            logging.info("Nothing available. Waiting for the next run.")
                    
            
        
        random_wait(60, 120)
