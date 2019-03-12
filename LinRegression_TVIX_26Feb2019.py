import time
import code
from sklearn.linear_model import LinearRegression
import pandas as pd
import seaborn
import requests
import alpha_vantage
import json
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import code


API_URL = "https://www.alphavantage.co/query?"

#Volatility
symbols = ['VIX', 'TVIX']# 'ZIV', 'SVXY', 'UVXY']
vix_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
tvix_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
ziv_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
svxy_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}
uvxy_data = {'date': [], 'open': [], 'high': [], 'low': [], 'close' : []}

vol_list = [vix_data, tvix_data]# ziv_data, svxy_data, uvxy_data]

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
############################################################################
#TVIX Linear Regression
tvix = pd.DataFrame.from_dict(tvix_data)

tvix['S_3'] = tvix['close'].shift(1).rolling(window = 3).mean()
tvix['S_9'] = tvix['close'].shift(1).rolling(window= 9).mean()

tvix['S_2'] = tvix['close'].shift(1).rolling(window=2).mean()
tvix['S_5'] = tvix['close'].shift(1).rolling(window=5).mean()

tvix = tvix.dropna()

X_3_9 = tvix[['S_3', 'S_9']]
X_2_5 = tvix[['S_2', 'S_5']]
X_3_9.head()
X_2_5.head()

y = tvix['close']
y.head()

t = 0.9
t = int(t*len(tvix))

