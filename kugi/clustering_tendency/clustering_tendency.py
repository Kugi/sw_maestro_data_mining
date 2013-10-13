__author__ = 'kugi'

from pandas import DataFrame, Series
import pandas as pd
import pandas.io.sql as sql
import numpy as np
import matplotlib.pyplot as plt
from IPython.core.display import Image

import numpy as np
import pylab as pl
from matplotlib import finance
from matplotlib.collections import LineCollection


import sys
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import re
import time
import math

import pickle


import pandas as pd
import numpy as np

from sklearn import cluster, covariance, manifold

#def attach

def load(fName):
    ''' load the file using std open'''
    f = open(fName,'r')

    data = []
    for line in f.readlines():
        data.append(line.replace('\n','').split(' '))

    f.close()

    return data


def createPMIDataFrame(appNameList, keywordList):
    pmi_frame = pd.DataFrame(data=0.0, index=appNameList, columns=keywordList)
    return pmi_frame

def setPMI(dstFrame, appName, keyword, pmi):
    dstFrame.loc[appName, keyword] = pmi

def getPMIFromDF(dstFrame, appName, keyword):
    return dstFrame.loc[appName, keyword]

def calcPMI(AppScore, KeywordScore, BothScore, nTotalDocs):
    val = (AppScore*KeywordScore/(BothScore*nTotalDocs+1))
    if val <= 0:
        return 0.0
    return math.log10(val)


class DatabaseManager():

    __BaseObj__ = declarative_base()
    __db__ = create_engine('postgresql://soma:maestro@)!#@soma1.buzzni.com/application')
    __Session__ = sessionmaker(bind=__db__)
    #__s__ = __Session__()

    #__db__.echo = False  # Try changing this to True and see what happens
    #__metadata__ = MetaData(__db__)


    class Cache_query(__BaseObj__):
        __tablename__ = 'query_freq'
        query = Column('query', String(100), primary_key=True)
        num = Column('num', Integer)
        update_date = Column('update_date', Date(),default=datetime.now(), onupdate=datetime.now())
        def __init__(self,query,num):
            self.query=query
            self.num=num

    class Cache_pmi(__BaseObj__):
        __tablename__ = 'app_keyword_pmi'
        app_name = Column('app_name', String(100), primary_key=True)
        keyword = Column('keyword', String(100), primary_key=True)
        pmi = Column('pmi', Float)
        update_date = Column('update_date', Date(),default=datetime.now(), onupdate=datetime.now())
        def __init__(self,app_name,keyword,pmi):
            self.app_name=app_name
            self.keyword=keyword
            self.pmi=pmi

    class Cache_keyword(__BaseObj__):
        __tablename__ = 'keywords'
        keyword = Column('keyword', String(100), primary_key=True)
        def __init__(self, keyword):
            self.keyword = keyword


    @staticmethod
    def get_query_count(query):
        s = DatabaseManager.__Session__()
        result = s.query(DatabaseManager.Cache_query).filter(DatabaseManager.Cache_query.query == query)
        s.close_all()

        if result.count()>0:
            return result[0].num
        return 0


    @staticmethod
    def set_query_count(query, count):
        s = DatabaseManager.__Session__()
        result = s.query(DatabaseManager.Cache_query).filter(DatabaseManager.Cache_query.query == query)

        if result.count()>0:
            result[0].num = count
        else:
            s.add(DatabaseManager.Cache_query(query,count))
        s.commit()
        s.close_all()


    @staticmethod
    def get_keywords():
        s = DatabaseManager.__Session__()
        result = s.query(DatabaseManager.Cache_keyword)
        s.close_all()

        if result.count()>0:
            return map(lambda x: x.keyword, result)
        return 0


    @staticmethod
    def add_keyword(keyword):
        s = DatabaseManager.__Session__()
        result = s.query(DatabaseManager.Cache_keyword).filter(DatabaseManager.Cache_keyword.keyword == keyword)

        if result.count()>0:
            return 0
        else:
            s.add(DatabaseManager.Cache_keyword(keyword))

        s.commit()
        s.close_all()

        return keyword


    @staticmethod
    def get_app_keyword_pmi(app_name, keyword):
        s = DatabaseManager.__Session__()
        result = s.query(DatabaseManager.Cache_pmi). \
            filter(DatabaseManager.Cache_pmi.app_name==app_name). \
            filter(DatabaseManager.Cache_pmi.keyword==keyword)
        s.close_all()

        if result.count()>0:
            return result[0].pmi
        return 0


    @staticmethod
    def set_app_keyword_pmi(app_name, keyword, pmi):
        s = DatabaseManager.__Session__()
        result = s.query(DatabaseManager.Cache_pmi). \
            filter(DatabaseManager.Cache_pmi.app_name==app_name). \
            filter(DatabaseManager.Cache_pmi.keyword==keyword)

        if result.count()>0:
            result[0].pmi = pmi
        else:
            s.add(DatabaseManager.Cache_pmi(app_name, keyword, pmi))
        s.commit()
        s.close_all()






app2 =  pd.read_pickle('/home/kugi/sw_maestro_data_mining/utils/data/app_info2.df')
app2 = app2[np.isfinite(app2['rate_num_all'])]
app2 = app2[np.isfinite(app2['score'])]
app2 = app2.sort(['rate_num_all'], ascending=False)
app2spec = app2[['id', 'genre', 'cate', 'score', 'name', 'price', 'developer', 'company', 'download_num', 'rate_num_all']]
'''

app2_name = app2.loc[:,['name']]
#print app2.head()
app2 = app2.sort(['rate_num_all'], ascending=False)
#print app2[['name', 'rate_num_all']][5:25]
res = app2.ix[app2['rate_num_all']>=5000]
res2 = res[73:1000]#res.ix[res['score']>50]
print 'size:'
print res.shape
res3 = res2['name']
print res3
                      '''

appList = app2spec.ix[app2spec['rate_num_all'] >= 1000000]
appList = appList.ix[appList['score'] >= 90]
print appList
app2test = appList.head()
appNameList = appList['name']
print app2test

#app2test['']


key = load('/home/kugi/sw_maestro_data_mining/utils/data/Keyword.txt')
keywords = [""]
for c in key[0]:
# keywords.append('+"'+c.replace(" ", "")+'"')
    keywords.append(c)

keywordList = keywords[1:]
keywordList[0] = keywordList[0].replace(" ", "")
print ' '.join(keywordList)


# make pmi Data Frame

pmiDataFrame = createPMIDataFrame(appNameList, keywords)

appListLen = len(appNameList)
keywordListLen = len(keywordList)
totalLen = appListLen * keywordListLen
print ("len: %d, %d" % (  appListLen, keywordListLen ) )

idxi=0
for a in appNameList:

    for k in keywordList:
        if a=="" or k=="" :
            continue

        #print a, k
        idxi += 1
        pmi = DatabaseManager.get_app_keyword_pmi('"'+a+'"', '"'+k+'"')
        setPMI(pmiDataFrame, a, k, pmi)
        print ("[%d/%d] setPMI: (%s, %s) = %f" % (idxi, totalLen, a, k, pmi) )


dumpFile = open('/home/kugi/sw_maestro_data_mining/utils/data/dumpedPmiFrame.df','wb')
pickle.dump(pmiDataFrame, dumpFile)
dumpFile.close()


pmiDataFrame2 = pd.read_pickle('/home/kugi/sw_maestro_data_mining/utils/data/dumpedPmiFrame.df')

#print pmiDataFrame.head()

print pmiDataFrame2.head()