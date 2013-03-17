from twisted.internet import reactor
from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS
import sys
import threading
import time
import StringIO
import pdb
import json as simplejson
import base64
import os
import shutil
import lzw


class LogThread(threading.Thread):
     def __init__(self,factory):
        threading.Thread.__init__(self)
        self.factory=factory

     def run(self):
   	  	count=0
   		while(count==0):
   			p="Current Connections:"+str(self.factory.getConnectionCount())
			print p 
			time.sleep(5)
 
class EchoServerProtocol(WebSocketServerProtocol):

  def onMessage(self, msg, binary):
 #   rm=lzw.readbytes(msg)
  #  dm=lzw.decompress(rm)
   # string=""
    #for i in dm:
     # string=string+i
   # pdb.set_trace()
    jsonmsg=simplejson.loads(msg)
 #   pdb.set_trace()
    userID=jsonmsg["user"]
    if jsonmsg["frame"]==1:
      if os.path.exists(userID):
        shutil.rmtree(userID)
      os.makedirs(userID)
    frameLength=len(str(jsonmsg["frame"]))
    fileframe=jsonmsg["frame"]*pow(10,5-frameLength) # no check for maximum
  #  print str(fileframe)
#    pdb.set_trace()
    output=open(userID+"/"+str(fileframe)+".jpg","wb")
    output.write(base64.b64decode(jsonmsg["payload"]))
    output.close()
 #   print msg
#    output=open("test.jpg","wb")
 #   output.write(base64.b64decode(msg))
  #  output.close()

if __name__ == '__main__': 	
   print "starting"
   factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
   factory.protocol = EchoServerProtocol
   thread1 = LogThread(factory)
   listenWS(factory)   
   reactor.run()