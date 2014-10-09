#!/bin/bash

# ips.csv is a file with 1 IP per line
sshuser=ubuntu
keypath=~/.ssh/privkey.pem

while read line
do
    ip=$line
    echo $ip
    ping -c 1 $ip
    if [ $? != 0 ] ; then
        echo "problem connecting to" $ip
        exit 1
    fi
    ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeychecking=no -n -i $keypath $sshuser@$ip 'cd smapbenchmark ; cat config.ini'
done < ips.csv
