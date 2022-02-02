#!/bin/bash
OIFS="$IFS"
IFS=$'\n'
set -e
search="$1"
key="volaq"
result=$(redis-cli LRANGE $key 0 -1 | grep  "$search")
echo "$result"
echo "Remove listed entries? This will delete them from the key: $key. [y/N]"
read confirm
if [[ $confirm == "y" ]]; then
  echo  "Removing..."
  for i in $result; do redis-cli LREM "$key" 1 "$i"; done
 
else
  echo "Exiting."
fi
IFS="$OIFS"
