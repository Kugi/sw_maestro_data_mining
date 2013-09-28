#coding:utf-8
import json
import logging
from wsgiref import simple_server
import urllib

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

from buzz_rpc.src.App import App
import inspect
class AppResource(App):

    def __init__(self):
        pass
        # self.logger = logging.getLogger('thingsapi.' + __name__)

    def inspect_func(self, result):
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

    def on_get(self, req, resp,func_name=''):
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

            method_args = inspect.getargspec(getattr(self,func_name))
            for each_args in method_args.args:
                if each_args == 'self' or not req._params.has_key(each_args):
                    continue
                param[each_args] = req._params[each_args]
            print "param:",param
            result = getattr(self,func_name)(**param)
            if func_name == 'get_list':
                result = result[0]
        # result = req._params
        print "method:",func_name,"param:",param
        # result = result[0]
        #print "result:",result
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result)

wsgi_app = api = falcon.API(before=[auth, check_media_type])

db = StorageEngine()
app = AppResource()
# api.add_route('/{user_id}/things', things)
api.add_route('/app/{func_name}', app)
api.add_route('/app', app)
app = application = api
# Useful for debugging problems in your API; works with pdb.set_trace()
if __name__ == '__main__':
    # gunicorn 으로 실행할때에는
    # gunicorn -w 7 -k eventlet BuzzREST:app -b 0.0.0.0:9009

    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
