import sys
import time
import code
import requests
import alpha_vantage
import json
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab 
import smtplib
import statistics as stat
import math
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

API_URL = "https://www.alphavantage.co/query?"


#####################################################################
#Volatility

symbols = ['VIX', 'TVIX', 'ZIV']#, '', '']
vix_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
tvix_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
ziv_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
#svxy_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
#uvxy_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
#vxxb_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}

vol_list = [vix_data, tvix_data, ziv_data]#, svxy_data, uvxy_data]


index = 0
while index <= len(vol_list)-1:
    dictionary = vol_list[index]
    symbol_specs = {
        "function" : "TIME_SERIES_DAILY",
        "symbol" : symbols[index],
        "outputsize": "full",
        "datatype" : "json",
        "apikey" :  "x00ZPIF6PN4TVK601"}
    
    response = requests.get(API_URL, params =  symbol_specs)
    data = response.json()
    dk = data.keys()

    if dk[0] != 'Meta Data':
        print(data[dk[0]])
        print('Fuck')
        break
    
    daily_data =  data[dk[1]]
    dates  = daily_data.keys()
    
    for date in dates:
        dictionary['date'].append(datetime.strptime(str(date), '%Y-%m-%d'))
    dictionary['date'].sort()
    for date in dictionary['date']:
        string_date = date.strftime('%Y-%m-%d')
        dictionary['open'].append(float(daily_data[string_date]['1. open']))
        dictionary['high'].append(float(daily_data[string_date]['2. high']))
        dictionary['low'].append(float(daily_data[string_date]['3. low']))
        dictionary['close'].append(float(daily_data[string_date]['4. close']))
    index+=1

time.sleep(60)

#Volatility Daily Data 

vix_today = {'date': [], 'price': [], 'change': [], 'change percent': [], 'low': [], 'high' : []}
tvix_today = {'date': [], 'price': [], 'change': [], 'change percent': [], 'low': [], 'high' : []}
ziv_today = {'date': [], 'price': [], 'change': [], 'change percent': [], 'low': [], 'high' : []}

vol_today_list = [vix_today, tvix_today, ziv_today]

index = 0
while index <= len(vol_today_list)-1:
    dictionary = vol_today_list[index]
    symbol_specs = {
        "function" : "Global_Quote",
        "symbol" : symbols[index],
        "datatype" : "json",
        "apikey" :  "x00ZPIF6PN4TVK601"}

    response = requests.get(API_URL, params =  symbol_specs)
    data = response.json()
   
    daily_data =  data['Global Quote']
    print(daily_data)
    
    dictionary['price'].append(float(daily_data['05. price']))
    dictionary['change'].append(float(daily_data['09. change']))
    dictionary['change percent'].append(float(daily_data['10. change percent'][:-1])/100)
    dictionary['low'].append(float(daily_data['04. low']))
    dictionary['high'].append(float(daily_data['03. high']))

    dictionary['date'].append(datetime.strptime(daily_data['07. latest trading day'],'%Y-%m-%d'))
    index+=1

    
########################################################################################################################
# Finding latest starting date for data to shorten the data
vix_start = vix_data['date'][0]
tvix_start = tvix_data['date'][0]
ziv_start = ziv_data['date'][0]

start_list = [vix_start, tvix_start, ziv_start]
start_list.sort()
start_date = start_list[-1]

#Start Date is the last split of TVIX which is the lastest split of any of the ETNs analyzed
start_date = datetime(2018, 9, 18, 0, 0)

#Finding index of Vol  start date
vix_index = vix_data['date'].index(start_date)
tvix_index = tvix_data['date'].index(start_date)
ziv_index = ziv_data['date'].index(start_date)

#Setting new start date of data using index of start date
vix_date = vix_data['date'][vix_index:]
vix_open = vix_data['open'][vix_index:]
vix_high = vix_data['high'][vix_index:]
vix_low = vix_data['low'][vix_index:]
vix_close = vix_data['close'][vix_index:]

tvix_date = tvix_data['date'][tvix_index:]
tvix_open = tvix_data['open'][tvix_index:]
tvix_high = tvix_data['high'][tvix_index:]
tvix_low = tvix_data['low'][tvix_index:]
tvix_close = tvix_data['close'][tvix_index:]

