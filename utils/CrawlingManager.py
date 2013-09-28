__author__ = 'kugi'

import re
import time

import requests
from scrapy.selector import HtmlXPathSelector

import DatabaseManager

class CrawlingManager(object):

    def __init__(self, searchWordsAsSeries, startIndex=None, endIndex=None):
        self.startIndex = startIndex if startIndex != None else 0
        self.endIndex = endIndex if endIndex != None else len(searchWordsAsSeries)
        self.waitMinute = 0
        self.searchWordsAsSeries= searchWordsAsSeries

    def __search(self,q):
        """
        parameter:
            q : String for search.
        """
        try:
            q='+'.join(q.split())
            xpath = """//div[@id='content']/div[@class='blog section _blogBase']/div[@class='section_head']/span[@class='title_num']"""
            html = requests.get("http://cafeblog.search.naver.com/search.naver?where=post&sm=tab_jum&ie=utf8&query="+q).text
            hx =HtmlXPathSelector(text=html)
            items = hx.select(xpath)
            inputstr = (items.extract()[0].split()[3]+"")
            result = int(''.join(re.findall(r'\d+', inputstr)))
            print result
            return result
        except:
            print "except 0"
            return 0


    def __ifError(self,word):
        print "stuck at "+word
        while True:
            time.sleep(self.waitMinute*60)
            try:
                self.__search(word)
                print "sleeping... :  %d" %(self.waitMinute*60)
            except:
                self.waitMinute += 1
                continue
            break
        print "escape!!!"

    def start(self):
        for index in range(self.startIndex,self.endIndex):
            word = self.searchWordsAsSeries[index]
            try:
                DatabaseManager.set_query_count('+'.join(word.split()),self.__search(word))
            except:
                print "stuck index: %d, %s "%index, word
                self.__ifError(word)
            if index % 100 ==0 and index!=0:
                print "pass 100 : %d"%index
        print "doneait"
