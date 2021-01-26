#!/bin/bash
#
# Usage: wait_and_get_file_content.sh <URL>
#
while true; do
  response=`curl $1 --output event.txt --silent`
  res=$?
  if [ $res -eq 0 ]
  then
    if [ -f event.txt ]; then
      event=`/bin/cat event.txt`
      if [ -n "$event" ]
      then
        echo -n $event
        break
      fi
    fi
  fi
  /bin/sleep 1
done
