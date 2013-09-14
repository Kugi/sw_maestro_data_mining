import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

def is_even(n):
    return n%2 == 0

server = SimpleXMLRPCServer(("localhost", 8010))
print "Listening on port 8010..."
server.register_function(is_even, "is_even")
server.serve_forever()
