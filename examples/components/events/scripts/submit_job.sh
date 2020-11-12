#!/bin/bash

if [ -z "$STDERR_FILE" ]
then
  STDERR_FILE=/tmp/stderr_event_example
fi
if [ -z "$STDOUT_FILE" ]
then
  STDOUT_FILE=/tmp/stdout_event_example
fi

nohup /bin/bash $script_to_execute  < /dev/null 2> $STDERR_FILE > $STDOUT_FILE &
TOSCA_JOB_ID=$!
export TOSCA_JOB_ID
SUBMIT_DATE_EPOCH=`date +%s`
export SUBMIT_DATE_EPOCH
