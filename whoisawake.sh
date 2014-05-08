#!/bin/sh

COUNTER=1

while [ $COUNTER -lt 254 ]
do
   #change this to whatever subnet
   ping 10.0.0.$COUNTER -c 1 | grep -B 1 '100%'
   COUNTER=$(( $COUNTER + 1 ))
done
