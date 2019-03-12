import csv
import pandas
import scipy
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt
import datetime
from sklearn import preprocessing
import statistics as stat

#############################################################################
#Read and Organize Data
############################################################################
#VIX
with open('Volatility_Data/VIX_30Nov2010.csv', 'rb') as VIX_csv:
    VIX_reader = csv.reader(VIX_csv, delimiter = ',')

    vix_data = {}
    vix_data['date'] = []
    vix_data['open'] = []
    vix_data['high'] = []
    vix_data['low'] = []
    vix_data['close'] = []
        
    for row in VIX_reader:
        vix_data['date'].append(row[0])
        try:
            vix_data['open'].append(float(row[1]))
            vix_data['high'].append(float(row[2]))
            vix_data['low'].append(float(row[3]))
            vix_data['close'].append(float(row[4]))
        except ValueError:
            pass

#TVIX
with open('Volatility_Data/TVIX_30Nov2010.csv', 'rb') as TVIX_csv:
    TVIX_reader = csv.reader(TVIX_csv, delimiter = ',')

    tvix_data = {}
    tvix_data['date'] = []
    tvix_data['open'] = []
    tvix_data['high'] = []
    tvix_data['low'] = []
    tvix_data['close'] = []
    tvix_data['volume'] = []

    for row in TVIX_reader:
        tvix_data['date'].append(row[0])
        try:
            tvix_data['open'].append(float(row[1]))
            tvix_data['high'].append(float(row[2]))
            tvix_data['low'].append(float(row[3]))
            tvix_data['close'].append(float(row[4]))
            tvix_data['volume'].append(float(row[6]))
        except ValueError:
            pass
#ZIV
with open('Volatility_Data/ZIV_30Nov2010.csv', 'rb') as ZIV_csv:
    ZIV_reader = csv.reader(ZIV_csv, delimiter = ',')

    ziv_data = {}
    ziv_data['date'] = []
    ziv_data['open'] = []
    ziv_data['high'] = []
    ziv_data['low'] = []
    ziv_data['close'] = []
        
    for row in ZIV_reader:
        ziv_data['date'].append(row[0])
        try:
            ziv_data['open'].append(float(row[1]))
            ziv_data['high'].append(float(row[2]))
            ziv_data['low'].append(float(row[3]))
            ziv_data['close'].append(float(row[4]))
        except ValueError:
            pass


#SVXY
with open('Volatility_Data/SVXY_4Oct2011.csv', 'rb') as SVXY_csv:
    SVXY_reader = csv.reader(SVXY_csv, delimiter = ',')

    svxy_data = {}
    svxy_data['date'] = []
    svxy_data['open'] = []
    svxy_data['high'] = []
    svxy_data['low'] = []
    svxy_data['close'] = []
        
    for row in SVXY_reader:
        svxy_data['date'].append(row[0])
        try:
            svxy_data['open'].append(float(row[1]))
            svxy_data['high'].append(float(row[2]))
            svxy_data['low'].append(float(row[3]))
            svxy_data['close'].append(float(row[4]))
        except ValueError:
            pass

#UVXY
with open('Volatility_Data/UVXY_04Oct2011.csv', 'rb') as UVXY_csv:
    UVXY_reader = csv.reader(UVXY_csv, delimiter = ',')

    uvxy_data = {}
    uvxy_data['date'] = []
    uvxy_data['open'] = []
    uvxy_data['high'] = []
    uvxy_data['low'] = []
    uvxy_data['close'] = []
        
    for row in UVXY_reader:
        uvxy_data['date'].append(row[0])
        try:
            uvxy_data['open'].append(float(row[1]))
            uvxy_data['high'].append(float(row[2]))
            uvxy_data['low'].append(float(row[3]))
            uvxy_data['close'].append(float(row[4]))
        except ValueError:
            pass

#VXXB
with open('Volatility_Data/VXXB_25Jan2018.csv', 'rb') as VXXB_csv:
    VXXB_reader = csv.reader(VXXB_csv, delimiter = ',')

    vxxb_data = {}
    vxxb_data['date'] = []
    vxxb_data['open'] = []
    vxxb_data['high'] = []
    vxxb_data['low'] = []
    vxxb_data['close'] = []
        
    for row in VXXB_reader:
        vxxb_data['date'].append(row[0])
        try:
            vxxb_data['open'].append(float(row[1]))
            vxxb_data['high'].append(float(row[2]))
            vxxb_data['low'].append(float(row[3]))
            vxxb_data['close'].append(float(row[4]))
        except ValueError:
            pass

