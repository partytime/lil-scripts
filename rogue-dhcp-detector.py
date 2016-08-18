#!/usr/bin/python
import sys
from os import geteuid
from scapy.all import *

#check for root
if geteuid() != 0:
    print "This must be run as root"
    exit(1)

# CONFIGURATION #
"""
Scapy normally makes sure that replies come from the same IP address the stimulus was sent to. But our DHCP packet is sent to the  broadcast address (255.255.255.255) and any answer packet will have the IP address of the replying DHCP server as its source IP address (e.g. 192.168.1.1). Because these IP addresses don't match, we have to disable Scapy's check with conf.checkIPaddr = False before sending the stimulus.
"""
conf.checkIPaddr = False
fam,hw = get_if_raw_hwaddr(conf.iface)

# CRAFTING THE DHCP PACKET #
dhcp_discover_packets = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=hw)/DHCP(options=[("message-type","discover"),"end"])

# SENDING THE PACKET #
ans, unans = srp(dhcp_discover_packets, multi=True, timeout=3)

# GET THE RESULTS #
replyingServers=[]
for result in ans:
    print "\nGot a DHCP offer from", result[1][IP].src, "with MAC address", result[1][Ether].src
    replyingServers.append(result[1][IP].src)

if len(replyingServers) > 1:
    print ("!!!!!!!!!!!!\nWARNING: MORE THAN 1 DHCP SERVER REPLIED TO OUR PACKETS\n!!!!!!!!!!!!")
elif len(replyingServers) < 1:
    print ("Didnt get a reply from anyone....is there a DHCP server on this subnet?")
else:
    print ("\nGot one DHCP reply, looks good!")
