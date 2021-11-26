#!/bin/bash

: >logfile
while true; do

    echo "------------------" >>logfile
    netstat -tan | grep ":80" | grep "ESTABLISHED" >>logfile
    sleep 0.1

done
