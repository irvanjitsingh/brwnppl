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
import random
import requests

class Command(object):
    def __init__(self,socket, user):
        self.cmd = "avconv -i "+user+"/%05d.jpg -c:v libx264 -r 30 "+user+"/foo.mp4"
        self.process = None
        self.socket=socket
        self.status=0;
        self.user=user;
        self.username='h6sidhu'
        self.apikey='59d78d873277b643e665cea3a0139230'

    def run(self, timeout):
        def target():
          try:
            self.process = subprocess.Popen(self.cmd, shell=True)
            a=self.process.communicate()
            if os.path.exists(self.user+"/foo.mp4"):
              VID=self.user+str(random.random())[2:]
              conn = cloudfiles.get_connection(self.username, self.apikey)
              container=conn.get_container("videos")
              mp4obj=container.create_object(VID+".mp4")
              mp4obj.load_from_filename(self.user+"/foo.mp4")
              URI=mp4obj.public_streaming_uri()
              response = requests.get("http://bpbhangra.herokuapp.com/api/1/"+self.user+"/"+VID+"/"+"\""+URI+"\"")
              pdb.set_trace()
              shutil.rmtree(self.user)
              self.status=0;
            else:
              self.status=1;
          except Exception:
            self.status=1;

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()
            self.socket.sendMessage("1",False)
        else:
          if self.status==1:
            self.socket.sendMessage("1",False)
          else:
            self.socket.sendMessage("0",False)
        print self.process.returncode
 
class EchoServerProtocol(WebSocketServerProtocol):

  def onMessage(self, msg, binary):
    jsonmsg=simplejson.loads(msg)
    userID=str(jsonmsg["user"])
    if os.path.exists(userID):
      shutil.rmtree(userID)
    os.makedirs(userID)
    for x in range(1, 375):
      fileframe=str(x)
      output=open(userID+"/"+fileframe.zfill(5)+".jpg","wb")
      output.write(base64.b64decode(jsonmsg[str(x)]))
      output.close()
    command=Command(self,userID)
    command.run(timeout=9000)

if __name__ == '__main__': 	
   print "starting"
   factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
   factory.protocol = EchoServerProtocol
   listenWS(factory)   
   reactor.run()





   #command = Command("echo 'Process started'; sleep 2; echo 'Process finished'")
#command.run(timeout=3)
#command.run(timeout=1)
