import pickle
from datetime import date

import pandas as pd


uapp = pickle.load(file('data/user_app.df'))
apps = pickle.load(file('data/app_info2.df'))
user_gender = pickle.load(file('data/profiled_gender.pkl'))
user_gender['gender'] = (-1) * user_gender['gender'] + 3


class AppResource:

    def weekDay(self, i):
        year = i/10000
        month = i%10000/100
        day = i%100
        weekday = date(year, month, day).weekday()
            #print "year:%d month:%d day:%d weekday:%d"%(year, month, day, weekday)
        return weekday

    def addWeekday(self, id_, date, cnt):
        result = []
        for a, b in zip(date, cnt):
            temp = {'id': id_, 'date': a, 'weekday':self.weekDay(a), 'count': b}
            result.append(temp)
        return result

    def date_app(self, id_):
        app = uapp.ix[uapp['entity_id']==id_]

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

        group = self.addWeekday(id_, a, b)
        group_ = pd.DataFrame(group)
        group_weekday = group_.groupby('weekday')
        cnt_group_weekday = group_weekday['count'].sum()
        cnt_weekday = {}
        cnt_weekday['mon'] = int(cnt_group_weekday[0])
        cnt_weekday['tue'] = int(cnt_group_weekday[1])
        cnt_weekday['wed'] = int(cnt_group_weekday[2])
        cnt_weekday['thu'] = int(cnt_group_weekday[3])
        cnt_weekday['fri'] = int(cnt_group_weekday[4])
        cnt_weekday['sat'] = int(cnt_group_weekday[5])
        cnt_weekday['sun'] = int(cnt_group_weekday[6])

        print cnt_weekday

test = AppResource();
#test.id_= 1527791
test.date_app(1527791)