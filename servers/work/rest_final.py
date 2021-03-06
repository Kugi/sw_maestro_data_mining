#coding:utf-8

__author__ = 'jeongmingi'

import json
import logging
from wsgiref import simple_server
import urllib
import pickle
import pandas as pd
import falcon
import numpy as np
from datetime import date
from sklearn.externals import joblib
import inspect


_AUTHKEY_DICT = {'namsangboy':'UnpvK25V0PY7XDzsDROBiDESQ7UUoUFphf'}
uapp = pickle.load(file('data/user_app.df'))
apps = pickle.load(file('data/app_info2.df'))
user_gender = pickle.load(file('data/profiled_gender.pkl'))
user_gender['gender'] = (-1) * user_gender['gender'] + 3




class StorageEngine:
    pass
class StorageError(Exception):
    pass
def token_is_valid(token, user_id):
    return True  # Suuuuuure it's valid...
def auth(req, resp, params):
    # Alternatively, do this in middleware
    token = req.get_header('X-Auth-Token')
    # if token is None:
    #     raise falcon.HTTPUnauthorized('Auth token required',
    #                                   'Please provide an auth token '
    #                                   'as part of the request',
    #                                   'http://docs.example.com/auth')

    if not token_is_valid(token, params.get('user_id','')):
        raise falcon.HTTPUnauthorized('Authentication required',
                                      'The provided auth token is '
                                      'not valid. Please request a '
                                      'new token and try again.',
                                      'http://docs.example.com/auth')

def check_media_type(req, resp, params):
    if not req.client_accepts_json:
        raise falcon.HTTPUnsupportedMediaType(
            'Media Type not Supported',
            'This API only supports the JSON media type.',
            'http://docs.examples.com/api/json')


