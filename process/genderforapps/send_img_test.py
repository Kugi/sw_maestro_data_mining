#coding:utf8

__author__ = 'jeongmingi'

import Image, sys,os
from twisted.web import xmlrpc, server
from twisted.internet import reactor
sys.path.append("/home/newmoni/workspace/utils/src")
from time import time



_PATH = "appGender.png"
class ImgRpc(xmlrpc.XMLRPC):

    def xmlrpc_save(self, data="", mode=""):
        if data == "rest": # old version 과 호환하기위함
            data = mode
        if type(data) != str:
            data = data.data

        s_time = time()

        # img file name
        fname  = "%s" % (_PATH)
        # save img
        f = open(fname, "wb")
        f.write(data)
        f.close()

        # get img info
        img_open = Image.open(fname)
        width, height = img_open.size
        e_time = time()
        print "%s\t(%d,%d)\t%d\t%.2f" % code, width, height, len(data), (e_time-s_time)
        return code, width, height

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage='%prog [options] \nDescription: buzzni img xmlrpc server.'.decode("utf-8"))
    parser.add_option("--port", default = 10080, help="포트 번호".decode("utf-8"))
    parser.add_option("--host", default = "localhost", help="host ".decode("utf-8"))
    parser.add_option("--pool", default=100, type="int", help="pool size")
    (options, args) = parser.parse_args()

    print "IMG RPC START:\t", options.host, ":", options.port
    reactor.suggestThreadPoolSize(options.pool)
    reactor.listenTCP(int(options.port), server.Site(ImgRpc()),interface=options.host)
    reactor.run()


