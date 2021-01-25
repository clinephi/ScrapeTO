# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 23:42:31 2021

@author: phili
"""
import time, datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import smtplib, ssl

# === SETUP EMAIL CLIENT === #
port = 465  # For SSL
sender_email = "philip.business78@gmail.com"
receiver_email = ["philip.cline@gmail.com" , "carwanasarah@gmail.com"]
password = "EglestonSquare78!"
context = ssl.create_default_context()
# ==================== # 

# SOME INPUT VARIABLES # 
driver_link = "C:/Users/phili/OneDrive - University of Toronto/Documents/U of T/4.0_Fourth_Year/scrape_skating_reservations/chromedriver_win32/chromedriver.exe"
skate_link = "https://www.toronto.ca/explore-enjoy/recreation/skating-winter-sports/public-leisure-skating/#location=&lat=43.658434&lng=-79.513550" 
delay = 20 # seconds 
# ==================== # 

keep_running = True
print( "starting up ...") 
while (keep_running): 
    try: 
        print( "Running webscraper @ ...", datetime.datetime.now() )
        
        # RERUN OUR WEBDRIVER:
        wd = webdriver.Chrome( driver_link )  
        wd.get(skate_link) 
    
        b = WebDriverWait(wd, delay).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()=" Filter Results"]'))
            )
        print( "filter button found "  )
        b.click() 
        
        chkbox = WebDriverWait(wd, delay).until(
                EC.presence_of_element_located((By.ID, 'checkbox0-0-1')) 
            )
        print( "chkbox button found "  )
        chkbox.click()
        
        reserve = WebDriverWait(wd, delay).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#listViewBox > li:nth-child(2) > div > div.listingItem__template > div > div.col-xs-12.col-sm-8 > div > button[data-title='Colonel Samuel Smith Park']" ))
            )
        print( "reserve button found " )
        reserve.click()
        
        # -- Made it to reservation page -- # 
        time.sleep( 10 ) 
        rows = wd.find_elements_by_css_selector( "#reservationtableData > tbody > tr" ) ##reservationtableData > tbody > tr:nth-child(1)
    
        for r in rows:
            if ( ("Available" in r.text) or ("Some Spots Left" in r.text)) :
                print( "sending off email...")
                SUBJECT = "Skating rink update"
                TEXT = "There is an opening at the Colonel Samuel Smith Park. \nDetails: \n" + r.text
                message = 'Subject: {}\n\n{}\n\n Link:{}'.format(SUBJECT, TEXT, skate_link)
                
                with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                    server.login( sender_email , password)
                    server.sendmail(sender_email, receiver_email, message)
        
        print( "Successfully exiting webscraper" )
        wd.quit()
        time.sleep( 1800 ) # run every 30 minutes. 
        
    except TimeoutException: 
        print( "loading too long or errored out ... ")
    except: 
        print( "another bad error occurred .. ") 

    