#!/bin/sh
while read oid val
 do  
echo $oid,$val >> /var/log/traps_10.log
if [ $oid = "SNMP-COMMUNITY-MIB::snmpTrapAddress.0" ] || [ $oid = "iso.3.6.1.6.3.18.1.3.0" ] ;  #gets paremters from trap received #.1.3.6.1.6.3.18.1.3.0
   then
     vars="$val"
    # echo "wars"
   elif [ "$oid" = "iso.3.6.1.6.3.18.1.4.0" ] || [ "$oid" = "SNMP-COMMUNITY-MIB::snmpTrapCommunity.0" ] ;
   then
    mars="$val"
    elif [ "$oid" = "iso.3.6.1.4.1.41717.10.1" ] || [ "$oid" = "SNMPv2-SMI::enterprises.41717.10.1" ] || [ "$oid" = ".1.3.6.1.4.1.41717.10.1" ] ;
    then 
     hostnam=$val
   elif [ "$oid" = "iso.3.6.1.4.1.41717.10.2" ] || [ "$oid" = "SNMPv2-SMI::enterprises.41717.10.2" ] || [ "$oid" = ".1.3.6.1.4.1.41717.10.2" ] ;
    then 
     lstatus=$val
   fi
done
ltime=$(date +%s)
#exports environmental variable to pythonscript
export vars
export mars
export hostnam
export lstatus
export ltime


/usr/bin/python /home/trapDaemon.py # passes to python script and after that python feeds them into database 
#8341894963
