__author__ = 'jeongmingi'

import pickle
from datetime import date

import pandas as pd


apps = pickle.load(file('data/app_info2.df'))
uapp = pickle.load(file('data/user_app.df'))

def weekDay(i):
    #print i
    year = i/10000
    month = i%10000/100
    day = i%100
    weekday = date(year, month, day).weekday()
    #print "year:%d month:%d day:%d weekday:%d"%(year, month, day, weekday)
    return weekday

def addWeekday0(id_, date, cnt):
    result = []
    for a, b in zip(date, cnt):
        temp = {'id': id_, 'date': a, 'weekday':weekDay(a), 'count': b}
        result.append(temp)
    return result

uni_id = uapp['entity_id'].unique()

group_ = pd.DataFrame()
dic_ = []

for id_ in uni_id[:2000]:
    print id_
    app = uapp.ix[uapp['entity_id']==id_]
    apps.ix[apps['id']==id_].name
    app['create_date'] = app['create_date']//1000000
    app['update_date'] = app['update_date']//1000000
    keys = app['create_date'].unique()
    b = app.groupby('create_date')

    data1 = []
    for name, group in b:
        name = int(name)
        temp = {'date' : name, 'cnt' : int(len(group))}
        data1.append(temp)
    pd_data1 = pd.DataFrame(data1)
    a = pd_data1.date.values
    b = pd_data1.cnt.values

    group = addWeekday0(id_, a, b)
    temp = pd.DataFrame(group)
    temp_weekday = temp.groupby('weekday')
    cnt_group_weekday = temp_weekday['count'].sum()
    temp['totweek_app'] = 0
    #temp['weekday'] == 2 = False처럼 값을 갖지않는 경우 에러 생긴다.
    for i in temp['weekday'].unique():
        temp.ix[temp['weekday']==i, 'totweek_app'] = int(cnt_group_weekday[i])
    if(group_.empty):
        group_ = temp
    else:
        group_ = pd.concat([group_,temp], ignore_index=True)

from sklearn.tree import DecisionTreeRegressor
# Instantiate the model, fit the results, and scatter in vs. out

yalru1 = DecisionTreeRegressor()
yalru1.fit(X, y)