from volapi import Room
import sys

nick = "sepiroth"

ro = sys.argv[1]

with Room(ro, nick) as BEEPi:
    def urls(msg):
        if msg.uploader != nick:
            print(msg.url)
    BEEPi.listen(once=True)
    for f in BEEPi.files:
        urls(f)
