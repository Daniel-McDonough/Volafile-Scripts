#!/bin/env bash
OIFS="$IFS"
IFS=$'\n'


list=$(find . -type f  ! -name '*.srt'  ! -name '*.nfo')
#echo "$list"
#echo "list above"
for i in $list; do
#	echo "$i"
	files=$(echo -e "$list" | grep "$i")
        count=$(echo -e "$files" | wc -l)
	if [[ $count > 1 ]]; then
		echo "multiple entries: $count"
		echo "$files"
		sizes=$(for r in $files; do du "$r"; done)
		#echo "$sizes" | sort -k1 -n
		keep=$(echo "$sizes" | sort -k1 -n | tail -n1)
                echo "Keeping:"
		keepFile=$(echo "$keep" | cut -f1 --complement)
		echo "$keepFile"
		echo "New file name"
		newName=$(echo "$keepFile" | sed "s/\.[0-9]$//g")
		echo "$newName"
		mv "$keepFile" "$newName"
		rm "$newName".*
		#| grep -oe "^.*[^ ]./"
	fi
#	echo "---------------"
done

IFS="$OIFS"
