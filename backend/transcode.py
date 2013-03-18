import subprocess

import os, cloudfiles

def transcode(uid, mp3):
	cmd = "avconv -i transcode/img/%(user)s/%05d.jpg -c:v libx264 -i transcode/mp3/%(filename)s.mp3 %(user)s.mp4" 
		% {'user':uid, 'filename':mp3}
	return subprocess.call(cmd)



# import os
# import cloudfiles

username = 'h6sidhu'
apikey = '59d78d873277b643e665cea3a0139230'


# conn = cloudfiles.get_connection(username, apikey)
# container = conn.create_container('api_speed_test3')
# data_list = ('test_data/%s'%x for x in os.listdir('test_data') if x.endswith('.dat'))
# for filename in data_list:
# 	try:
# 		obj = container.create_object(filename)
# 		obj.load_from_filename(filename)
# 	except cloudfiles.errors.ResponseError, err:
# 		print err
# print len(container.list_objects())


import sys
import os
import httplib
import time

from cf_auth import username, apikey

container_name = sys.argv[1]

use_service_net = os.environ.get('USECFSERVICENET', False)

# auth
conn = httplib.HTTPSConnection('auth.api.rackspacecloud.com')
conn.request('GET', '/auth',
             headers={'x-auth-user': username, 'x-auth-key': apikey})
resp = conn.getresponse()
auth_token = resp.getheader('x-auth-token')
url = resp.getheader('x-storage-url')
conn.close()
# send data
send_headers = {'X-Auth-Token': auth_token, 'Content-Type': 'text/plain'}
container_path = '/' + '/'.join(url.split('/')[3:]) + '/' + container_name
storage_url = url.split('/')[2]
if use_service_net:
    storage_url = 'snet-' + storage_url
conn = httplib.HTTPSConnection(storage_url)
conn.request('PUT', container_path, headers=send_headers)
conn.getresponse().read()
data_list = ('test_data/%s' % x for x in os.listdir('test_data')
             if x.endswith('.dat'))


for filename in data_list:
    start = time.time()
    with open(filename, 'rb') as f:
        conn.request('PUT', container_path + '/' + filename, body=f,
             headers=send_headers)
    resp = conn.getresponse()
    resp.read()
    if resp.status >= 300:
        print resp.status, resp.reason, container_path + '/' + filename
    print '%s uploaded in %.4f seconds' % (filename, (time.time()-start))
conn.close()


