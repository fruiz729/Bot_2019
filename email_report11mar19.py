import time
import code
import requests
import alpha_vantage
import json
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import smtplib

API_URL = "https://www.alphavantage.co/query?"
#####################################################################
#Vanguard ETFS
#VT = Total World Stock
#ESGV = ESG USA Stock
#VSGX = ESG International Stock
#VWO = Emerging Markets
#VPU = Utilities 

symbols = ['VT', 'ESGV', 'VSGX', 'VWO', 'VPU']
vt_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
esgv_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
vsgx_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
vwo_data =  {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
vpu_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}

vol_list = [vt_data, esgv_data, vsgx_data, vwo_data, vpu_data]

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

########################################################################################
########################################################################################
#USD to EUR, GBP
symbols = ["EUR", "GBP"]
    
eur_data =  {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
#mxn_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
#cad_data =  {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
#cnh_data =  {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
gbp_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}

forex_list = [eur_data, gbp_data] # mxn_data, cad_data, cnh_data, gbp_data]

index = 0
while index <= len(forex_list)-1:
    dictionary = forex_list[index]
    symbol_specs = {
        "function" : "FX_DAILY",
        "from_symbol" : symbols[index],
        "to_symbol" : "USD",
        "outputsize": "full",
        "datatype" : "json",
        "apikey" :  "x00ZPIF6PN4TVK601"}
    
    response = requests.get(API_URL, params =  symbol_specs)
    print(response.status_code)
    data = response.json()
    dk = data.keys()
    print(dk)
    
    if dk[0] != 'Meta Data':
        print('Fuck')
        print(data[dk[0]])

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

########################################################################################################################
# Finding latest starting date for data to shorten the data
vt_start = vt_data['date'][0]
esgv_start = esgv_data['date'][0]
vsgx_start = vsgx_data['date'][0]
vpu_start = vpu_data['date'][0]
vwo_start = vwo_data['date'][0]

vix_start = vix_data['date'][0]
tvix_start = tvix_data['date'][0]
ziv_start = ziv_data['date'][0]

eur_start = eur_data['date'][0]
gbp_start = gbp_data['date'][0]

start_list = [vt_start, esgv_start, vsgx_start, vpu_start, vwo_start, vix_start, tvix_start, ziv_start, eur_start, gbp_start]
start_list.sort()
start_date = start_list[-1]
#start_date = datetime(2018, 9, 18, 0, 0)

#Finding index of Index and commodity start date
vt_index = vt_data['date'].index(start_date)
esgv_index = esgv_data['date'].index(start_date)
vsgx_index = vsgx_data['date'].index(start_date)
vpu_index = vpu_data['date'].index(start_date)
vwo_index = vwo_data['date'].index(start_date)

#Setting new start date of data using index of start date
vt_date = vt_data['date'][vt_index:]
vt_open = vt_data['open'][vt_index:]
vt_high = vt_data['high'][vt_index:]
vt_low = vt_data['low'][vt_index:]
vt_close = vt_data['close'][vt_index:]

esgv_date = esgv_data['date'][esgv_index:]
esgv_open = esgv_data['open'][esgv_index:]
esgv_high = esgv_data['high'][esgv_index:]
esgv_low = esgv_data['low'][esgv_index:]
esgv_close = esgv_data['close'][esgv_index:]

vsgx_date = vsgx_data['date'][vsgx_index:]
vsgx_open = vsgx_data['open'][vsgx_index:]
vsgx_high = vsgx_data['high'][vsgx_index:]
vsgx_low = vsgx_data['low'][vsgx_index:]
vsgx_close = vsgx_data['close'][vsgx_index:]

vpu_date = vpu_data['date'][vpu_index:]
vpu_open = vpu_data['open'][vpu_index:]
vpu_high = vpu_data['high'][vpu_index:]
vpu_low = vpu_data['low'][vpu_index:]
vpu_close = vpu_data['close'][vpu_index:]

