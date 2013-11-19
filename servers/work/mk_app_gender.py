import pgdb
import pandas
import pickle
import json
from pandas import DataFrame, Series
from sklearn.datasets import load_svmlight_file

# len=330600
prof_user = pickle.load(file("./data/profiled_gender.pkl"))

# len=10616409
userapp = pickle.load(file("./data/user_app.df"))

# len=277774
appinfo2 = pickle.load(file("./data/app_info2.df"))


dfcols = {'appid', 'appname', 'man', 'woman'}
dfidxs = list(appinfo2['id'])
dfidxs.sort()

app_gender_df = pandas.DataFrame(index=dfidxs, columns=dfcols)
app_gender_df.loc[:,:] = 0
app_gender_df['appid'] = dfidxs

#print app_gender_df.loc[676983][1]
print 'working...'
for idx, app in appinfo2.iterrows():
    app_gender_df.loc[app['id'],'appname'] = app['name']


app_gender_df.to_pickle("./data/app_gender.df")
