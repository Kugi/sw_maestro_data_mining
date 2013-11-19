# -*- coding: utf-8 -*-

__author__ = 'jeongmingi'


#!/usr/bin/python

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
# db에 저장하고 불러오는 클래스 집합
class DatabaseManager():

    __BaseObj__ = declarative_base()
    __db__ = create_engine('postgresql://soma:maestro@)!#@soma3.buzzni.com/application')
    __Session__ = sessionmaker(bind=__db__)
    #__s__ = __Session__()

    #__db__.echo = False  # Try changing this to True and see what happens
    #__metadata__ = MetaData(__db__)

    #db중에 query_freq테이블에 만들고 setting하는 명령어.
    class Cache_query(__BaseObj__):
        __tablename__ = 'query_freq'
        query = Column('query', String(100), primary_key=True) #primary_key, 기본키(중복이안되고 null값이 아닌)
        num = Column('num', Integer)
        update_date = Column('update_date', Date(),default=datetime.now(), onupdate=datetime.now())
        def __init__(self,query,num):
            self.query=query
            self.num=num

    #db중에 app_keyword_pmi테이블에 만들고 setting하는 명령어.
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

    #s.query를 날리는데 table중에서 Cache_query에 해당하는 테이블에서 .query == query를 만족하는 값을 받아온다.
    @staticmethod
    def get_query_count(query):
        s = DatabaseManager.__Session__()
        result = s.query(DatabaseManager.Cache_query).filter(DatabaseManager.Cache_query.query == query)
        s.close_all() #db연결을 끊는다.

        if result.count()>0: #.count()가 0보다 크지않으면 제대로 안들어있는 db데이터
            return result[0].num
        return 0

    #s.query를 날리는데 table중에서 Cache_query에 해당하는 테이블에서 .query == query를 만족하는 값을 저장한다.
    @staticmethod
    def set_query_count(query, count):
        s = DatabaseManager.__Session__()
        result = s.query(DatabaseManager.Cache_query).filter(DatabaseManager.Cache_query.query == query)

        if result.count()>0:
            result[0].num = count
        else:
            s.add(DatabaseManager.Cache_query(query,count)) #db에 저장하는 부분
        s.commit() #query 명령을 한번에 수행(add하고 commit안하면 실행x)
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

    #filter를 통해 app_name, keyword에 맞는 Cache_pmi 테이블에 저장되어진 값을(result) 받아온다
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

    #filter를 통해 app_name, keyword에 맞는 Cache_pmi 테이블에 저장한다.(app_name, keyword)
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

tempDebug = 0;

class PMICrawler(object):

    waitMinute = 0

    #class 변수 셋팅
    def __init__(self, appname, keyword, startIndex=None, endIndex=None):
        PMICrawler.waitMinute = 0
        self.appname = appname
        self.keyword = keyword
        self.both = self.appname + "+" + self.keyword

    #검색엔진에 검색을 해서 결과 갯수(result)를 반환, q는 검색어
    @staticmethod
    def __search(q):

        sleep(1) #1초 sleep
        """
        parameter:
            q : String for search.
        """
        try:
            q ='+'.join(q.split())
            xpath = """//span[@class='title_num']""" #검색어 결과 갯수 나오는 위치
            #user agendt삽입, mobile로하면 그것에서 검색한 효과
            _MOBILE_HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.162 Safari/535.19'}
            #url q 검색한 주소
            url = "http://cafeblog.search.naver.com/search.naver?where=post&sm=tab_jum&ie=utf8&query="+q
            #해당 url의 모든 html받기
            html = requests.get(url, headers=_MOBILE_HEADER).text
            #html에서 xpath부분 짤라서 가져온다.
            hx = HtmlXPathSelector(text=html)
            items = hx.select(xpath)
            inputstr = (items.extract()[0].split()[3]+"") #숫자만 빼기(문자열)
            result = int(''.join(re.findall(r'\d+', inputstr))) #숫자
            return result
        except Exception, e:
            print e
            if q != '네이버1' and q != '""':
                PMICrawler.__ifError(q)
            print "except 0"
            return 0



    @staticmethod
    def __ifError(word):
        tempRes = PMICrawler.__search('네이버1')
        if tempRes <= 0: #결과(tempRes)가 안나오면 짤린것
            print ("tempRes=%d" % tempRes)

            print "stuck at ["+ word + "]" #검색어(p) 출력
            while True:
                if PMICrawler.waitMinute <= 0:
                    PMICrawler.waitMinute = 1
                PMICrawler.waitMinute *= 2
                if PMICrawler.waitMinute >= 1440:
                    PMICrawler.waitMinute = 1440

                print "sleeping... :  %d" %(PMICrawler.waitMinute*60)
                time.sleep(PMICrawler.waitMinute*60)

                tempRes = PMICrawler.__search('네이버1')
                if tempRes == 0:
                    continue;
                else:
                    try:
                        keyRes1 = PMICrawler.__search(word)
                        DatabaseManager.set_query_count(word, keyRes1) #word(p)
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

        appRes = self.__search(self.appname)

        if ( appRes != 0 ):

            keyRes = DatabaseManager.get_query_count(self.keyword)
            botRes = self.__search(self.both)

            DatabaseManager.set_query_count(self.appname, appRes)
            DatabaseManager.set_query_count(self.both, botRes)
            print appRes, keyRes, botRes

            pmi = self._calcPMI(appRes, keyRes, botRes, 1000000000.0)
            DatabaseManager.set_app_keyword_pmi(self.appname, self.keyword, pmi)

            print 'pmi=', pmi



    def _calcPMI(self, AppScore, KeywordScore, BothScore, nTotalDocs):

        if AppScore <= 0 or KeywordScore <= 0:
            return 0

        t = 1000000000.0
        pa = AppScore/t
        pb = KeywordScore/t
        pab = BothScore/t
        #(AppScore*KeywordScore/(BothScore*nTotalDocs))

        if pa <= 0 or pb <= 0 or pab <= 0:
            return 0
        val = math.log((pab+0.0000001)/(pa*pb + 0.0000001))


        return val



