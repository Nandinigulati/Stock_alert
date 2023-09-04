import os
import smtplib
import imghdr
import time
from email.message import EmailMessage

import yfinance as yf

from yahoo_fin import stock_info
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr


msg=EmailMessage()

EMAIL_ADDRESS = '123@gmail.com'
EMAIL_PASSWORD = '**' 

yf.pdr_override()
start=dt.datetime(2023,8,28)
end=dt.datetime.now()

stock_targets = {
    "SBIN.NS": 570,
    "UNIONBANK.NS": 86,
}


alerted=False
 
while True:
    for stock, target_price in stock_targets.items():
        ticker = yf.Ticker(stock)
        df= pdr.get_data_yahoo(stock, start, end)
        currentPrice= df["Adj Close"][-1]

        condition= currentPrice>= target_price

        if (condition and alerted==False):
            message = stock + " has achieved the target " + str(target_price) +\
            "\nCurrent Price: " +str(currentPrice)
            print(message)
            #del stock_targets[stock]
            msg.set_content(message)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
                smtp.send_message(msg)

        else:
            new_message= stock+ " yet to achieve target."
            print(new_message)
            

    time.sleep(30)


    

