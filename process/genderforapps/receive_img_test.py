#coding: utf-8

__author__ = 'jeongmingi'


import xmlrpclib

def main():
    server = xmlrpclib.Server("http://localhost:10080")
    print server
    img_path = "appGender.png"
    #_IMG_RPC =
    binary_img = xmlrpclib.Binary(open(img_path, "rb").read())
    imgname, width, height = _IMG_RPC.save(binary_img)

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