app_list_new = pd.read_csv('./data/app_list.csv')
print app_list_new

# app2 =  pd.read_pickle('./data/app_info2.df')
# app2 = app2[np.isfinite(app2['rate_num_all'])]
# app2_name = app2.loc[:,['name']]
# print app2.head()
# app2 = app2.sort(['rate_num_all'], ascending=False)
# #print app2[['name', 'rate_num_all']][5:25]
# res = app2.ix[app2['rate_num_all']>=5000]
# res2 = res.ix[res['score']>50]
# print 'size:'
# print res.shape
# res3 = res2['name']
# #print res3


def load(fname):
    ''' load the file using std open'''
    f = open(fname,'r')

    data = []
    for line in f.readlines():
        data.append(line.replace('\n','').split(','))

    f.close()

    return data


key = load('./data/Keyword.txt')
keywords = []
#keywords2 = [""]
for c in key[0]:
# keywords.append('+"'+c.replace(" ", "")+'"')
    keywords.append(c.replace(" ", ""))
    #keywords2.append(c.replace(" ", ""))




keyword = keywords

#print ' '.join(keyword)

searchWordArray = np.array(app_list_new)
#for i, a in app2_2000_name.iterrows():
#    print a['name']

ii = 0;

app_list_new = pd.read_csv('./data/app_list.csv')
print app_list_new.shape

app_list_new.head()
#PMICrawler.initKeywords(keyword)
app_list_already = pd.read_csv('./data/already_app.csv')
print app_list_already.shape
app_list_already.head()
app_already_set =  set(map(lambda i : i[1].replace('"',''),app_list_already.to_dict()['appname'].items()))

already = app_list_already.to_dict()


ct = 0
searchWordArray = []
for idx, app in app_list_new[:].iterrows():
    temp = app['appname']
    if temp in app_already_set:
        ct +=1
    else:
        searchWordArray.append(temp)
print ct
print len(searchWordArray)

from random import choice
from time import sleep

countt = 0
startnum = 7980
for idx, a in enumerate(searchWordArray[startnum:8000]):
    print startnum+countt
    countt += 1
    a = ''.join(a)
    sys.stdout.flush()
    sys.stdout.write('\r')
    sys.stdout.write("app %s start: count=%d\n" % (a, ii))
    ii += 1;
    if not(idx % 5):
        t= choice(range(10))
        print "tempo sleep: ", t
        sleep(t)


    cw = PMICrawler('"'+a+'"','')
    cw.start()
    appResult = DatabaseManager.get_query_count('"'+a+'"')
    print appResult

    if(appResult > 0):
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
