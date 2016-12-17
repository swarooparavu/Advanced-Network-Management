#!/bin/bash
#schedules backend.pl
while true
do
start=`date +%s`
perl backend.pl
end=`date +%s`
runtime=$((end-start))
sleep $((300-runtime))
done

