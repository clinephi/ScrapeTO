# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 00:38:45 2021

@author: phili
"""
# test email setup: 
import smtplib, ssl

port = 465  # For SSL

# === INPUTS === # 
sender_email = "saraha78t@gmail.com"
receiver_email = ["philip.cline@gmail.com", "carwanasarah@gmail.com"]
message = """\
Subject: Skating rink update

There is an opening at the Colonel Samuel Smith Park. 
Details:  """
# ===============# 
password = input("Type your password and press enter: ")
# password is: DufferinGrove78!

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("saraha78t@gmail.com", password)
    server.sendmail(sender_email, receiver_email, message)
