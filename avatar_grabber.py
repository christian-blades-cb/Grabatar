import json, md5, sys
from popen2 import popen2
from urllib2 import urlopen, HTTPError
from os import mkdir, path

CMD = 'git log --pretty="{\\\"email\\\":\\\"%ae\\\",\\\"username\\\":\\\"%an\\\"}" | sort | uniq'
IMAGE_SIZE = 90
GRAVATAR_PATTERN = 'http://www.gravatar.com/avatar/{0}?d=404&s={1}'
AVATAR_PATH = path.join('.', 'avatars')

def download_gravatar(user):
	avatar = md5.new(user["email"].lower()).hexdigest()
	url = GRAVATAR_PATTERN.format(avatar, IMAGE_SIZE)
	
	try:
		req = urlopen(url)
		image_filename = "{0}.png".format(user["username"])
		image_path = path.join(AVATAR_PATH, image_filename)
		image_out = open(image_path, 'wb')
		image_out.write(req.fp.read())
		image_out.close()
	except Exception, e:
		if e.code == 404:
			return False
		else:
			raise e
	return True

pipe_in, pipe_out = popen2(CMD)
userlist = (json.loads(x) for x in pipe_in)

if not path.exists(AVATAR_PATH):
	mkdir(AVATAR_PATH)

progress = []

for user in userlist:
	sys.stdout.write("\r[ {0} ] - {1}".format("".join(['.' if x else 'x' for x in progress]), user["username"] + (" " * 10)))
	sys.stdout.flush()
	progress.append(download_gravatar(user))

sys.stdout.write("\r[ {0} ] - {1}\n".format("".join(['.' if x else 'x' for x in progress]), "done." + (" " * 10)))
sys.stdout.flush()