ziv_date = ziv_data['date'][ziv_index:]
ziv_open = ziv_data['open'][ziv_index:]
ziv_high = ziv_data['high'][ziv_index:]
ziv_low = ziv_data['low'][ziv_index:]
ziv_close = ziv_data['close'][ziv_index:]

# Normalizing all volatility values
vix_open_norm = [x/sum(vix_open) for x in vix_open]
vix_high_norm = [x/sum(vix_high) for x in vix_high]
vix_low_norm = [x/sum(vix_low) for x in vix_low]
vix_close_norm = [x/sum(vix_close) for x in vix_close]

tvix_open_norm = [x/sum(tvix_open) for x in tvix_open]
tvix_high_norm = [x/sum(tvix_high) for x in tvix_high]
tvix_low_norm = [x/sum(tvix_low) for x in tvix_low]
tvix_close_norm = [x/sum(tvix_close) for x in tvix_close]

ziv_open_norm = [x/sum(ziv_open) for x in ziv_open]
ziv_high_norm = [x/sum(ziv_high) for x in ziv_high]
ziv_low_norm = [x/sum(ziv_low) for x in ziv_low]
ziv_close_norm = [x/sum(ziv_close) for x in ziv_close]

########################################################
#Correlations
#VIX & TVIX
vix_tvix_corr = np.corrcoef(tvix_close, vix_close)[0][1]
#VIX & ZIV
vix_ziv_corr = np.corrcoef(ziv_close, vix_close)[0][1]

#Statistics

def getreport_data(close_list, today_dict):
    #Statistical Analysis
    today_date = today_dict['date'][0]
    today_price = today_dict['price'][0]

    diff1 = today_dict['change'][0]
    days = int(len(close_list))
    days3 = days-4
    days5 = days-6
    days14 = days-15    
    diff3 = today_price - (close_list[0:days3][-1])
    diff5 = today_price - (close_list[0:days5][-1])
    diff14 = today_price - (close_list[0:days14][-1])                           
    mean = stat.mean(close_list)
    median = stat.median(close_list)
    var = stat.pvariance(close_list, mean)    
    stdev = stat.pstdev(close_list)

    price_greater = []
    price_less = []
    for price in close_list:
        if today_price >= price:
            price_less.append(price)
        else:
            price_greater.append(price)
    percentile = float(len(price_less))/float(len(close_list))

    price_dict = {'today_date': today_date, 'today_price': today_price, 'diff1': diff1, 'diff3': diff3, 'diff5':diff5, 'diff14':diff14}
    stat_dict = {'mean': mean, 'median': median, 'stdev': stdev, 'var': var, 'percentile' : percentile}                            
    return [price_dict, stat_dict]

#Volatility Report Data
vix_report = getreport_data(vix_close, vix_today)
vix_mean = vix_report[1]['mean']
vix_median = vix_report[1]['median']
vix_stdev = vix_report[1]['stdev']
vix_var = vix_report[1]['var']
vix_percentile = vix_report[1]['percentile']

vix_today_date = vix_report[0]['today_date']
vix_today_price = vix_report[0]['today_price']
vix_diff1 = vix_report[0]['diff1']
vix_diff3 = vix_report[0]['diff3']
vix_diff5 = vix_report[0]['diff5']
vix_diff14 = vix_report[0]['diff14']

tvix_report = getreport_data(tvix_close, tvix_today)
tvix_mean = tvix_report[1]['mean']
tvix_median = tvix_report[1]['median']
tvix_stdev = tvix_report[1]['stdev']
tvix_var = tvix_report[1]['var']
tvix_percentile = tvix_report[1]['percentile']

tvix_today_date = tvix_report[0]['today_date']
tvix_today_price = tvix_report[0]['today_price']
tvix_diff1 = tvix_report[0]['diff1']
tvix_diff3 = tvix_report[0]['diff3']
tvix_diff5 = tvix_report[0]['diff5']
tvix_diff14 = tvix_report[0]['diff14']

ziv_report = getreport_data(ziv_close, ziv_today)
ziv_mean = ziv_report[1]['mean']
ziv_median = ziv_report[1]['median']
ziv_stdev = ziv_report[1]['stdev']
ziv_var = ziv_report[1]['var']
ziv_percentile = ziv_report[1]['percentile']

