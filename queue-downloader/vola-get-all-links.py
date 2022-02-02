from volapi import Room
import sys
import redis
from functools import partial

r = redis.StrictRedis(host='localhost', port=6379)
ro = sys.argv[1]
dest = sys.argv[2]
nick = "sepiroth"

def publish(o):
	try:
		r.lpush('volaq',o)

	except Exception as e:
		print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
		print(str(e))
		print(traceback.format_exc())

def dedupe():
	print("i should be doing something")

with Room(ro, nick) as BEEPi:
	def urls(msg,nick,dest):
		if msg.uploader != nick :
	        	o = msg.url + ";" + dest + ro
	        	publish(o)

		#BEEPi.add_listener("file",urls)
	BEEPi.listen(once=True)
	for f in BEEPi.files:
	    urls(f)
