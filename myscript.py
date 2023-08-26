"""_tracking element price on a certain amazon link using lxml and beautiful soup methods _
    """

import requests
from bs4 import BeautifulSoup
from lxml import html
import time
import smtplib
from email.mime.text import MIMEText


########################################################################
## 1--- utilizing requests module to open up the live site
########################################################################
## general heading parameters 
user_agent= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
accept_language="en-US,en;q=0.9"
web_site = "https://www.amazon.eg/%D8%A7%D9%84%D8%AD%D9%85%D8%A7%D9%8A%D8%A9-%D8%A7%D9%84%D8%AA%D9%8A%D8%A7%D8%B1-%D8%A7%D9%84%D9%83%D9%87%D8%B1%D8%A8%D8%A7%D8%A6%D9%8A-%D9%84%D9%84%D8%AA%D8%B9%D8%AF%D9%8A%D9%84-OPS1-63A/dp/B0C6J2PGJR/ref=sr_1_2?keywords=over+under+voltage+protector&qid=1692363543&sprefix=over+,aps,184&sr=8-2&language=en_AE"

## -------- establishing a connection to the site with REQUESTS  module -------
site_requested_headers={"user_agent": user_agent, "accept_language":accept_language}
site_response = requests.get(web_site, headers=site_requested_headers)
tries_count = 11
retry_delay = 0.2  # seconds
tries = 0
def connect_with_retries(url, headers, max_retries=tries_count, retry_delay=retry_delay):
    global tries
    tries+=1
    for _ in range(1,max_retries):
        site_response = requests.get(url, headers=headers)
        if site_response.status_code == 200:
            return site_response
        time.sleep(retry_delay)
    
    return None

site_response = connect_with_retries(web_site, site_requested_headers, tries_count, retry_delay)

if site_response is not None:
    
    print(f"Connected successfully to the site ,after {tries} tries" )

else:
    print(f"After {tries_count} tries, Request failed with status code: {site_response.status_code}")
    exit()

#
##########################################################################
##2----- There are 2 methods of scrapping , the other one is at the end.
##-- using beautiful soup method  to retrieve the data from online site 
# after having <Response [200]> from requests module.
###################################################################################################
soup = BeautifulSoup(site_response.content,"lxml")
price = soup.find(class_="a-offscreen").get_text()
price_without_currency = price.split("EGP")[1]
price_as_float = float(price_without_currency)
# print(price_as_float)

product_name = soup.find(class_="a-size-large product-title-word-break").get_text()
# print(product_name)
#
#
#
#
##############################################################################
## -------- sending the message by mail  -------#
##############################################################################
expected_price = 750

if price_as_float > expected_price:
    sender_email = "ahmed0abdo0test@hotmail.com"
    subject = "price is down, shopping time"
    message = f"{product_name} is available now for{price_as_float}"
    # message = "This is a test email."
    receiver_email = "ahmed0abdo0test@gmail.com"


    smtp_server = "smtp.office365.com"
    smtp_port = 587
    smtp_username = "ahmed0abdo0test@hotmail.com"
    smtp_password = "Test5398"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

else:
    print("price is high")
