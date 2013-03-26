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
        self.status=0
        self.user=user
        self.username='h6sidhu'
        self.apikey='59d78d873277b643e665cea3a0139230'
        self.request={}
        self.url="https://bpbhangra.herokuapp.com/api/1/videos/add/"
        self.cloudcontainer=None
        self.cloudcontainer2=None

    def run(self, timeout):
        def target():
          try:
            self.process = subprocess.Popen(self.cmd, shell=True)
            a=self.process.communicate()
            if os.path.exists(self.user+"/foo.mp4"):
              VID=self.user+str(random.random())[8:]
              conn = cloudfiles.get_connection(self.username, self.apikey)
              container=conn.get_container("videos")
              self.cloudcontainer=container.create_object(VID+".mp4")
              self.cloudcontainer.load_from_filename(self.user+"/foo.mp4")
              meta_data['mime-type'] = "video/mp4"
              pdb.set_trace()
              self.cloudcontainer.metadata=meta_data
              self.cloudcontainer.sync_metadata()
              URI=self.cloudcontainer.public_streaming_uri()
              self.cloudcontainer2=container.create_object(VID+".jpg")
              self.cloudcontainer2.load_from_filename(self.user+"/00150.jpg")
              Thumbnail=self.cloudcontainer2.public_uri()
              jsonmsg = {'uid': self.user, 'vid': VID, 'uri_v': URI, 'uri_i':Thumbnail}
              response = requests.post(self.url, data=simplejson.dumps(jsonmsg))
              jsonresponse=simplejson.loads(response.text)
              if jsonresponse["response"]!="success":
                self.status=1
                self.cloudcontainer.purge_from_cdn()
                self.cloudcontainer2.purge_from_cdn()
              else:
                self.status=0
            else:
              self.status=1
            shutil.rmtree(self.user)
          except Exception:
            self.status=1

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
