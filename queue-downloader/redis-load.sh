#!/bin/bash
REDIS_CLI="redis-cli -h 127.0.0.1"

while read p; do
	if echo "$p" | grep "https://volafile.org/get"; then
	      	echo "LPUSH volaq \"$p\"" | $REDIS_CLI
	else
		echo "Not a valid vola file"
	fi	
done <$1