vwo_date = vwo_data['date'][vwo_index:]
vwo_open = vwo_data['open'][vwo_index:]
vwo_high = vwo_data['high'][vwo_index:]
vwo_low = vwo_data['low'][vwo_index:]
vwo_close = vwo_data['close'][vwo_index:]

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

#Finding index of Forex start date
eur_index = eur_data['date'].index(start_date)
gbp_index = gbp_data['date'].index(start_date)

#Setting new start date of Forex date data
eur_date = eur_data['date'][eur_index:]
eur_open = eur_data['open'][eur_index:]
eur_high = eur_data['high'][eur_index:]
eur_low = eur_data['low'][eur_index:]
eur_close = eur_data['close'][eur_index:]

gbp_date = gbp_data['date'][gbp_index:]
gbp_open = gbp_data['open'][gbp_index:]
gbp_high = gbp_data['high'][gbp_index:]
gbp_low = gbp_data['low'][gbp_index:]
gbp_close = gbp_data['close'][gbp_index:]

#Finding dates that are not in volatility data
eur_date_list = []
gbp_date_list = []

for date in eur_date:
    if not date in vix_date:
        eur_date_list.append(date)
for date in gbp_date:
    if not date in vix_date:
        gbp_date_list.append(date)

vix_date_list = []
for date in vix_date:
    if not date in eur_date:
        vix_date_list.append(date)
    
vt_date_list = []
for date in vt_date:
    if not date in eur_date:
        vt_date_list.append(date)
        
#Setting new start date of data using index of start date
for date in eur_date_list:
    eur_index = eur_date.index(date)
    eur_open.pop(eur_index)
    eur_high.pop(eur_index)
    eur_low.pop(eur_index)
    eur_close.pop(eur_index)
    eur_date.remove(date)


for date in gbp_date_list:    
    gbp_index = gbp_date.index(date)
    gbp_open.pop(gbp_index)
    gbp_high.pop(gbp_index)
    gbp_low.pop(gbp_index)
    gbp_close.pop(gbp_index)
    gbp_date.pop(gbp_index)

for date in vix_date_list:    
    vix_index = vix_date.index(date)
    vix_open.pop(vix_index)
    vix_high.pop(vix_index)
    vix_low.pop(vix_index)
    vix_close.pop(vix_index)
    vix_date.pop(vix_index)

    tvix_index = tvix_date.index(date)
    tvix_open.pop(tvix_index)
    tvix_high.pop(tvix_index)
    tvix_low.pop(tvix_index)
    tvix_close.pop(tvix_index)
    tvix_date.pop(tvix_index)

    ziv_index = ziv_date.index(date)
    ziv_open.pop(ziv_index)
    ziv_high.pop(ziv_index)
    ziv_low.pop(ziv_index)
    ziv_close.pop(ziv_index)
    ziv_date.pop(ziv_index)

for date in vt_date_list:    
    vt_index = vt_date.index(date)
    vt_open.pop(vt_index)
    vt_high.pop(vt_index)
    vt_low.pop(vt_index)
    vt_close.pop(vt_index)
    vt_date.pop(vt_index)

    esgv_index = esgv_date.index(date)
    esgv_open.pop(esgv_index)
    esgv_high.pop(esgv_index)
    esgv_low.pop(esgv_index)
    esgv_close.pop(esgv_index)
    esgv_date.pop(esgv_index)

    vsgx_index = vsgx_date.index(date)
    vsgx_open.pop(vsgx_index)
    vsgx_high.pop(vsgx_index)
    vsgx_low.pop(vsgx_index)
    vsgx_close.pop(vsgx_index)
    vsgx_date.pop(vsgx_index)

    vpu_index = vpu_date.index(date)
    vpu_open.pop(vpu_index)
    vpu_high.pop(vpu_index)
    vpu_low.pop(vpu_index)
    vpu_close.pop(vpu_index)
    vpu_date.pop(vpu_index)

    vwo_index = vwo_date.index(date)
    vwo_open.pop(vwo_index)
    vwo_high.pop(vwo_index)
    vwo_low.pop(vwo_index)
    vwo_close.pop(vwo_index)
    vwo_date.pop(vwo_index)

