#!/bin/bash
export DISPLAY=:0
REDIS_CLI="redis-cli -h 127.0.0.1"
q1="volaq"
q2="volap"
icon=""
previous=""
clip=""
xclip -i <<< "$clip"
produce () {
if echo "$clip" | grep -qe "^https://volafile.org/get"; then
	echo "LPUSH $q1 \"$clip\"" | $REDIS_CLI
    	_fi=$(echo "$clip" | cut -d "/" -f 6)
    	notify-send -i "$icon" "Queueing $_fi"
	echo "Queueing $_fi"
fi
}

check () {
if ! [ "$clip" == "$previous" ]; then
produce
fi
}		
while true; do
  clip=$(xclip -o)
  check
  previous="$clip"
  sleep 3
  done
