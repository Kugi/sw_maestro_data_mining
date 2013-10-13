#coding:utf-8

__author__ = 'jeongmingi'

import json
import logging
from wsgiref import simple_server
import urllib
import pickle
import pandas as pd

import falcon
_AUTHKEY_DICT = {'namsangboy':'UnpvK25V0PY7XDzsDROBiDESQ7UUoUFphf'}

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

import inspect
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
        return a+b;

    def get_count_gender(self, app):
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
        return male


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

    httpd = simple_server.make_server('127.0.0.1', 9016, app)
    httpd.serve_forever()

