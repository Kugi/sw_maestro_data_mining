#coding:utf-8
__author__ = 'jeongmingi'


from sklearn.externals import joblib
import pandas as pd
filename = "data/age_my_model_80.pkl"
filename2 = "data/my_model_10000"

gender_clf = joblib.load(filename2)
age_clf = joblib.load(filename)

import numpy as np
import pickle
uapp = pickle.load(file('data/user_app.df'))
EF_table = pickle.load(file('data/age_feature.pkl'))
uapp_ = uapp[['user_id', 'entity_id', 'usage']]
user_id_ = uapp_['user_id'].unique()

def what_ages(i):
    #c = 0
    #print i
    user_ = uapp_.ix[(uapp_['user_id'] == i)]
    #user_ = uapp_[uapp_.apply(lambda x: x['user_id'] == i, axis=1)]
    ########## pickle 'entityid_featureid' uesed for translating...##########
    #####
    X_test = (0 , list(user_.entity_id))
    temp = []
    #print X_test[1]
    rev_table = {}
    for ii in X_test[1]:
        c_i = str(ii)
        if(EF_table.has_key(c_i) == True):
            ef = EF_table[c_i]
            temp.append(ef)
            rev_table[str(ef)] = ii
        else:
            pass
            #print(i ,False)
            #print temp
        ##########################################################################
    ########## vectorization... It will have 49,683 features and not have
    ########## weight... ㅎㅎㅎ
    ########## 그러나 0~1의 가중치를 줄 수 있지 안을까?
    n_features = 49683 ##!!!!!!
    temp2 = np.zeros(n_features, dtype = np.float64)
    for ii in range(n_features):
        if((ii+1) in temp):
            t = rev_table[str(ii+1)]
            #print t
            t = int(user_[user_['entity_id']==t].usage)
            tt = t+1

            temp2[ii] += tt
            #c += 1
            #print tt
        else:
            temp2[ii] = 0
    X_test = np.array([temp2])
    ages = age_clf.predict(X_test)
    #print int(gender)
    #X_test = np.array([0, temp])
    #print c
    return i, int(ages)

def what_gender(i):
    user_ = uapp_.ix[(uapp_['user_id'] == i)]
    #user_ = uapp_[uapp_.apply(lambda x: x['user_id'] == i, axis=1)]
    ########## pickle 'entityid_featureid' uesed for translating...##########
    #####
    X_test = (0 , list(user_.entity_id))
    temp = []
    for ii in X_test[1]:
        c_i = str(ii)
        if(EF_table.has_key(c_i) == True):
            temp.append(EF_table[c_i])
        else:
            pass
            #print(i ,False)
            ##########################################################################
    n_features = 52600
    temp2 = np.zeros(n_features, dtype = np.float64)
    for ii in range(n_features):
        if((ii+1) in temp):
            temp2[ii] = temp2[ii] + 1
        else:
            temp2[ii] = 0
    X_test = np.array([temp2])
    gender = gender_clf.predict(X_test)
    #print int(gender)
    #X_test = np.array([0, temp])
    return i, int(gender)


user = []
gender = []
age = []
user_id__ = user_id_[:20]

for i in user_id__:
    temp1, temp2 = what_gender(i)
    temp3, temp4 = what_ages(i)

    user.append(temp1)
    gender.append(temp2)
    age.append(temp4)
    print i
data = {'user' : user,
        'gender' : gender,
        'age' : age}
userngender = pd.DataFrame(data)
pd.DataFrame.save(userngender, "data/profiled_data.pkl")