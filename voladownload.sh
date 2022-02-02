#!/bin/bash

#while read p; do   
#  proxychain --conf  wget --header="Referer:https://volafile.org/r/${1}" --header="Cookie: allow-download=1" "$p"
# done <$1
args=''
IFS=$'\r\n' GLOBIGNORE='*' command eval  'proxies=($(find ~/proxychains/confs/ -mindepth 1 -maxdepth 1 -type f))'
IFS=$'\r\n' GLOBIGNORE='*' command eval  'urls=($(cat "$1"))'
for ((i=0;i<${#urls[@]};++i)); do
#	      "${urls[i]}" "${proxies[i]}"
	      args="${args}\nsleep 60; proxychains -f \"${proxies[i]}\"  wget  --header=\"Cookie: allow-download=1\" \"${urls[i]}\" "
done 
echo -e "$args" | parallel --verbose -j3