# Normalizing all Indeces and Commodity values
vt_open_norm = [x/sum(vt_open) for x in vt_open]
vt_high_norm = [x/sum(vt_high) for x in vt_high]
vt_low_norm = [x/sum(vt_low) for x in vt_low]
vt_close_norm = [x/sum(vt_close) for x in vt_close]

esgv_open_norm = [x/sum(esgv_open) for x in esgv_open]
esgv_high_norm = [x/sum(esgv_high) for x in esgv_high]
esgv_low_norm = [x/sum(esgv_low) for x in esgv_low]
esgv_close_norm = [x/sum(esgv_close) for x in esgv_close]

vsgx_open_norm = [x/sum(vsgx_open) for x in vsgx_open]
vsgx_high_norm = [x/sum(vsgx_high) for x in vsgx_high]
vsgx_low_norm = [x/sum(vsgx_low) for x in vsgx_low]
vsgx_close_norm = [x/sum(vsgx_close) for x in vsgx_close]

vpu_open_norm = [x/sum(vpu_open) for x in vpu_open]
vpu_high_norm = [x/sum(vpu_high) for x in vpu_high]
vpu_low_norm = [x/sum(vpu_low) for x in vpu_low]
vpu_close_norm = [x/sum(vpu_close) for x in vpu_close]

vwo_open_norm = [x/sum(vwo_open) for x in vwo_open]
vwo_high_norm = [x/sum(vwo_high) for x in vwo_high]
vwo_low_norm = [x/sum(vwo_low) for x in vwo_low]
vwo_close_norm = [x/sum(vwo_close) for x in vwo_close]    
    
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

# Normalizing all Forex  values
eur_open_norm = [x/sum(eur_open) for x in eur_open]
eur_high_norm = [x/sum(eur_high) for x in eur_high]
eur_low_norm = [x/sum(eur_low) for x in eur_low]
eur_close_norm = [x/sum(eur_close) for x in eur_close]

gbp_open_norm = [x/sum(gbp_open) for x in gbp_open]
gbp_high_norm = [x/sum(gbp_high) for x in gbp_high]
gbp_low_norm = [x/sum(gbp_low) for x in gbp_low]
gbp_close_norm = [x/sum(gbp_close) for x in gbp_close]
########################################################
#Correlations
#VIX & TVIX
vix_tvix_corr = np.corrcoef(tvix_close, vix_close)[0][1]
#VIX & ZIV
vix_ziv_corr = np.corrcoef(ziv_close, vix_close)[0][1]

#VIX & VT
vix_vt_corr = np.corrcoef(vt_close, vix_close)[0][1]
#VIX & ESGV
vix_esgv_corr = np.corrcoef(esgv_close, vix_close)[0][1]
#VIX & Vsgx
vix_vsgx_corr = np.corrcoef(vsgx_close, vix_close)[0][1]
#VIX & VPU
vix_vpu_corr = np.corrcoef(vpu_close, vix_close)[0][1]
#VIX & VWO
vix_vwo_corr = np.corrcoef(vwo_close, vix_close)[0][1]


for date in vix_date:
    if not date in eur_date:
        print('euro date')
        print(date)
        print('________')
    if not date in gbp_date:
        print('gbp date')
        print(date)
        print('________')

#VIX & EUR        
vix_eur_corr = np.corrcoef(eur_close, vix_close)[0][1]
#VIX & GBP
vix_gbp_corr = np.corrcoef(gbp_close, vix_close)[0][1]


#Best Fit Polynomial

# variable_day = np.arange(1.0, float(len(vix_close)+1), 1)