x_train = X_3_9[:t]
x_train2 = X_2_5[:t]
x_train_date = [date.toordinal()  for date in tvix_data['date']][:t]
x_train3 = [[x_train_date, 
y_train = y[:t]

x_test = X_3_9[t:]
x_test2 = X_2_5[t:]
x_test3 = [date.toordinal()  for date in tvix_data['date']][t:]
y_test = y[t:]


linear = LinearRegression().fit(x_train, y_train)
linear2 = LinearRegression().fit(x_train2, y_train)
linear3 = LinearRegression().fit(x_train3, y_train)

predicted_price = linear.predict(x_test)
predicted_price2 = linear.predict(x_test2)
predicted_price3 = linear.predict(x_test3)

predicted_price = pd.DataFrame(predicted_price, index = y_test.index)
predicted_price2 = pd.DataFrame(predicted_price2, index = y_test.index)
predicted_price3 =  pd.DataFrame(predicted_price3, index = y_test.index)

tvix_score = linear.score(X_3_9[t:], y[t:])
tvix_score2 = linear.score(X_2_5[t:], y[t:])
tvix_score3 = linear.score(x_test3, y[t:])

# predicted_price = predicted_price.values.tolist()
# predicted_price = [item for sublist in predicted_price for item in sublist]

# predicted_price2 = predicted_price2.values.tolist()
# predicted_price = [item for sublist in predicted_price2 for item in sublist]

# x_test = x_test.values.tolist()
# y_test = y_test.values.tolist()
# #y_test = [item for sublist in y_test for item in sublist]
# print(y_test)
# print(x_test)



dates = tvix_data['date'][t:][9:]
plot_predicted = predicted_price.values.tolist()
plot_predicted2 = predicted_price2.values.tolist()
plot_predicted3 = predicted_price3.values.tolist()
y_test_plot = y_test.values.tolist()

plt.figure(1)
plt.plot(dates, plot_predicted, label = '3&9 ' + str(tvix_score))
plt.plot(dates, plot_predicted2, label = '2&5' +str(tvix_score2))
plt.plot(dates, plot_predicted3, label = 'Dates' +str(tvix_score3))
plt.plot(dates ,y_test_plot, label = 'Actual')
plt.legend()
plt.show()


# if tvix_score >= tvix_score2:
#     plt.plot(
#     y_test.plot()
#     plt.legend(['predicted_price = ' + str(tvix_score), 'actual_price'])
#     plt.show()
# else:
#     predicted_price2.plot()
#     y_test.plot()
#     plt.legend(['predicted_price2 = ' + str(tvix_score2), 'actual_price'])
#     plt.show()

    
#######################################################################
# vix_start = vix_data['date'][0]
# tvix_start = tvix_data['date'][0]
# ziv_start = ziv_data['date'][0]
# svxy_start = svxy_data['date'][0]
# uvxy_start = uvxy_data['date'][0]

# vix_end = vix_data['date'][-1]
# tvix_end = tvix_data['date'][-1]
# ziv_end = ziv_data['date'][-1]
# svxy_end = svxy_data['date'][-1]
# uvxy_end = uvxy_data['date'][-1]

# start_list = [vix_start, tvix_start, ziv_start, svxy_start, uvxy_start]
# start_list.sort()
# #start_date = start_list[-1]
# start_date = datetime(2018, 9, 18, 0, 0)

# #Finding index of Vol  start date
# vix_index = vix_data['date'].index(start_date)
# tvix_index = tvix_data['date'].index(start_date)
# ziv_index = ziv_data['date'].index(start_date)
# svxy_index = svxy_data['date'].index(start_date)
# uvxy_index = uvxy_data['date'].index(start_date)

# #Setting new start date of data using index of start date
# vix_date = vix_data['date'][vix_index:]
# vix_open = vix_data['open'][vix_index:]
# vix_high = vix_data['high'][vix_index:]
# vix_low = vix_data['low'][vix_index:]
# vix_close = vix_data['close'][vix_index:]

# tvix_date = tvix_data['date'][tvix_index:]
# tvix_open = tvix_data['open'][tvix_index:]
# tvix_high = tvix_data['high'][tvix_index:]
# tvix_low = tvix_data['low'][tvix_index:]
# tvix_close = tvix_data['close'][tvix_index:]

# ziv_date = ziv_data['date'][ziv_index:]
# ziv_open = ziv_data['open'][ziv_index:]
# ziv_high = ziv_data['high'][ziv_index:]
# ziv_low = ziv_data['low'][ziv_index:]
# ziv_close = ziv_data['close'][ziv_index:]

# svxy_date = svxy_data['date'][svxy_index:]
# svxy_open = svxy_data['open'][svxy_index:]
# svxy_high = svxy_data['high'][svxy_index:]
# svxy_low = svxy_data['low'][svxy_index:]
# svxy_close = svxy_data['close'][svxy_index:]

# uvxy_date = uvxy_data['date'][uvxy_index:]
# uvxy_open = uvxy_data['open'][uvxy_index:]
# uvxy_high = uvxy_data['high'][uvxy_index:]
# uvxy_low = uvxy_data['low'][uvxy_index:]
# uvxy_close = uvxy_data['close'][uvxy_index:]

    
# # Normalizing all volatility values
# vix_open_norm = [x/sum(vix_open) for x in vix_open]
# vix_high_norm = [x/sum(vix_high) for x in vix_high]
# vix_low_norm = [x/sum(vix_low) for x in vix_low]
# vix_close_norm = [x/sum(vix_close) for x in vix_close]

# tvix_open_norm = [x/sum(tvix_open) for x in tvix_open]
# tvix_high_norm = [x/sum(tvix_high) for x in tvix_high]
# tvix_low_norm = [x/sum(tvix_low) for x in tvix_low]
# tvix_close_norm = [x/sum(tvix_close) for x in tvix_close]

# ziv_open_norm = [x/sum(ziv_open) for x in ziv_open]
# ziv_high_norm = [x/sum(ziv_high) for x in ziv_high]
# ziv_low_norm = [x/sum(ziv_low) for x in ziv_low]
# ziv_close_norm = [x/sum(ziv_close) for x in ziv_close]

# svxy_open_norm = [x/sum(svxy_open) for x in svxy_open]
# svxy_high_norm = [x/sum(svxy_high) for x in svxy_high]
# svxy_low_norm = [x/sum(svxy_low) for x in svxy_low]
# svxy_close_norm = [x/sum(svxy_close) for x in svxy_close]

# uvxy_open_norm = [x/sum(uvxy_open) for x in uvxy_open]
# uvxy_high_norm = [x/sum(uvxy_high) for x in uvxy_high]
# uvxy_low_norm = [x/sum(uvxy_low) for x in uvxy_low]
# uvxy_close_norm = [x/sum(uvxy_close) for x in uvxy_close]
# #Correlations
# #VIX & TVIX
# print(np.corrcoef(tvix_close, vix_close))
# vix_tvix_corr = np.corrcoef(tvix_close, vix_close)[0][1]
# #VIX & ZIV
# vix_ziv_corr = np.corrcoef(ziv_close, vix_close)[0][1]
# #VIX & SVXY
# vix_svxy_corr = np.corrcoef(svxy_close, vix_close)[0][1]
# #VIX & UVXY
# vix_uvxy_corr = np.corrcoef(uvxy_close, vix_close)[0][1]



 
################################################################################################################
#Graphs

# plt.figure(1)
# plt.title('Volatility')
# plt.plot(vix_date, vix_close_norm, 'k', label = 'VIX ')
# plt.plot(tvix_date, tvix_close_norm, 'r', label = 'TVIX '+ str(vix_tvix_corr))
# plt.plot(ziv_date, ziv_close_norm, 'b', label = 'ZIV '+ str(vix_ziv_corr))
# plt.plot(svxy_date, svxy_close_norm, 'm', label = 'SVXY '+ str(vix_svxy_corr))
# plt.plot(uvxy_date, uvxy_close_norm, 'g', label = 'UVXY '+ str(vix_uvxy_corr))
# plt.legend()
# plt.show()

########################################################################
code.interact(local=locals())
