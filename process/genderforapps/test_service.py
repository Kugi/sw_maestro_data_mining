__author__ = 'jeongmingi'

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import gender_for_apps
import numpy
import pickle

class RequestHandler(SimpleXMLRPCRequestHandler) :
    rpc_paths = ("/output0",)

def main() :
    server = SimpleXMLRPCServer(("localhost", 2013), requestHandler=RequestHandler)
    server.register_introspection_functions()
    server.register_instance(gender_for_apps.GenderForApps())
    try :
        print "Listing 2013"
        server.serve_forever()
    except KeyboardInterrupt :
        print "exit..."


if __name__ == "__main__" :
    main()

'''
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)




# Create server
server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler)
server.register_introspection_functions()

# Register pow() function; this will use the value of
# pow.__name__ as the name, which is just 'pow'.
server.register_function(pow)

# Register a function under a different name
def adder_function(x,y):
    return x + y
server.register_function(adder_function, 'add')



# xmlrpc, in server, classes provied.
# Register an instance; all the methods of the instance are
# published as XML-RPC methods (in this case, just 'mul').
class MyFuncs:
    def mul(self, x, y):
        return x * y

server.register_instance(MyFuncs())

# Run the server's main loop
server.serve_forever()
'''