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
import cloudfiles


class Command(object):
    def __init__(self,socket, user):
        self.cmd = "avconv -i "+user+"/%05d.jpg -c:v libx264 -r 30 "+user+"/foo.mp4"
        self.process = None
        self.socket=socket

    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True)
            a=self.process.communicate()
            pdb.set_trace()

      
        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()
            self.socket.sendMessage("1",False)
        else:
          self.socket.sendMessage("0",False)
        print self.process.returncode
 
class EchoServerProtocol(WebSocketServerProtocol):

  def onMessage(self, msg, binary):
    jsonmsg=simplejson.loads(msg)
    userID=jsonmsg["user"]
    if os.path.exists(userID):
      shutil.rmtree(userID)
    os.makedirs(userID)
    for x in range(1, 375):
      fileframe=str(x)
      output=open(userID+"/"+fileframe.zfill(5)+".jpg","wb")
      output.write(base64.b64decode(jsonmsg[str(x)]))
      output.close()
    command=Command(self,userID)
    command.run(timeout=60)

if __name__ == '__main__': 	
   print "starting"
   factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
   factory.protocol = EchoServerProtocol
   listenWS(factory)   
   reactor.run()





   #command = Command("echo 'Process started'; sleep 2; echo 'Process finished'")
#command.run(timeout=3)
#command.run(timeout=1)
