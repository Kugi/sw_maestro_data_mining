import pgdb
import pandas
import pickle
import json
from pandas import DataFrame, Series
from sklearn.datasets import load_svmlight_file

# len=330600
prof_user = pickle.load(file("./data/profiled_gender.pkl"))

userlist = list(prof_user['user'])
genlist = list(prof_user['gender'])
#userlist.sort()
prof_user_con = pandas.DataFrame(index=userlist, columns={'gender'})
prof_user_con['gender'] = genlist

# len=10616409
userapp = pickle.load(file("./data/user_app.df"))

app_gender_df = pandas.read_pickle("./data/app_gender.df")

print 'working...'
#gen = prof_user_con.loc[2007318]
#print gen
for idx, ua in userapp.iterrows():
    try:
        gen = prof_user_con.loc[ua['user_id']]
        if gen==1: #female
            app_gender_df.loc[ua['entity_id'], 'woman'] += 1
        elif gen==2: #male
            app_gender_df.loc[ua['entity_id'], 'man'] += 1
    except Exception, e:
        print e
        pass


app_gender_df.to_pickle("./data/app_gender_filled.df")
