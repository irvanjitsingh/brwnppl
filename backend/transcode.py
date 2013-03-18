import subprocess

def transcode(uid, mp3):
	cmd = "avconv -i transcode/img/%(user)s/%05d.jpg -c:v libx264 -i transcode/mp3/%(filename)s.mp3 %(user)s.mp4" 
		% {'user':uid, 'filename':mp3}
	return subprocess.call(cmd)