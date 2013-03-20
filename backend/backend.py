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
import subprocess

class Command(object):
    def __init__(self, cmd,user):
        self.cmd = "avconv -i "+user+"/%05d.jpg -c:v libx264 -r 30 /"+user+"/foo.mp4"
        self.process = None

    def run(self, timeout):
        def target():
            print 'Thread started'
            self.process = subprocess.Popen(self.cmd, shell=True)
            self.process.communicate()
            print 'Thread finished'

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            print 'Terminating process'
            self.process.terminate()
            thread.join()
        print self.process.returncode

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
    jsonmsg=simplejson.loads(msg)
    userID=jsonmsg["user"]
    if jsonmsg["frame"]==1:
      if os.path.exists(userID):
        shutil.rmtree(userID)
      os.makedirs(userID)
    fileframe=str(jsonmsg["frame"])
    output=open(userID+"/"+fileframe.zfill(5)+".jpg","wb")
    output.write(base64.b64decode(jsonmsg["payload"]))
    output.close()

if __name__ == '__main__': 	
   print "starting"
   factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
   factory.protocol = EchoServerProtocol
   thread1 = LogThread(factory)
   listenWS(factory)   
   reactor.run()
