#coding: utf-8

__author__ = 'jeongmingi'


import xmlrpclib
import pickle
import numpy as np

def main():
    """
        get_count_gender(app), if you input app id as app, it will return counted male, female #
        graph_gender_rate(apps), if you input apps as list of "id",
            it will return frame that has name in index, n_male & n_female in colums
            it will return norm_frame that has name in index, rate of male & female in colums

    """


    #apps = pickle.load(file('data/app_info2.df')) #app의 id를 출력 하기위함... 실제 id만 있어도 가능.
    server = xmlrpclib.Server("http://localhost:2013/output0")
    #i = apps['id'][0]
    #print server.get_count_gender(int(i))

    #applist = apps['id'][:5].values.tolist()
    #frame = server.get_graph_for_gender(applist)

    f = server.xmlrpc_save('')
    binary_img = xmlrpclib.Binary(open(f, "rb").read())



    '''
    dic_ = apps[:5].to_dict()       #can be update
    #apps_ = apps[:5]
    converted_ = []
    for i in dic_['id']:
        #converted_.append(int(i))
        temp = {}
        temp = {'id' : int(dic_['id'][i]), 'name' : str(dic_['name'][i])}
        converted_.append(temp)

    print converted_

    frame, norm_frame = server .graph_gender_rate(converted_)

    print frame[:], '\n', norm_frame[:]
    '''

    print server.system.listMethods()  #print list methods.... kk

if __name__ == "__main__" :
    main()



'''
# Create an object to represent our server.
server_url = 'http://localhost:8800';
server = xmlrpclib.Server(server_url);

# Call the server and get our result.
result = server.sample.sumAndDifference(5, 3)
print "Sum:", result['sum']
print "Difference:", result['difference']
'''