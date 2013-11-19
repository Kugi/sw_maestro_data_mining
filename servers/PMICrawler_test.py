#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'kugi'

from pandas import DataFrame, Series
import pandas as pd
import pandas.io.sql as sql
import pickle
import numpy as np
#import matplotlib.pyplot as plt
from IPython.core.display import Image
import sys

from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import re
import time

import requests
from scrapy.selector import HtmlXPathSelector

import math


# 클래스 중복됨... 모듈이 제대로 만들어질 때 까지는 코드를 가져와서 사용함.
class DatabaseManager():

    __BaseObj__ = declarative_base()
    __db__ = create_engine('postgresql://soma:maestro@)!#@soma3.buzzni.com/application')
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
    # class Cache_pmi(__BaseObj__):
    #     __tablename__ = 'app_keyword_pmi'
    #     app_name = Column('app_name', String(100), primary_key=True)
    #     keyword = Column('keyword', String(100), primary_key=True)
    #     pmi = Column('pmi', Float)
    #     update_date = Column('update_date', Date(),default=datetime.now(), onupdate=datetime.now())
    #     def __init__(self,app_name,keyword,pmi):
    #         self.app_name=app_name
    #         self.keyword=keyword
    #         self.pmi=pmi


    class Cache_pmi_new(__BaseObj__):
        __tablename__ = 'app_keyword_pmi'
        app_name = Column('app_name', String(100), primary_key=True)
        keyword = Column('keyword', String(100), primary_key=True)
        pmi_new = Column('pmi', Float)
        update_date = Column('update_date', Date(),default=datetime.now(), onupdate=datetime.now())
        def __init__(self,app_name,keyword,pmi_new):
            self.app_name=app_name
            self.keyword=keyword
            self.pmi_new=pmi_new

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

    @staticmethod
    def set_app_keyword_pmi_new(app_name, keyword, pmi):
        s = DatabaseManager.__Session__()
        result = s.query(DatabaseManager.Cache_pmi_new). \
            filter(DatabaseManager.Cache_pmi_new.app_name==app_name). \
            filter(DatabaseManager.Cache_pmi_new.keyword==keyword)

        if result.count()>0:
            result[0].pmi_new = pmi
        else:
            s.add(DatabaseManager.Cache_pmi_new(app_name, keyword, pmi))
        s.commit()
        s.close_all()

class PMICrawler(object):

    waitMinute = 0

    def __init__(self, appname, keyword, norms, startIndex=None, endIndex=None):
        PMICrawler.waitMinute = 0
        self.appname = appname
        self.keyword = keyword
        self.norms = norms
        self.both = self.appname + "+" + self.keyword

    @staticmethod
    def __search(q):
        """
        parameter:
            q : String for search.
        """
        try:
            #time.sleep(200)
            q ='+'.join(q.split())
            xpath = """//span[@class='title_num']"""
            html = requests.get("http://cafeblog.search.naver.com/search.naver?where=post&sm=tab_jum&ie=utf8&query="+q).text
            hx = HtmlXPathSelector(text=html)
            items = hx.select(xpath)
            inputstr = (items.extract()[0].split()[3]+"")
            result = int(''.join(re.findall(r'\d+', inputstr)))
            #print result
            return result
        except Exception, e:
            #print "search Exception"
            print e
            if q != '네이버1' and q != '""':
                PMICrawler.__ifError(q)
            #print "except 0"
            return 0



    @staticmethod
    def __ifError(word):
        tempRes = PMICrawler.__search('네이버1')
        if tempRes <= 0:
            print ("tempRes=%d" % tempRes)

            print "stuck at ["+ word + "]"
            while True:
                if PMICrawler.waitMinute <= 0:
                    PMICrawler.waitMinute = 1
                PMICrawler.waitMinute *= 2
                if PMICrawler.waitMinute >= 1440:
                    PMICrawler.waitMinute = 1440
                    #print "escaped. (fail1)"
                    #return 0

                print "sleeping... :  %d" %(PMICrawler.waitMinute*60)
                time.sleep(PMICrawler.waitMinute*60)

                tempRes = PMICrawler.__search('네이버1')
                if tempRes == 0:
                    continue;
                else:
                    try:
                        keyRes1 = PMICrawler.__search(word)
                        DatabaseManager.set_query_count(word, keyRes1)
                        print "escaped. (success, wm=%d)" % PMICrawler.waitMinute
                        PMICrawler.waitMinute = 1
                        return 0
                    except:
                        print "escaped. (fail2)"
                        return 0
                    break
            print "escaped."



    @staticmethod
    def initKeywords(keywords):

        for key in keywords:

            if DatabaseManager.get_query_count('"'+key+'"')==0:
                keyRes = PMICrawler.__search('"'+key+'"')
                DatabaseManager.set_query_count('"'+key+'"', keyRes)

                #sys.stdout.flush()
                #sys.stdout.write('\r')


    def start(self):
    #   try:
    #time.sleep(100)
        # global datadic;
        # appRes = self.__search(self.appname)

        #if ( appRes != 0 ):

        keyRes = DatabaseManager.get_query_count(self.keyword)
        # botRes = self.__search(self.both)

        appRes = DatabaseManager.get_query_count(self.appname)
        botRes = DatabaseManager.get_query_count(self.both)

        print "app 검색 갯수: ", appRes, "key 검색 갯수: ", keyRes, "app & key 검색 갯수: ", botRes
        pmi = self._calcPMI(appRes, keyRes, botRes, 1000000000.0, self.norms)
        print "pmi: ", pmi
        # datadic[self.keyword] = pmi
        DatabaseManager.set_app_keyword_pmi_new(self.appname, self.keyword, pmi)

        #sys.stdout.flush()
        #sys.stdout.write('\r')
        #sys.stdout.write("app=%s(%d), keyword=%s(%d), both=%s(%d), pmi=%.3f\n" % (self.appname, appRes, self.keyword, keyRes, self.both, botRes, pmi) )

        #  except:
        #      __debug__.
        #      print "error: app=%s, keyword=%s\n" % (self.appname, self.keyword)
        #self.__ifError(word)


    def _calcPMI(self, AppScore, KeywordScore, BothScore, nTotalDocs, norms):

		if AppScore <= 0 or KeywordScore <= 0:
			return 0
			
		t = 1000000000.0
		pa = AppScore/t
		pb = KeywordScore/t
		pab = BothScore/t
			#(AppScore*KeywordScore/(BothScore*nTotalDocs))
			
		if pa <= 0 or pb <= 0 or pab <= 0:
			return 0
		val = math.log((pab+norms)/((pa*pb)+norms))

		return val


