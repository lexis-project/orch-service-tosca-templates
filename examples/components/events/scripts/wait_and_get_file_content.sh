#!/bin/bash

while true; do
  response=`curl $FILE_URL --output event.txt --silent`
  res=$?
  if [ $res -eq 0 ]
  then
    event=`/bin/cat event.txt`
    if [ -n "$event" ]
    then
      echo $event
      break
    fi
  fi
  /bin/sleep 1
done