class AppResource():

    def __init__(self):
        pass
        # self.logger = logging.getLogger('thingsapi.' + __name__)

    def inspect_func(self, result):                                         #url -- inspect 함수기능 search...
        func_list = inspect.getmembers(App, predicate=inspect.ismethod)
        for each_name, each_method in func_list:
            method_args = inspect.getargspec(each_method)
            defaults = []
            if method_args.defaults:
                defaults = method_args.defaults
            args = []
            for idx, each_args in enumerate(method_args.args):
                if each_args == 'self':
                    continue
                info = {'name': each_args, 'z_default': 'undefined'}
                if idx < len(defaults):
                    info['z_default'] = defaults[idx]
                args.append(info)
            result.append({'param': args,'method': each_name})

    def parse_params(self, req):
        for key in req._params.keys():
            if req._params[key].isdigit():
                req._params[key] = int(req._params[key])
            else:
                req._params[key] = urllib.unquote(req._params[key])

    def on_get(self, req, resp,func_name=''):                   #!!!!!!!!!!!!!!!중요
        result = []
        print dir(req)
        print req._params

        self.parse_params(req)
        if not func_name:
            func_name=req._params.pop('func','')
        print "func_name:",func_name
        param = {}
        if func_name == 'inspect':
            self.inspect_func(result)
        else:
            print "func_name:",func_name,":",req._params
            if func_name == 'query':
                func_name = 'get_list'

            method_args = inspect.getargspec(getattr(self,func_name))           #self.func_name의 사용하는 params 인자를 받아온다.
            for each_args in method_args.args:
                if each_args == 'self' or not req._params.has_key(each_args):   #req에서 받은 값들 중에 유효한 키를 받지 않으면...
                    continue
                param[each_args] = req._params[each_args]
            print "param:",param
            result = getattr(self,func_name)(**param)           #self자기 객체, func_name;클래의함수내임
            if func_name == 'get_list':
                result = result[0]
        # result = req._params
        print "method:",func_name,"param:",param
        # result = result[0]
        #print "result:",result
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result)    #result를 dump하면 body로...

    def add(self,a, b):
        return a*b;






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
        return {"male" : male, "female":female};


    def weekDay(self, i):
        year = i/10000
        month = i%10000/100
        day = i%100
        weekday = date(year, month, day).weekday()
            #print "year:%d month:%d day:%d weekday:%d"%(year, month, day, weekday)
        return weekday

    def addWeekday(self, id_, date, cnt):
        result = []
        for a, b in zip(date, cnt):
            temp = {'id': id_, 'date': a, 'weekday':self.weekDay(a), 'count': b}
            result.append(temp)
        return result

    def date_app(self, id_):
        app = uapp.ix[uapp['entity_id']==id_]

        app['create_date'] = app['create_date']//1000000
        app['update_date'] = app['update_date']//1000000

        keys = app['create_date'].unique()


        b = app.groupby('create_date')
        data1 = []
        for name, group in b:
            name = int(name)
            temp = {'date' : name, 'cnt' : int(len(group))}
            data1.append(temp)
            
        pd_data1 = pd.DataFrame(data1)

        a = pd_data1.date.values
        b = pd_data1.cnt.values

        group = self.addWeekday(id_, a, b)
        group_ = pd.DataFrame(group)
        group_weekday = group_.groupby('weekday')
        cnt_group_weekday = group_weekday['count'].sum()
        cnt_weekday = {}
        cnt_weekday['mon'] = int(cnt_group_weekday[0])
        cnt_weekday['tue'] = int(cnt_group_weekday[1])
        cnt_weekday['wed'] = int(cnt_group_weekday[2])
        cnt_weekday['thu'] = int(cnt_group_weekday[3])
        cnt_weekday['fri'] = int(cnt_group_weekday[4])
        cnt_weekday['sat'] = int(cnt_group_weekday[5])
        cnt_weekday['sun'] = int(cnt_group_weekday[6])

        return cnt_weekday



    def process(self, id_):
        group_ = pd.DataFrame()

        app = uapp.ix[uapp['entity_id']==id_]
        app['create_date'] = app['create_date']//1000000
        app['update_date'] = app['update_date']//1000000
        keys = app['create_date'].unique()
        b = app.groupby('create_date')
    
        data1 = []
        for name, group in b:
            name = int(name)
            temp = {'date' : name, 'cnt' : int(len(group))}
            data1.append(temp)
            pd_data1 = pd.DataFrame(data1)
            a = pd_data1.date.values
            b = pd_data1.cnt.values
        
            group = self.addWeekday(id_, a, b)
            temp = pd.DataFrame(group)
            temp_weekday = temp.groupby('weekday')
            cnt_group_weekday = temp_weekday['count'].sum()
            temp['totweek_app'] = 0
            #temp['weekday'] == 2 = False처럼 값을 갖지않는 경우 에러 생긴다.
            for i in temp['weekday'].unique():
                temp.ix[temp['weekday']==i, 'totweek_app'] = int(cnt_group_weekday[i])
            group_ = temp
        
        data = []
        for i, key in enumerate(group_['date'].values):
            c = group_.ix[group_['date']==key, 'count'].values
            w = group_.ix[group_['date']==key, 'weekday'].values
            t = group_.ix[group_['date']==key, 'totweek_app'].values
            data.append({"date" : int(key), "count" : int(c), "weekday":int(w), "totweek":int(t)})
    
        return data




    def process2(self, id_):
        group_ = pd.DataFrame()

        app = uapp.ix[uapp['entity_id']==id_]
        app['create_date'] = app['create_date']//1000000
        app['update_date'] = app['update_date']//1000000
        keys = app['create_date'].unique()
        b = app.groupby('create_date')
    
        data1 = []
        for name, group in b:
            name = int(name)
            temp = {'date' : name, 'cnt' : int(len(group))}
            data1.append(temp)
            pd_data1 = pd.DataFrame(data1)
            a = pd_data1.date.values
            b = pd_data1.cnt.values
        
            group = self.addWeekday(id_, a, b)
            temp = pd.DataFrame(group)
            temp_weekday = temp.groupby('weekday')
            cnt_group_weekday = temp_weekday['count'].sum()
            temp['totweek_app'] = 0
            #temp['weekday'] == 2 = False처럼 값을 갖지않는 경우 에러 생긴다.
            for i in temp['weekday'].unique():
                temp.ix[temp['weekday']==i, 'totweek_app'] = int(cnt_group_weekday[i])
            group_ = temp
        
        data = []
        for i, key in enumerate(group_['date'].values):
            c = group_.ix[group_['date']==key, 'count'].values
            w = group_.ix[group_['date']==key, 'weekday'].values
            t = group_.ix[group_['date']==key, 'totweek_app'].values
            data.append({"date" : int(key), "count" : int(c), "weekday":int(w), "totweek":int(t)})
        
        d = pd.DataFrame(data)
        d['month'] = 0;
        d['date'].values
        for i in d['date'].values:
            d.ix[d['date']==i, 'month'] = int(i)%10000/100
        b = d.groupby('month')
        data1 = []
        temp = {}
        for name, group in b:
           name = int(name)
           temp['m'+str(name)] = int(len(group))
            
        return temp


    def process3(self, id_):
        from sklearn.externals import joblib
        
        group_ = pd.DataFrame()
                
        filename = "data/regression_model_weekday500.pkl"
        clf = joblib.load(filename)
        app = uapp.ix[uapp['entity_id']==id_]
        app['create_date'] = app['create_date']//1000000
        app['update_date'] = app['update_date']//1000000
        keys = app['create_date'].unique()
        b = app.groupby('create_date')
        
        data1 = []
        for name, group in b:
            name = int(name)
            temp = {'date' : name, 'cnt' : int(len(group))}
            data1.append(temp)
            pd_data1 = pd.DataFrame(data1)
            a = pd_data1.date.values
            b = pd_data1.cnt.values
            group = self.addWeekday(id_, a, b)
            
            temp = pd.DataFrame(group)
            temp_weekday = temp.groupby('weekday')
            cnt_group_weekday = temp_weekday['count'].sum()
            temp['totweek_app'] = 0
            #temp['weekday'] == 2 = False처럼 값을 갖지않는 경우 에러 생긴다.
            for i in temp['weekday'].unique():
                temp.ix[temp['weekday']==i, 'totweek_app'] = int(cnt_group_weekday[i])
            group_ = temp
            
        test = [{'id' : id_ , 'weekday' : 0, 'totweek_app' : int(cnt_group_weekday[0])},
            {'id' : id_ , 'weekday' : 1, 'totweek_app' : int(cnt_group_weekday[1])},
            {'id' : id_ , 'weekday' : 2, 'totweek_app' : int(cnt_group_weekday[2])},
            {'id' : id_ , 'weekday' : 3, 'totweek_app' : int(cnt_group_weekday[3])},
            {'id' : id_ , 'weekday' : 4, 'totweek_app' : int(cnt_group_weekday[4])},
            {'id' : id_ , 'weekday' : 5, 'totweek_app' : int(cnt_group_weekday[5])},
            {'id' : id_ , 'weekday' : 6, 'totweek_app' : int(cnt_group_weekday[6])}
            ]

        temp = {}       
    
        test = pd.DataFrame(test)
        for i, cnt in enumerate(clf.predict(test)):
            temp['w'+str(i)] = cnt

        return temp
        
    def wow_cluster(self, name):
        app_names = ["Sky+", "Facebook", "Twitter", "YouTube", "IM+"]
	
	result = [
        	
            {'id' : app_names[0], 'value' : 0},
            {'id' : app_names[1], 'value' : 1},
            {'id' : app_names[2], 'value' : 2},
            {'id' : app_names[3], 'value' : 3.4},
            {'id' : app_names[4], 'value': 3.2}
        
        ]
        return result



    def weekDay_new(self, id_):
        app = uapp.ix[uapp['entity_id']==id_]

        app['create_date'] = app['create_date']//1000000
        app['update_date'] = app['update_date']//1000000

        keys = app['create_date'].unique()


        b = app.groupby('create_date')
        data1 = []
        for name, group in b:
            name = int(name)
            temp = {'date' : name, 'cnt' : int(len(group))}
            data1.append(temp)
        pd_data1 = pd.DataFrame(data1)

        a = pd_data1.date.values
        b = pd_data1.cnt.values

        group = self.addWeekday(id_, a, b)
        group_ = pd.DataFrame(group)
        group_weekday = group_.groupby('weekday')
        cnt_group_weekday = group_weekday['count'].sum()

        cnt_weekDay = []
        cnt_weekDay.append({"count":int(cnt_group_weekday[6]),"name":"Sun"})
        cnt_weekDay.append({"count":int(cnt_group_weekday[0]),"name":"Mon"})
        cnt_weekDay.append({"count":int(cnt_group_weekday[1]),"name":"Tue"})
        cnt_weekDay.append({"count":int(cnt_group_weekday[2]),"name":"Wed"})
        cnt_weekDay.append({"count":int(cnt_group_weekday[3]),"name":"Thu"})
        cnt_weekDay.append({"count":int(cnt_group_weekday[4]),"name":"Fri"})
        cnt_weekDay.append({"count":int(cnt_group_weekday[5]),"name":"Sat"})

        #cnt_weekday = {}
        #cnt_weekday['mon'] = int(cnt_group_weekday[0])
        #cnt_weekday['tue'] = int(cnt_group_weekday[1])
        #cnt_weekday['wed'] = int(cnt_group_weekday[2])
        #cnt_weekday['thu'] = int(cnt_group_weekday[3])
        #cnt_weekday['fri'] = int(cnt_group_weekday[4])
        #cnt_weekday['sat'] = int(cnt_group_weekday[5])
        #cnt_weekday['sun'] = int(cnt_group_weekday[6])

        #return cnt_weekday
        return cnt_weekDay




    def date_new(self, id_):
        group_ = pd.DataFrame()

        app = uapp.ix[uapp['entity_id']==id_]
        app['create_date'] = app['create_date']//1000000
        app['update_date'] = app['update_date']//1000000
        keys = app['create_date'].unique()
        b = app.groupby('create_date')
    
        data1 = []
        for name, group in b:
            name = int(name)
            temp = {'date' : name, 'cnt' : int(len(group))}
            data1.append(temp)
            pd_data1 = pd.DataFrame(data1)
            a = pd_data1.date.values
            b = pd_data1.cnt.values
        
            group = self.addWeekday(id_, a, b)
            temp = pd.DataFrame(group)
            temp_weekday = temp.groupby('weekday')
            cnt_group_weekday = temp_weekday['count'].sum()
            temp['totweek_app'] = 0
            #temp['weekday'] == 2 = False처럼 값을 갖지않는 경우 에러 생긴다.
            for i in temp['weekday'].unique():
                temp.ix[temp['weekday']==i, 'totweek_app'] = int(cnt_group_weekday[i])
            group_ = temp
        
        data = []
        for i, key in enumerate(group_['date'].values):
            c = group_.ix[group_['date']==key, 'count'].values
            
            keystr = str(key)
            keystr_form = "{0}-{1}-{2}T15:00:00.000Z".format(keystr[0:4], keystr[4:6], keystr[6:8])
            

            
            data.append({"date" : keystr_form, "close" : float(c)})
    
        return data


wsgi_app = api = falcon.API(before=[auth, check_media_type])

db = StorageEngine()
app = AppResource()
# api.add_route('/{user_id}/things', things)
api.add_route('/app/{func_name}', app) #해당 url을 입력하면 app을 호출...
api.add_route('/app', app)
app = application = api
# Useful for debugging problems in your API; works with pdb.set_trace()
if __name__ == '__main__':
    # gunicorn 으로 실행할때에는
    # gunicorn -w 7 -k eventlet BuzzREST:app -b 0.0.0.0:9009

    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