#Popping off header "date" from csv file data so the data only incules dates
vix_data['date'].pop(0)
tvix_data['date'].pop(0)
ziv_data['date'].pop(0)
svxy_data['date'].pop(0)
uvxy_data['date'].pop(0)
vxxb_data['date'].pop(0)
     
############################################################################
#Converting all date data to date_time objects

def date_maker (list_str_dates):
    date_objects = []
    for date in list_str_dates:
        if '/' in date:
            date_list = date.split('/')
            date_obj = datetime.date(int(date_list[2]),int(date_list[0]),int(date_list[1]))
        elif '-' in date:
            date_list = date.split('-')
            date_obj = datetime.date(int(date_list[0]),int(date_list[1]),int(date_list[2]))
        else:
            print('Other delimiter in dates')
            break     
        date_objects.append(date_obj)
    return date_objects

#print('TVIX')
#print(tvix_data['date'][0:5])
#print('ZIV')
#print(ziv_data['date'][0:5])
#print('SVXY')
#print(svxy_data['date'][0:5])
#print('UVXY')
#print(uvxy_data['date'][0:5])
#print('VXXB')
#print(vxxb_data['date'][0:5])

vix_data['date'] = date_maker(vix_data['date'])
tvix_data['date'] = date_maker(tvix_data['date'])
ziv_data['date'] = date_maker(ziv_data['date'])
svxy_data['date'] = date_maker(svxy_data['date'])
uvxy_data['date'] = date_maker(uvxy_data['date'])
vxxb_data['date'] = date_maker(vxxb_data['date'])

#Finding index for the most recent split date in data for every symbol (eg. VIX, TVIX, SVXY etc.)
#Latest split was 18 Sept 2018 when SVXY and UVXY
#Making this start point of all data or all symbols to not have to adjust for splits
      
splindex_vix = vix_data['date'].index(datetime.date(2018, 9, 18))
splindex_tvix = tvix_data['date'].index(datetime.date(2018 ,9, 18))
splindex_ziv = ziv_data['date'].index(datetime.date(2018, 9, 18))
splindex_svxy = svxy_data['date'].index(datetime.date(2018, 9, 18))
splindex_uvxy = uvxy_data['date'].index(datetime.date(2018, 9, 18))
splindex_vxxb = vxxb_data['date'].index(datetime.date(2018, 9, 18))

#Shortening list to date of last split 18 Sept 2018
def list_short(data_dict, splindex):
    date_list = data_dict['date'][splindex:]
    open_list = data_dict['open'][splindex:]
    close_list = data_dict['close'][splindex:]
    high_list = data_dict['high'][splindex:]
    low_list = data_dict['low'][splindex:]
    return [date_list, open_list, close_list, high_list, low_list]

#VIX
vix_date = list_short(vix_data, splindex_vix)[0]
vix_open = list_short(vix_data, splindex_vix)[1]
vix_close = list_short(vix_data, splindex_vix)[2]
vix_high = list_short(vix_data, splindex_vix)[3]
vix_low = list_short(vix_data, splindex_vix)[4]
#TVIX
tvix_date = list_short(tvix_data, splindex_tvix)[0]
tvix_open = list_short(tvix_data, splindex_tvix)[1]
tvix_close = list_short(tvix_data, splindex_tvix)[2]
tvix_high = list_short(tvix_data, splindex_tvix)[3]
tvix_low = list_short(tvix_data, splindex_tvix)[4]
#ZIV
ziv_date = list_short(ziv_data, splindex_ziv)[0]
ziv_open = list_short(ziv_data, splindex_ziv)[1]
ziv_close = list_short(ziv_data, splindex_ziv)[2]
ziv_high = list_short(ziv_data, splindex_ziv)[3]
ziv_low = list_short(ziv_data, splindex_ziv)[4]
#SVXY
svxy_date = list_short(svxy_data, splindex_svxy)[0]
svxy_open = list_short(svxy_data, splindex_svxy)[1]
svxy_close = list_short(svxy_data, splindex_svxy)[2]
svxy_high = list_short(svxy_data, splindex_svxy)[3]
svxy_low = list_short(svxy_data, splindex_svxy)[4]
#UVXY
uvxy_date = list_short(uvxy_data, splindex_uvxy)[0]
uvxy_open = list_short(uvxy_data, splindex_uvxy)[1]
uvxy_close = list_short(uvxy_data, splindex_uvxy)[2]
uvxy_high = list_short(uvxy_data, splindex_uvxy)[3]
uvxy_low = list_short(uvxy_data, splindex_uvxy)[4]
#VXXB
vxxb_date = list_short(vxxb_data, splindex_vxxb)[0]
vxxb_open = list_short(vxxb_data, splindex_vxxb)[1]
vxxb_close = list_short(vxxb_data, splindex_vxxb)[2]
vxxb_high = list_short(vxxb_data, splindex_vxxb)[3]
vxxb_low = list_short(vxxb_data, splindex_vxxb)[4]