ziv_today_date = ziv_report[0]['today_date']
ziv_today_price = ziv_report[0]['today_price']
ziv_diff1 = ziv_report[0]['diff1']
ziv_diff3 = ziv_report[0]['diff3']
ziv_diff5 = ziv_report[0]['diff5']
ziv_diff14 = ziv_report[0]['diff14']

################################################################################################################

time_stamp = datetime.now()
time_stamp = time_stamp.strftime('%Y_%m_%d.%H-%M')
file_list = []

#Histograms            
plt.figure(1)
plt.title('VIX' + '     Start Date: ' + str(start_date))
n, bins, patches = plt.hist(vix_close, 200 ,density =1, facecolor='green') 
y = mlab.normpdf(bins, vix_mean, vix_stdev)
l = plt.plot(bins, y, 'r--', linewidth = 1)
plt.axvline(x=vix_today_price, color = 'r', linestyle = '--', linewidth =2, label = 'Price Now: ' + str(vix_today_price) + ' Percentile: ' + str(vix_percentile))
plt.axvline(x=vix_mean, color = 'b',linestyle = '--', label= 'Mean' + str(vix_mean))
plt.axvline(x= vix_mean+vix_stdev, ymin=0, color = 'b', linestyle = '--', label ='Mean + Stdev ' + str(float(vix_mean+vix_stdev)))
plt.axvline(x = vix_mean-vix_stdev, ymin=0, color = 'b', linestyle = '--', label= 'Mean-Stdev ' + str(float(vix_mean-vix_stdev)))
plt.axvline(x= min(vix_close), ymin=0, color = 'b', linestyle = '--', label ='Min ' + str(min(vix_close)))
plt.axvline(x = max(vix_close), ymin=0, color = 'b', linestyle = '--', label= 'Max ' + str(max(vix_close)))
plt.legend()
plt.grid(True)
#Save Figure
plt.savefig('VIX_Histogram_' + time_stamp +'.png')
file_list.append('VIX_Histogram_' + time_stamp +'.png')

plt.figure(2)
plt.title('TVIX' + '     Start Date: ' + str(start_date))
n, bins, patches = plt.hist(tvix_close,200, density =1, facecolor='green') 
y = mlab.normpdf(bins, tvix_mean, tvix_stdev)
l = plt.plot(bins, y, 'r--', linewidth =1)
plt.axvline(x=tvix_today_price, ymin = 0 ,color = 'r',linestyle = '--', linewidth =2, label = 'Price Now: ' + str(tvix_today_price) + ' Percentile: ' + str(tvix_percentile))
plt.axvline(x=tvix_mean, ymin = 0, color = 'b',linestyle = '--',label= 'Mean ' + str(tvix_mean))
plt.axvline(x= tvix_mean+tvix_stdev, ymin = 0, color = 'b', linestyle = '--', label ='Mean + Stdev ' + str(float(tvix_mean+tvix_stdev)))
plt.axvline(x = tvix_mean-tvix_stdev, ymin = 0, color = 'b', linestyle = '--', label= 'Mean-Stdev ' + str(float(tvix_mean-tvix_stdev)))
plt.axvline(x= min(tvix_close), ymin = 0, color = 'b', linestyle = '--', label ='Min ' + str(min(tvix_close)))
plt.axvline(x = max(tvix_close), ymin = 0, color = 'b', linestyle = '--', label= 'Max ' + str(max(tvix_close)))
plt.legend()
plt.grid(True)
plt.savefig('TVIX_Histogram_' + time_stamp +'.png')
file_list.append('TVIX_Histogram_' + time_stamp +'.png')

