
import random
import time

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import datetime

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

def convert_datetime_format(unformatted_datetime):
    return datetime.strptime(unformatted_datetime, "%d/%m/%Y at %I:%M %p")
    

def check_if_expected_datetime(search_res, start_date, end_date, start_time, end_time):
    res_datetime = convert_datetime_format(search_res)
    res_date = res_datetime.date()
    res_time = res_datetime.time()
    return start_date <= res_date <= end_date and start_time <= res_time <= end_time