#Normalizing all values for simpler comparison
#VIX
vix_open_norm = [x/sum(vix_open) for x in vix_open]
vix_close_norm = [x/sum(vix_close) for x in vix_close]
vix_high_norm = [x/sum(vix_high) for x in vix_high]
vix_low_norm = [x/sum(vix_low) for x in vix_low]
#TVIX
tvix_open_norm = [x/sum(tvix_open) for x in tvix_open]
tvix_close_norm = [x/sum(tvix_close) for x in tvix_close]
tvix_high_norm = [x/sum(tvix_high) for x in tvix_high]
tvix_low_norm = [x/sum(tvix_low) for x in tvix_low]
#ZIV
ziv_open_norm = [x/sum(ziv_open) for x in ziv_open]
ziv_close_norm = [x/sum(ziv_close) for x in ziv_close]
ziv_high_norm = [x/sum(ziv_high) for x in ziv_high]
ziv_low_norm = [x/sum(ziv_low) for x in ziv_low]
#SVXY
svxy_open_norm = [x/sum(svxy_open) for x in svxy_open]
svxy_close_norm = [x/sum(svxy_close) for x in svxy_close]
svxy_high_norm = [x/sum(svxy_high) for x in svxy_high]
svxy_low_norm = [x/sum(svxy_low) for x in svxy_low]
#UVXY
uvxy_open_norm = [x/sum(uvxy_open) for x in uvxy_open]
uvxy_close_norm = [x/sum(uvxy_close) for x in uvxy_close]
uvxy_high_norm = [x/sum(uvxy_high) for x in uvxy_high]
uvxy_low_norm = [x/sum(uvxy_low) for x in uvxy_low]
#VXXB
vxxb_open_norm = [x/sum(vxxb_open) for x in vxxb_open]
vxxb_close_norm = [x/sum(vxxb_close) for x in vxxb_close]
vxxb_high_norm = [x/sum(vxxb_high) for x in vxxb_high]
vxxb_low_norm = [x/sum(vxxb_low) for x in vxxb_low]

##############################################################################3
#Statistical Analysis
#VIX
mean_vix_close = stat.mean(vix_close)
median_vix_close = stat.median(vix_close)
stdev_vix_close = stat.pstdev(vix_close)
var_vix_close = stat.pvariance(vix_close)
#TVIX
mean_tvix_close = stat.mean(tvix_close)
median_tvix_close = stat.median(tvix_close)
stdev_tvix_close = stat.pstdev(tvix_close)
var_tvix_close = stat.pvariance(tvix_close)
#ZIV
mean_ziv_close = stat.mean(ziv_close)
median_ziv_close = stat.median(ziv_close)
stdev_ziv_close = stat.pstdev(ziv_close)
var_ziv_close = stat.pvariance(ziv_close)
#SVXY
mean_svxy_close = stat.mean(svxy_close)
median_svxy_close = stat.median(svxy_close)
stdev_svxy_close = stat.pstdev(svxy_close)
var_svxy_close = stat.pvariance(svxy_close)
#UVXY
mean_uvxy_close = stat.mean(uvxy_close)
median_uvxy_close = stat.median(uvxy_close)
stdev_uvxy_close = stat.pstdev(uvxy_close)
var_uvxy_close = stat.pvariance(uvxy_close)
#VXXB
mean_vxxb_close = stat.mean(vxxb_close)
median_vxxb_close = stat.median(vxxb_close)
stdev_vxxb_close = stat.pstdev(vxxb_close)
var_vxxb_close = stat.pvariance(vxxb_close)


ziv_close = ziv_close[0:89]
svxy_close = svxy_close[0:89]
uvxy_close = uvxy_close[0:89]
vxxb_close = vxxb_close[0:89]

