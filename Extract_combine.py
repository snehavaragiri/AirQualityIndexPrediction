from Plot_AQI import avg_data_2013,avg_data_2014,avg_data_2015,avg_data_2016
import requests
import sys
import pandas as pd
from bs4 import BeautifulSoup
import os
import csv

def met_data(month, year):
    
    file_html = open('Data/Html_Data/{}/{}.html'.format(year,month), 'rb')
    plain_text = file_html.read()   # read the entire content from the html file to plain_text.

    tempD = []
    finalD = []
    
    #initialize the BeautifulSoup. pass the html content and lxml to it. lxml is the format used for web scrapping.
    soup = BeautifulSoup(plain_text, "lxml")
    for table in soup.findAll('table', {'class': 'medias mensuales numspan'}):  #On table tag find the whole class medias mensuales numspan
        for tbody in table:          #iterate through tbody tage in table 
            for tr in tbody:         ##iterate through tr tage in tbody 
                a = tr.get_text()    # from tr tag get the entire row of the table(contains 15 features) 
                tempD.append(a)      #append the text to tempD variable.

    rows = len(tempD) / 15  # number of rows = total no of rows / no of features

    for times in range(round(rows)):
        newtempD = []
        for i in range(15):
            newtempD.append(tempD[0])
            tempD.pop(0)
        finalD.append(newtempD)

    length = len(finalD)

    finalD.pop(length - 1)  # delete the last row which isnt needed.
    finalD.pop(0)           # Pop the 0th row.. which is the feature names

    for a in range(len(finalD)):      # pop the 0,6,9,10,11,12,13 columns
        finalD[a].pop(6)
        finalD[a].pop(13)
        finalD[a].pop(12)
        finalD[a].pop(11)
        finalD[a].pop(10)
        finalD[a].pop(9)
        finalD[a].pop(0)

    return finalD

def data_combine(year, cs):
    for a in pd.read_csv('Data/Real-Data/real_' + str(year) + '.csv', chunksize=cs):
        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
    return mylist


if __name__ == "__main__":
    #create if the folder doesnt exists
    if not os.path.exists("Data/Real-Data"):
        os.makedirs("Data/Real-Data")
    for year in range(2013, 2017): #iterate through 2013 to 2017
        final_data = []
        with open('Data/Real-Data/real_' + str(year) + '.csv', 'w') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')  # save the file as csv.. Dialect is styling
            # write these column names as 1st row
            wr.writerow(
                ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        for month in range(1, 13):    #iterate through every month of the year.
            temp = met_data(month, year)      # webScrap the data from html
            final_data = final_data + temp    # this gives all the independent features data
            
        pm = getattr(sys.modules[__name__], 'avg_data_{}'.format(year))()   # get the dependent feature data

        if len(pm) == 364:
            pm.insert(364, '-')

        for i in range(len(final_data)-1): #iterate through every row in final data and add pm value in last column(PM2.5)
            # final[i].insert(0, i + 1)
            final_data[i].insert(8, pm[i])  # add as 8 th row

        with open('Data/Real-Data/real_' + str(year) + '.csv', 'a') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            for row in final_data:
                flag = 0
                for elem in row:
                    if elem == "" or elem == "-":
                        flag = 1
                if flag != 1:
                    wr.writerow(row)
                    
    data_2013 = data_combine(2013, 600)
    data_2014 = data_combine(2014, 600)
    data_2015 = data_combine(2015, 600)
    data_2016 = data_combine(2016, 600)
     
    total=data_2013+data_2014+data_2015+data_2016
    
    with open('Data/Real-Data/Real_Combine.csv', 'w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)
        
        
df=pd.read_csv('Data/Real-Data/Real_Combine.csv')