'''
app2 =  pd.read_pickle('../data/app_info2.df')
app2 = app2[np.isfinite(app2['rate_num_all'])]
app2_name = app2.loc[:,['name']]
#print app2.head()
#app2 = app2.sort(['rate_num_all'], ascending=False)
#print app2[['name', 'rate_num_all']][5:25]
res = app2# app2.ix[app2['rate_num_all']>=5000]
res2 = res#res.ix[res['score']>50]
print 'size:'
print res.shape
res3 = res2['name']
print res3
'''
def load(fname):
    ''' load the file using std open'''
    f = open(fname,'r')

    data = []
    for line in f.readlines():
        data.append(line.replace('\n','').split(','))

    f.close()

    return data


key = load('../data/Keyword.txt')
keywords = []
#keywords2 = [""]
for c in key[0]:
# keywords.append('+"'+c.replace(" ", "")+'"')
    keywords.append(c.replace(" ", ""))
    #keywords2.append(c.replace(" ", ""))




keyword = keywords

print ' '.join(keyword)

#searchWordArray = np.array(res3)
#for i, a in app2_2000_name.iterrows():
#    print a['name']

ii = 0;

# datadic = {}
import pandas as pd
app_list_already = pd.read_csv('already_app.csv')
print app_list_already.shape
app_list_already.head()
app_already_set =  set(map(lambda i : i[1].replace('"',''),app_list_already.to_dict()['appname'].items()))

already = app_list_already.to_dict()
print app_list_already.shape

#PMICrawler.initKeywords(keyword)
norms = 0.0000001
count =0
import time
for app_ in app_already_set:
    st = time.time()
    print app_, count
    for key in keyword[:]:
        key = '"' + key + '"'
        print key
        cw = PMICrawler('"' + app_ + '"', key, norms)
        cw.start()
    count+=1
    print "computing time : ", time.time()-st
# datadic = sorted(datadic.items(), key=lambda (k,v) : (v,k), reverse=True)
# for idx,each in enumerate(datadic[:20]) :
#     print idx, each[0],each[1]

'''
for a in searchWordArray:
    a = ''.join(a)
    sys.stdout.flush()
    sys.stdout.write('\r')
    sys.stdout.write("app %s start: count=%d\n" % (a, ii))
    ii += 1;

    for key in keyword:

	ret = DatabaseManager.get_app_keyword_pmi('"'+a+'"', '"'+key+'"')

		#sys.stdout.write(" [%f: app %s  key %s] " % (ret, a, key))

	if ret == 0:
		sys.stdout.write(" [%d: app %s  key %s] " % (ii, a, key))
			#  searchWordList = ["+".join(a)+key]

		cw = PMICrawler('"'+a+'"', '"'+key+'"')
		cw.start()

			#    DatabaseManager.set_app_keyword_pmi(a, key, pmi)
			#     sys.stdout.write("pmi=%.2f : (%s), (%s), (%s)\n" % (pmi, a, key, "".join(a)+key))

print "done."
                                            '''