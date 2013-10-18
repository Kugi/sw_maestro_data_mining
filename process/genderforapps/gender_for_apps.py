__author__ = 'jeongmingi'

import pickle
import pandas as pd


uapp = pickle.load(file('data/user_app.df'))
apps = pickle.load(file('data/app_info2.df'))
user_gender = pickle.load(file('data/profiled_gender.pkl'))
user_gender['gender'] = (-1) * user_gender['gender'] + 3

class GenderForApps(object):
    def __init__(self):
        pass

    def get_count_gender(self, app):
        #temp = self.mul(5,2) #self recall has no problem...
        male = 0.0
        female = 0.0
        users = uapp[uapp['entity_id']==app].user_id
        if(users.count>=3000):
            users = users[:3000]

        for user in users:
            gender = user_gender[user_gender['user']==user]['gender']
            if gender:
                if gender == 1:
                    male += 1
                elif gender == 2:
                    female += 1
                else:
                    print "ERROR IN 'get_graph_gender()'"
            else:
                print 'NAN'
        temp = apps.ix[apps['id']==app,'name']
        name = temp.values[0]

        return name, male, female

    def graph_gender_rate(self, apps):
        #print apps          #if server witch import *.py print that commits print-command
        temp = []
        index_ = []
        #print apps[:]
        for i in apps: # can be update....
            male, female = self.get_count_gender(i['id'])
            temp.append([male, female])
            t = apps['name']
            t = t.values
            t = ''.join(t)
            index_.append(t)
        frame = pd.DataFrame(temp, columns = ['male', 'female'],
                             index = index_)
        normed_ = frame.div(frame.sum(axis=1), axis=0)

        #grouped = app_info['name'].groupby(['male', 'female'])
        #app_info[app_info['id'] == app
        return frame, normed_

    def mul(self, x, y):
        return x * y