# i = 2
# best_corr = 0.0
# while i < 100:
#     coeffs = poly.polyfit(variable_day, vix_close, i)
#     fit = poly.polyval(variable_day, coeffs)
#     corr = np.corrcoef(vix_close, fit)[0][1]
#     if corr > best_corr:
#         best_corr = corr
#         best_deg = i
#     i+=1
    

# vix_coeffs = poly.polyfit(variable_day, vix_close, best_deg)

# tvix_coeffs = poly.polyfit(variable_day,tvix_close, 9)
# ziv_coeffs = poly.polyfit(variable_day, ziv_close, 9)
# svxy_coeffs = poly.polyfit(variable_day, svxy_close, 9)
# uvxy_coeffs = poly.polyfit(variable_day, uvxy_close, 9)
# vxxb_coeffs = poly.polyfit(variable_day, vxxb_close, 9)

# vix_fit = poly.polyval(variable_day, vix_coeffs)

# variable_day_long = (1, 100,1)
# vix_fit_long = poly.polyval(variable_day_long, vix_coeffs)
 
################################################################################################################
#Graphs

plt.figure(1)
plt.title('Volatility')
plt.plot(vix_date, vix_close_norm, 'k', label = 'VIX ')
plt.plot(tvix_date, tvix_close_norm, 'r', label = 'TVIX '+ str(vix_tvix_corr))
plt.plot(ziv_date, ziv_close_norm, 'b', label = 'ZIV '+ str(vix_ziv_corr))
#plt.plot(svxy_date, svxy_close_norm, 'm', label = 'SVXY '+ str(vix_svxy_corr))
#plt.plot(uvxy_date, uvxy_close_norm, 'g', label = 'UVXY '+ str(vix_uvxy_corr))
plt.legend()

plt.figure(2)
plt.title('Forex')
plt.plot(gbp_date, gbp_close, 'm', label = 'GBP '+ str(vix_gbp_corr))
plt.plot(eur_date, eur_close, 'g', label = 'EUR '+ str(vix_eur_corr))
#plt.plot(mxn_date, mxn_close_norm, 'b', label = 'MXN '+ str(vix_mxn_corr))
#plt.plot(cad_date, cad_close_norm, 'r', label = 'CAD '+ str(vix_cad_corr))
#plt.plot(cnh_date, cnh_close_norm, 'y', label = 'CNH '+ str(vix_cnh_corr))
plt.legend()


plt.figure(3)
plt.title('Indeces & Global ETFs')
plt.plot(vt_date, vt_close_norm, 'm', label = 'VT-World '+ str(vix_vt_corr))
plt.plot(esgv_date, esgv_close_norm, 'g', label = 'ESG  USA '+ str(vix_esgv_corr))
plt.plot(vsgx_date, vsgx_close_norm, 'b', label = 'ESG Inernational'+ str(vix_vsgx_corr))
plt.plot(vpu_date, vpu_close_norm, 'r', label = 'VPU Utilities '+ str(vix_vpu_corr))
plt.plot(vwo_date, vwo_close_norm, 'y', label = 'VWO Emerging Markets '+ str(vix_vwo_corr))
plt.legend()
plt.show()

#Sending Email

text = "Vanguard ETFs" + '/n' + '/n' +
'VT - Total World Stock'+ '/n' + 
'Current Price = ' + '/n' 
'Price_Percentile = ' + '/n'
'1 day gain = ' + '/n'
'3 day gain = ' + '/n'
'5 day gain = ' + '/n'
'14 day gain = ' + '/n' + '/n'

'ESGV - ESG US Stock'+ '/n'+ 
'Current Price = ' + '/n' 
'Price_Percentile = ' + '/n'
'1 day gain = ' + '/n'
'3 day gain = ' + '/n'
'5 day gain = ' + '/n'
'14 day gain = ' + '/n' + '/n'




try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('nanis.nani.bot@gmail.com', 'nanibotsocool')
    server.sendmail('nanis.nani.bot@gmail.com', 'fruiz729@gmail.com', text)
    server.close()

    print('Sent')
   
except:
    print('Something went wrong :(')
