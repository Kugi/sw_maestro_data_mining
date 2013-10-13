#coding:utf-8
import pickle
import pandas as pd

__author__ = 'jeongmingi'

def get_count_gender(app):
    uapp = pickle.load(file('data/user_app.df'))
    apps = pickle.load(file('data/app_info2.df'))
    user_gender = pickle.load(file('data/profiled_gender.pkl'))
    user_gender['gender'] = (-1) * user_gender['gender'] + 3

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
    return male;

print get_count_gender(1525767)