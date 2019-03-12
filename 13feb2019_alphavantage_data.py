import time
import code
import requests
import alpha_vantage
import json
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import code

API_URL = "https://www.alphavantage.co/query?"
#####################################################################
#Major World Indeces plus crude oil and gold

symbols = ['VEA', 'INX', 'VGK', 'VPL', 'VWO']
vea_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
inx_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
vgk_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
vpl_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
vwo_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}

vol_list = [vea_data,inx_data,vgk_data,vpl_data,vwo_data]

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

print(float(len(vea_data['close'])+len(vgk_data['close'])+len(vpl_data['close'])+len(vwo_data['close']))*5)

time.sleep(60)
#####################################################################
#Volatility

symbols = ['VIX', 'TVIX', 'ZIV', 'SVXY', 'UVXY']
vix_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
tvix_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
ziv_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
svxy_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
uvxy_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
#vxxb_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}

vol_list = [vix_data, tvix_data, ziv_data, svxy_data, uvxy_data]

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

print(float(len(vix_data['close'])+len(tvix_data['close'])+len(ziv_data['close'])+len(svxy_data['close'])+len(uvxy_data['close']))*5)
time.sleep(60)

########################################################################################
########################################################################################
#USD to EUR, GDP, MXN, CAD
symbols = ["EUR", "MXN","CAD", "CNH", "GBP"]
    
