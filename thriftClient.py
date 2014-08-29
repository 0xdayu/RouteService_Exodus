import sys
sys.path.append('./gen-py')
 
from route import RouteService
from route.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift import Thrift
 
import socket

try:
    transport = TSocket.TSocket('192.168.1.103', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = RouteService.Client(protocol)
    transport.open()

    #Test topology
    f = open("test_topo", "r")

    for line in f.readlines()[1:]:
        line = line.strip()
        tokens = line.split(",")
        n = Notification()
        n.notificationType = "LINKSTATE_UP"
        n.values = {}
        n.values["srcsw"] = tokens[0]
        n.values["srcpt"] = tokens[1]
        n.values["dstsw"] = tokens[2]
        n.values["dstpt"] = tokens[3]
        n.values["cost"] = tokens[4]
        client.notifyMe(n)
    f.close()   
    
    f = open("switch_config", "r")

    for line in f.readlines()[1:]:
        line = line.strip()
        token = line.split(",")
        n = Notification()
        n.notificationType = "SWITCH_CONFIG"
        n.values = {}
        n.values["swid"] = token[0]
        n.values["ptid"] = token[1]
        n.values["prefix"] = token[2]
        n.values["mask"] = token[3]
        client.notifyMe(n)
    f.close()
    
    q = Query()
    q.arguments = ["5","c","c","c"]
    result = client.doQuery(q)

    print result

except Thrift.TException, ex:
  print "%s" % (ex.message)
