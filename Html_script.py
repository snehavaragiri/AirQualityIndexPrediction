# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 21:34:41 2019

@author: krish.naik
"""
import os
import time
import requests  # helps to download the page in  the form of HMTL
import sys

# this functions is used to collect data for each and every month for all the years.
def retrieve_html():
    for year in range(2013,2019):
        for month in range(1,13):
            if(month<10):
                url='http://en.tutiempo.net/climate/0{}-{}/ws-421820.html'.format(month
                                                                          ,year)
            else:
                url='http://en.tutiempo.net/climate/{}-{}/ws-421820.html'.format(month
                                                                          ,year)
            texts=requests.get(url)   # Download the HTML and utf-8 encode it.
            text_utf=texts.text.encode('utf=8')
            
            #if the folder doesnot exists , create it
            if not os.path.exists("Data/Html_Data/{}".format(year)):
                os.makedirs("Data/Html_Data/{}".format(year))
            with open("Data/Html_Data/{}/{}.html".format(year,month),"wb") as output:    #open the folder and write it in write byte mode.
                output.write(text_utf)
            
        sys.stdout.flush()
        
if __name__=="__main__":
    start_time=time.time()
    retrieve_html()
    stop_time=time.time()
    print("Time taken {}".format(stop_time-start_time))
        
    