eur_data =  {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
mxn_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
cad_data =  {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
cnh_data =  {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
gbp_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}

forex_list = [eur_data, mxn_data, cad_data, cnh_data, gbp_data]

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

print(float(len(vix_data['close'])+len(tvix_data['close'])+len(ziv_data['close'])+len(svxy_data['close'])+len(uvxy_data['close'])+len(eur_data['close']) + len(gbp_data['close'])+ len(mxn_data['close']) +len(cnh_data['close'])+len(cad_data['close']))*5) 
########################################################################################################################
# Finding latest starting date for data to shorten the data
vea_start = vea_data['date'][0]
inx_start = inx_data['date'][0]
vgk_start = vgk_data['date'][0]
vpl_start = vpl_data['date'][0]
vwo_start = vwo_data['date'][0]

vix_start = vix_data['date'][0]
tvix_start = tvix_data['date'][0]
ziv_start = ziv_data['date'][0]
svxy_start = svxy_data['date'][0]
uvxy_start = uvxy_data['date'][0]

eur_start = eur_data['date'][0]
mxn_start = mxn_data['date'][0]
cad_start = cad_data['date'][0]
cnh_start = cnh_data['date'][0]
gbp_start = gbp_data['date'][0]

start_list = [vix_start, tvix_start, ziv_start, svxy_start, uvxy_start, eur_start, mxn_start, cad_start, cnh_start, gbp_start]
start_list.sort()
#start_date = start_list[-1]
start_date = datetime(2018, 9, 18, 0, 0)

#Finding index of Index and commodity start date
vea_index = vea_data['date'].index(start_date)
inx_index = inx_data['date'].index(start_date)
vgk_index = vgk_data['date'].index(start_date)
vpl_index = vpl_data['date'].index(start_date)
vwo_index = vwo_data['date'].index(start_date)

#Setting new start date of data using index of start date
vea_date = vea_data['date'][vea_index:]
vea_open = vea_data['open'][vea_index:]
vea_high = vea_data['high'][vea_index:]
vea_low = vea_data['low'][vea_index:]
vea_close = vea_data['close'][vea_index:]

inx_date = inx_data['date'][inx_index:]
inx_open = inx_data['open'][inx_index:]
inx_high = inx_data['high'][inx_index:]
inx_low = inx_data['low'][inx_index:]
inx_close = inx_data['close'][inx_index:]

vgk_date = vgk_data['date'][vgk_index:]
vgk_open = vgk_data['open'][vgk_index:]
vgk_high = vgk_data['high'][vgk_index:]
vgk_low = vgk_data['low'][vgk_index:]
vgk_close = vgk_data['close'][vgk_index:]

vpl_date = vpl_data['date'][vpl_index:]
vpl_open = vpl_data['open'][vpl_index:]
vpl_high = vpl_data['high'][vpl_index:]
vpl_low = vpl_data['low'][vpl_index:]
vpl_close = vpl_data['close'][vpl_index:]

vwo_date = vwo_data['date'][vwo_index:]
vwo_open = vwo_data['open'][vwo_index:]
vwo_high = vwo_data['high'][vwo_index:]
vwo_low = vwo_data['low'][vwo_index:]
vwo_close = vwo_data['close'][vwo_index:]

#Finding index of Vol  start date
vix_index = vix_data['date'].index(start_date)
tvix_index = tvix_data['date'].index(start_date)
ziv_index = ziv_data['date'].index(start_date)
svxy_index = svxy_data['date'].index(start_date)
uvxy_index = uvxy_data['date'].index(start_date)

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

svxy_date = svxy_data['date'][svxy_index:]
svxy_open = svxy_data['open'][svxy_index:]
svxy_high = svxy_data['high'][svxy_index:]
svxy_low = svxy_data['low'][svxy_index:]
svxy_close = svxy_data['close'][svxy_index:]

uvxy_date = uvxy_data['date'][uvxy_index:]
uvxy_open = uvxy_data['open'][uvxy_index:]
uvxy_high = uvxy_data['high'][uvxy_index:]
uvxy_low = uvxy_data['low'][uvxy_index:]
uvxy_close = uvxy_data['close'][uvxy_index:]

#Finding index of Forex start date
eur_index = eur_data['date'].index(start_date)
mxn_index = mxn_data['date'].index(start_date)
cad_index = cad_data['date'].index(start_date)
cnh_index = cnh_data['date'].index(start_date)
gbp_index = gbp_data['date'].index(start_date)

#Setting new start date of Forex date data
eur_date = eur_data['date'][eur_index:]
eur_open = eur_data['open'][eur_index:]
eur_high = eur_data['high'][eur_index:]
eur_low = eur_data['low'][eur_index:]
eur_close = eur_data['close'][eur_index:]

mxn_date = mxn_data['date'][mxn_index:]
mxn_open = mxn_data['open'][mxn_index:]
mxn_high = mxn_data['high'][mxn_index:]
mxn_low = mxn_data['low'][mxn_index:]
mxn_close = mxn_data['close'][mxn_index:]

cad_date = cad_data['date'][cad_index:]
cad_open = cad_data['open'][cad_index:]
cad_high = cad_data['high'][cad_index:]
cad_low = cad_data['low'][cad_index:]
cad_close = cad_data['close'][cad_index:]

cnh_date = cnh_data['date'][cnh_index:]
cnh_open = cnh_data['open'][cnh_index:]
cnh_high = cnh_data['high'][cnh_index:]
cnh_low = cnh_data['low'][cnh_index:]
cnh_close = cnh_data['close'][cnh_index:]

gbp_date = gbp_data['date'][gbp_index:]
gbp_open = gbp_data['open'][gbp_index:]
gbp_high = gbp_data['high'][gbp_index:]
gbp_low = gbp_data['low'][gbp_index:]
gbp_close = gbp_data['close'][gbp_index:]

#Finding dates that are not in volatility data
eur_date_list = []
mxn_date_list = []
cad_date_list = []
cnh_date_list = []
gbp_date_list = []

for date in eur_date:
    if not date in vix_date:
        eur_date_list.append(date)
for date in mxn_date:
    if not date in vix_date:
        mxn_date_list.append(date)
for date in cad_date:
    if not date in vix_date:
        cad_date_list.append(date)
for date in cnh_date:
    if not date in vix_date:
        cnh_date_list.append(date)
for date in gbp_date:
    if not date in vix_date:
        gbp_date_list.append(date)

vix_date_list = []
for date in vix_date:
    if not date in eur_date:
        vix_date_list.append(date)
    
vea_date_list = []
for date in vea_date:
    if not date in eur_date:
        vea_date_list.append(date)
        
#Setting new start date of data using index of start date
for date in eur_date_list:
    eur_index = eur_date.index(date)
    eur_open.pop(eur_index)
    eur_high.pop(eur_index)
    eur_low.pop(eur_index)
    eur_close.pop(eur_index)
    eur_date.remove(date)

for date in mxn_date_list: 
    mxn_index = mxn_date.index(date)
    mxn_open.pop(mxn_index)
    mxn_high.pop(mxn_index)
    mxn_low.pop(mxn_index)
    mxn_close.pop(mxn_index)
    mxn_date.remove(date)

for date in cad_date_list:
    cad_index = cad_date.index(date)
    cad_open.pop(cad_index)
    cad_high.pop(cad_index)
    cad_low.pop(cad_index)
    cad_close.pop(cad_index)
    cad_date.pop(cad_index)

for date in cnh_date_list:
    cnh_index = cnh_date.index(date)
    cnh_open.pop(cnh_index)
    cnh_high.pop(cnh_index)
    cnh_low.pop(cnh_index)
    cnh_close.pop(cnh_index)
    cnh_date.pop(cnh_index)

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

    svxy_index = svxy_date.index(date)
    svxy_open.pop(svxy_index)
    svxy_high.pop(svxy_index)
    svxy_low.pop(svxy_index)
    svxy_close.pop(svxy_index)
    svxy_date.pop(svxy_index)

    uvxy_index = uvxy_date.index(date)
    uvxy_open.pop(uvxy_index)
    uvxy_high.pop(uvxy_index)
    uvxy_low.pop(uvxy_index)
    uvxy_close.pop(uvxy_index)
    uvxy_date.pop(uvxy_index)

for date in vea_date_list:    
    vea_index = vea_date.index(date)
    vea_open.pop(vea_index)
    vea_high.pop(vea_index)
    vea_low.pop(vea_index)
    vea_close.pop(vea_index)
    vea_date.pop(vea_index)

    inx_index = inx_date.index(date)
    inx_open.pop(inx_index)
    inx_high.pop(inx_index)
    inx_low.pop(inx_index)
    inx_close.pop(inx_index)
    inx_date.pop(inx_index)

    vgk_index = vgk_date.index(date)
    vgk_open.pop(vgk_index)
    vgk_high.pop(vgk_index)
    vgk_low.pop(vgk_index)
    vgk_close.pop(vgk_index)
    vgk_date.pop(vgk_index)

    vpl_index = vpl_date.index(date)
    vpl_open.pop(vpl_index)
    vpl_high.pop(vpl_index)
    vpl_low.pop(vpl_index)
    vpl_close.pop(vpl_index)
    vpl_date.pop(vpl_index)

    vwo_index = vwo_date.index(date)
    vwo_open.pop(vwo_index)
    vwo_high.pop(vwo_index)
    vwo_low.pop(vwo_index)
    vwo_close.pop(vwo_index)
    vwo_date.pop(vwo_index)

# Normalizing all Indeces and Commodity values
vea_open_norm = [x/sum(vea_open) for x in vea_open]
vea_high_norm = [x/sum(vea_high) for x in vea_high]
vea_low_norm = [x/sum(vea_low) for x in vea_low]
vea_close_norm = [x/sum(vea_close) for x in vea_close]

inx_open_norm = [x/sum(inx_open) for x in inx_open]
inx_high_norm = [x/sum(inx_high) for x in inx_high]
inx_low_norm = [x/sum(inx_low) for x in inx_low]
inx_close_norm = [x/sum(inx_close) for x in inx_close]

vgk_open_norm = [x/sum(vgk_open) for x in vgk_open]
vgk_high_norm = [x/sum(vgk_high) for x in vgk_high]
vgk_low_norm = [x/sum(vgk_low) for x in vgk_low]
vgk_close_norm = [x/sum(vgk_close) for x in vgk_close]

vpl_open_norm = [x/sum(vpl_open) for x in vpl_open]
vpl_high_norm = [x/sum(vpl_high) for x in vpl_high]
vpl_low_norm = [x/sum(vpl_low) for x in vpl_low]
vpl_close_norm = [x/sum(vpl_close) for x in vpl_close]

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

svxy_open_norm = [x/sum(svxy_open) for x in svxy_open]
svxy_high_norm = [x/sum(svxy_high) for x in svxy_high]
svxy_low_norm = [x/sum(svxy_low) for x in svxy_low]
svxy_close_norm = [x/sum(svxy_close) for x in svxy_close]

uvxy_open_norm = [x/sum(uvxy_open) for x in uvxy_open]
uvxy_high_norm = [x/sum(uvxy_high) for x in uvxy_high]
uvxy_low_norm = [x/sum(uvxy_low) for x in uvxy_low]
uvxy_close_norm = [x/sum(uvxy_close) for x in uvxy_close]

# Normalizing all Forex  values
eur_open_norm = [x/sum(eur_open) for x in eur_open]
eur_high_norm = [x/sum(eur_high) for x in eur_high]
eur_low_norm = [x/sum(eur_low) for x in eur_low]
eur_close_norm = [x/sum(eur_close) for x in eur_close]

mxn_open_norm = [x/sum(mxn_open) for x in mxn_open]
mxn_high_norm = [x/sum(mxn_high) for x in mxn_high]
mxn_low_norm = [x/sum(mxn_low) for x in mxn_low]
mxn_close_norm = [x/sum(mxn_close) for x in mxn_close]

cad_open_norm = [x/sum(cad_open) for x in cad_open]
cad_high_norm = [x/sum(cad_high) for x in cad_high]
cad_low_norm = [x/sum(cad_low) for x in cad_low]
cad_close_norm = [x/sum(cad_close) for x in cad_close]

cnh_open_norm = [x/sum(cnh_open) for x in cnh_open]
cnh_high_norm = [x/sum(cnh_high) for x in cnh_high]
cnh_low_norm = [x/sum(cnh_low) for x in cnh_low]
cnh_close_norm = [x/sum(cnh_close) for x in cnh_close]

gbp_open_norm = [x/sum(gbp_open) for x in gbp_open]
gbp_high_norm = [x/sum(gbp_high) for x in gbp_high]
gbp_low_norm = [x/sum(gbp_low) for x in gbp_low]
gbp_close_norm = [x/sum(gbp_close) for x in gbp_close]
########################################################
#Correlations
#VIX & TVIX
print(np.corrcoef(tvix_close, vix_close))
vix_tvix_corr = np.corrcoef(tvix_close, vix_close)[0][1]
#VIX & ZIV
vix_ziv_corr = np.corrcoef(ziv_close, vix_close)[0][1]
#VIX & SVXY
vix_svxy_corr = np.corrcoef(svxy_close, vix_close)[0][1]
#VIX & UVXY
vix_uvxy_corr = np.corrcoef(uvxy_close, vix_close)[0][1]

#VIX & VEA
vix_vea_corr = np.corrcoef(vea_close, vix_close)[0][1]
#VIX & INX
vix_inx_corr = np.corrcoef(inx_close, vix_close)[0][1]
#VIX & Vgk
vix_vgk_corr = np.corrcoef(vgk_close, vix_close)[0][1]
#VIX & VPL
vix_vpl_corr = np.corrcoef(vpl_close, vix_close)[0][1]
#VIX & VWO
vix_vwo_corr = np.corrcoef(vwo_close, vix_close)[0][1]


print(len(eur_close))
print(len(mxn_close))
print(len(cad_close))
print(len(cnh_close))
print(len(gbp_close))
print('_______________')
print(len(vix_close))
print('____________')

for date in vix_date:
    if not date in eur_date:
        print('euro date')
        print(date)
        print('________')
    if not date in mxn_date:
        print('mxn date')
        print(date)
        print('________')
    if not date in cad_date:
        print('cad date')
        print(date)
        print('________')
    if not date in cnh_date:
        print('cnh date')
        print(date)
        print('________')
    if not date in gbp_date:
        print('gbp date')
        print(date)
        print('________')
    if not date in eur_date:
        print('euro date')
        print(date)
        print('________')

#VIX & EUR        
vix_eur_corr = np.corrcoef(eur_close, vix_close)[0][1]
#VIX & MXN
vix_mxn_corr = np.corrcoef(mxn_close, vix_close)[0][1]
#VIX & CAD
vix_cad_corr = np.corrcoef(cad_close, vix_close)[0][1]
#VIX & CNH
vix_cnh_corr = np.corrcoef(cnh_close, vix_close)[0][1]
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
plt.plot(svxy_date, svxy_close_norm, 'm', label = 'SVXY '+ str(vix_svxy_corr))
plt.plot(uvxy_date, uvxy_close_norm, 'g', label = 'UVXY '+ str(vix_uvxy_corr))
plt.legend()

plt.figure(2)
plt.title('Forex')
plt.plot(vix_date, vix_close_norm, 'k', label = 'VIX ')
plt.plot(gbp_date, gbp_close_norm, 'm', label = 'GBP '+ str(vix_gbp_corr))
plt.plot(eur_date, eur_close_norm, 'g', label = 'EUR '+ str(vix_eur_corr))
plt.plot(mxn_date, mxn_close_norm, 'b', label = 'MXN '+ str(vix_mxn_corr))
plt.plot(cad_date, cad_close_norm, 'r', label = 'CAD '+ str(vix_cad_corr))
plt.plot(cnh_date, cnh_close_norm, 'y', label = 'CNH '+ str(vix_cnh_corr))
plt.legend()


plt.figure(3)
plt.title('Indeces & Global ETFs')
plt.plot(vix_date, vix_close_norm, 'k', label = 'VIX ')
plt.plot(vea_date, vea_close_norm, 'm', label = 'VEA-World '+ str(vix_vea_corr))
plt.plot(inx_date, inx_close_norm, 'g', label = 'S&P500 USA '+ str(vix_inx_corr))
plt.plot(vgk_date, vgk_close_norm, 'b', label = 'VGK Europe '+ str(vix_vgk_corr))
plt.plot(vpl_date, vpl_close_norm, 'r', label = 'VPL Asia '+ str(vix_vpl_corr))
plt.plot(vwo_date, vwo_close_norm, 'y', label = 'VWO Emerging Markets '+ str(vix_vwo_corr))
plt.legend()
plt.show()

########################################################################
code.interact(local=locals())
