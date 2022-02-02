#!/bin/bash
OIFS="$IFS"
IFS=$'\n'
touch /tmp/voladownloadstatus
REDIS_CLI="/usr/bin/redis-cli -h 127.0.0.1"
q1="volaq"
q2="volap"
ORIGD=$(pwd)
serviceNum="$1"
storage_location=""
if ! grep -q "$serviceNum" /tmp/voladownloadstatus; then
	echo "${serviceNum}:WAITING" >> /tmp/voladownloadstatus
fi
# redis nil reply
nil=$(echo -n -e '\r\n')

remaining() {
	left=$(df | grep "$storage_location" | awk '{ print $5 }' | tr  -d "%")
	if (( $left > 80 )); then
		  storage="red"
	  else
                  storage="green"
	fi
}

consume() {
	
        # move message to processing queue
        MSG=$(echo "RPOPLPUSH $q1 $q2" | $REDIS_CLI)
	echo "$MSG"
        if [[ -z "$MSG" ]]; then
	    echo "No messages. Waiting."	
        else
	    MSGU=$(echo "$MSG" | cut -f 1 -d ';')
	    MSGR=$(echo "$MSG" | cut -f 2 -d ';')
	    if ! echo "$MSGR" | grep -q "^https"; then
		    mkdir "$MSGR"
		    cd "$MSGR"
	    fi
	    sed -i s/"$serviceNum":WAITING/"$serviceNum":ACTIVE/g  /tmp/voladownloadstatus	
        # processing message
            if wget  --header="Cookie: allow-download=1" --content-disposition "$MSGU"; then
                echo "LREM $q2 1 \"$MSG\"" | $REDIS_CLI >/dev/null
            else
             #Put back if failed
	         echo -e "LPUSH volaf \"$MSG\"" | $REDIS_CLI >/dev/null
		 echo -e "LREM $q2 1 \"$MSG\"" | $REDIS_CLI >/dev/null
#                MSG=$(echo "RPOPLPUSH $q2 $q1" | $REDIS_CLI)
		echo "Message failed. pushing $MSG back"
            fi
	    cd "$ORIGD"
	    sed -i s/"$serviceNum":ACTIVE/"$serviceNum":WAITING/g  /tmp/voladownloadstatus
	fi   
     sleep 1
     # remove message from processing queue
}

while true; do
	if [ -f /tmp/volastop ]; then
		sleep 10
	else
		remaining
		if [[ $storage == "green" ]]; then
			consume	
		else
			echo "Waiting for storage to free up. ${left}%" 
			sleep 20
		fi
	fi
done
IFS="$OIFS"
trap echo '"Putting message back into queue" && echo "LPUSH volaq \"$MSG\"" | $REDIS_CLI >/dev/null && echo "LREM $q2 1 \"$MSG\"" | $REDIS_CLI >/dev/null' SIGINT SIGTERM SIGKILL
