__author__ = 'jeongmingi'

import pickle
import pandas as pd

import pylab as pl
import matplotlib
import matplotlib.pyplot as plt
import pandas.tools.plotting
from IPython.core.display import Image


user_gender = pickle.load(file('data/profiled_gender.pkl'))
uapp = pickle.load(file('data/user_app.df'))
user_gender['gender'] = (-1) * user_gender['gender'] + 3

class GenderForApps(object):
    def __init__(self):
        pass

    def get_count_gender(self, app):
        temp = self.mul(5,2) #self recall has no problem...
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

        return male, female, temp

    def graph_gender_rate(self, apps):
        #print apps          #if server witch import *.py print that commits print-command
        temp = []
        index_ = []
        print apps[:]
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


    # ff is dataframe for 'app name' in index, 'male num', 'female num' in colums
    def get_graph_for_count(self, ff):
        matplotlib.rc('font', family='NanumGothicCoding')
        def _stringify(x):
            if isinstance(x, tuple):
                return '|'.join(str(y) for y in x)
            else:
                return unicode(x)
        pandas.tools.plotting._stringify = _stringify # hack
        ff.plot(kind='barh', alpha=0.5)
        plt.savefig('appGender.png', dpi=100)
        plt.show()

    #n_ff is dataframe for 'app name' in index, 'male rate', 'female rate' in colums
    def get_graph_for_rate(self, n_ff):
        matplotlib.rc('font', family='NanumGothicCoding')
        def _stringify(x):
            if isinstance(x, tuple):
                return '|'.join(str(y) for y in x)
            else:
                return unicode(x)
        pandas.tools.plotting._stringify = _stringify # hack

        n_ff.plot(kind='barh', stacked=True, title=''.join(u'gender rate for app'))
        plt.savefig('appGenderRate.png', dpi=100)
        plt.show()


    def mul(self, x, y):
        return x * y