plt.figure(3)
plt.title('ZIV'+ '     Start Date: ' + str(start_date))
n, bins, patches = plt.hist(ziv_close,200,density = 1, facecolor='green') 
y = mlab.normpdf(bins, ziv_mean, ziv_stdev)
l = plt.plot(bins, y, 'r--', linewidth =1)
plt.axvline(x=ziv_today_price, ymin = 0, color = 'r', linestyle = '--', linewidth =2, label = 'Price Now ' + str(ziv_today_price) + ' Percentile: ' + str(ziv_percentile))
plt.axvline(x=ziv_mean, ymin = 0,  color = 'b', linestyle = '--', label= 'Mean ' + str(ziv_mean))
plt.axvline(x= ziv_mean+ziv_stdev, ymin = 0, color = 'b', linestyle = '--', label ='Mean + Stdev ' + str(float(ziv_mean+ziv_stdev)))
plt.axvline(x = ziv_mean-ziv_stdev, ymin = 0, color = 'b', linestyle = '--', label= 'Mean-Stdev ' + str(float(ziv_mean-ziv_stdev)))
plt.axvline(x= min(ziv_close), ymin = 0, color = 'b', linestyle = '--', label ='Min ' + str(min(ziv_close)))
plt.axvline(x = max(ziv_close), ymin = 0, color = 'b', linestyle = '--', label= 'Max ' + str(max(ziv_close)))
plt.legend()
plt.grid(True)
plt.savefig('ZIV_Histogram_' + time_stamp +'.png')
file_list.append('ZIV_Histogram_' + time_stamp +'.png')

plt.figure(4)
plt.plot(vix_date, vix_close_norm, 'k', label = 'VIX ')
plt.plot(tvix_date, tvix_close_norm, 'g', label = 'TVIX '+ str(vix_tvix_corr))
plt.plot(ziv_date, ziv_close_norm, 'b', label = 'ZIV '+ str(vix_ziv_corr))
plt.scatter(ziv_today_date, ziv_today_price/sum(ziv_close), s = 10, color = 'r', label = 'Today Price: ' +str(ziv_today_price)) 
plt.scatter(vix_today_date, vix_today_price/sum(vix_close), s = 10, color = 'r', label = 'Today Price: ' +str(vix_today_price)) 
plt.scatter(tvix_today_date, tvix_today_price/sum(tvix_close), s = 10, color = 'r', label = 'Today Price: ' +str(tvix_today_price)) 
plt.legend()
plt.savefig('Vol_Plot_' + time_stamp +'.png')
file_list.append('Vol_Plot_' + time_stamp +'.png')

#plt.show()

#Sending Email
vix_text = 'VIX \n' + 'Price Percentile: ' + str(vix_percentile) + '\n' + 'Today Gain: ' + str(vix_diff1) + '\n' + '3 Day Gain: ' + str(vix_diff3) + '\n' + '5 Day Gain: ' + str(vix_diff5) + '\n' + '14 Day Gain: ' + str(vix_diff14)+ '\n \n'

tvix_text = 'TVIX \n' + 'Price Percentile: ' + str(tvix_percentile) + '\n' + 'Today Gain: ' + str(tvix_diff1) + '\n' + '3 Day Gain: ' + str(tvix_diff3) + '\n' + '5 Day Gain: ' + str(tvix_diff5) + '\n' + '14 Day Gain: ' + str(tvix_diff14) + '\n \n'

ziv_text = 'ZIV \n' + 'Price Percentile: ' + str(ziv_percentile) + '\n' + 'Today Gain: ' + str(ziv_diff1) + '\n' + '3 Day Gain: ' + str(ziv_diff3) + '\n' + '5 Day Gain: ' + str(ziv_diff5) + '\n' + '14 Day Gain: ' + str(ziv_diff14)


def SendMail(img_file_names):
    msg = MIMEMultipart()
    msg['Subject'] = 'VIX Data Update'
    msg['From'] = 'nanis.nani.bot@gmail.com'
    msg['To'] = 'fruiz729@gmail.com'

    data_text = vix_text + tvix_text + ziv_text
    text = MIMEText(data_text)
    msg.attach(text)

    for file_name in img_file_names:
        img_data = open(file_name, 'rb').read()
        image = MIMEImage(img_data, name=os.path.basename(file_name))
        msg.attach(image)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('nanis.nani.bot@gmail.com', 'nanibotsocool')
    s.sendmail('nanis.nani.bot@gmail.com', 'fruiz729@gmail.com', msg.as_string())
    s.quit()

try:    
    SendMail(file_list)
    print('Email Sent')
except:
    print('Email Failed to Send')
