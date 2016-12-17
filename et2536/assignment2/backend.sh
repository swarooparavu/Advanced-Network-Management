#!/bin/bash
/usr/bin/python backend2.py
while true
do
start=`date +%s`
perl backend.pl
end=`date +%s`
runtime=$((end-start))
sleep $((60-runtime))
done

