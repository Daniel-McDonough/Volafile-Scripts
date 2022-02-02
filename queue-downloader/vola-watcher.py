from volapi import Room
import sys
import redis
from functools import partial

r = redis.StrictRedis(host='localhost', port=6379)
nick = "Sepiroth"
dest = /temp
ro =sys.argv[1]
def debug_handler(_, frame):
    import code
    import traceback

    def printall():
        print("\n*** STACKTRACE - START ***\n", file=sys.stderr)
        code = []
        for threadid, stack in sys._current_frames().items():
            code.append("\n# ThreadID: %s" % threadid)
            for filename, lineno, name, line in traceback.extract_stack(stack):
                code.append('File: "%s", line %d, in %s' % (filename,
                                                            lineno, name))
                if line:
                    code.append("  %s" % (line.strip()))

        for line in code:
            print(line, file=sys.stderr)
        print("\n*** STACKTRACE - END ***\n", file=sys.stderr)

    def _exit(num=1):
        sys.exit(num)

    env = {
        "_frame": frame,
        "printall": printall,
        "exit": _exit
        }
    env.update(frame.f_globals)
    env.update(frame.f_locals)

    shell = code.InteractiveConsole(env)
    message = "Signal received : entering python shell.\nTraceback:\n"
    message += ''.join(traceback.format_stack(frame))
    shell.interact(message)


import signal
signal.signal(signal.SIGUSR2, debug_handler)

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
        print(msg)
        if msg.uploader != nick:
            o = msg.url + ";" + dest + ro
            print("Adding" + o)
            publish(o)
    BEEPi.add_listener("file",urls)
    BEEPi.listen()
