#!/bin/bash

#quick script to block all flames

BLOCK=$(cat twods.txt)
LIST="flamelist"

/sbin/iptables -N $LIST

for ip in $BLOCK
do 
    /sbin/iptables -A $LIST -s $ip -j DROP
done

/sbin/iptables -I INPUT -j $LIST
/sbin/iptables -I OUTPUT -j $LIST
/sbin/iptables -I FORWARD -j $LIST