#Correlations
#VIX & TVIX
vix_tvix_corr = np.corrcoef(tvix_close, vix_close)[0][1]
#VIX & ZIV
vix_ziv_corr = np.corrcoef(ziv_close, vix_close)[0][1]
#VIX & SVXY
vix_svxy_corr = np.corrcoef(svxy_close, vix_close)[0][1]
#VIX & UVXY
vix_uvxy_corr = np.corrcoef(uvxy_close, vix_close)[0][1]
#VIX & VXXB
vix_vxxb_corr = np.corrcoef(vxxb_close, vix_close)[0][1]

#Best Fit Polynomial

variable_day = np.arange(1.0, float(len(vix_close)+1), 1)

i = 2
best_corr = 0.0
while i < 100:
    coeffs = poly.polyfit(variable_day, vix_close, i)
    fit = poly.polyval(variable_day, coeffs)
    corr = np.corrcoef(vix_close, fit)[0][1]
    if corr > best_corr:
        best_corr = corr
        best_deg = i
    i+=1
    

vix_coeffs = poly.polyfit(variable_day, vix_close, best_deg)

tvix_coeffs = poly.polyfit(variable_day,tvix_close, 9)
ziv_coeffs = poly.polyfit(variable_day, ziv_close, 9)
svxy_coeffs = poly.polyfit(variable_day, svxy_close, 9)
uvxy_coeffs = poly.polyfit(variable_day, uvxy_close, 9)
vxxb_coeffs = poly.polyfit(variable_day, vxxb_close, 9)

vix_fit = poly.polyval(variable_day, vix_coeffs)

variable_day_long = (1, 100,1)
vix_fit_long = poly.polyval(variable_day_long, vix_coeffs)

print(vix_date[-1])
print(tvix_date[-1])
print(ziv_date[-1])
print(svxy_date[-1])
print(uvxy_date[-1])
print(vxxb_date[-1])



###################################################################################
#Graphs

plt.figure(1)
plt.title('VIX')
plt.hlines(mean_vix_close - stdev_vix_close, vix_date[0], vix_date[-1], 'r', label = 'Mean -1 sigma')
plt.hlines(mean_vix_close + stdev_vix_close, vix_date[0], vix_date[-1], 'r', label = 'Mean +1 sigma')
plt.hlines(mean_vix_close, vix_date[0], vix_date[-1], 'b', label = 'Mean')
plt.plot(vix_date, vix_close,'k', label = 'VIX_Close')
plt.plot(vix_date, vix_fit, 'g', label = 'VIX_Fit'+'   '+'Deg = '+str(best_deg))
plt.legend(loc = 'upper left')

#plt.figure(2)
#plt.plot(variable_day_long, vix_fit_long)

plt.figure(2)
plt.title('TVIX')
plt.hlines(mean_tvix_close - stdev_tvix_close, tvix_date[0], tvix_date[-1], 'r', label = 'Mean -1 sigma')
plt.hlines(mean_tvix_close + stdev_tvix_close, tvix_date[0], tvix_date[-1], 'r', label = 'Mean +1 sigma')
plt.hlines(mean_tvix_close,tvix_date[0], tvix_date[-1], 'b', label = 'Mean')
plt.plot(tvix_date,tvix_close,'k', label = 'TVIX Close')
plt.legend(loc = 'upper left')

plt.figure(3)
plt.plot(vix_date, vix_close_norm, 'k', label = 'VIX Normalized')
plt.plot(tvix_date, tvix_close_norm, 'b',label = 'TVIX Normalized'+'      ' + 'Correlation = ' +str(vix_tvix_corr))
plt.plot(ziv_date, ziv_close_norm, 'g', label = 'ZIV Normalized'+'      ' + 'Correlation = ' +str(vix_ziv_corr))
plt.plot(svxy_date, svxy_close_norm, 'r',label = 'SVXY Normalized'+'      ' + 'Correlation = ' +str(vix_svxy_corr))
plt.plot(uvxy_date, uvxy_close_norm, 'c', label = 'UVXY Normalized'+'      ' + 'Correlation = ' +str(vix_uvxy_corr))
plt.plot(vxxb_date, vxxb_close_norm, 'm',label = 'VXXB Normalized'+'      ' + 'Correlation = ' +str(vix_vxxb_corr))
plt.legend(loc = 'upper left')

plt.show()

