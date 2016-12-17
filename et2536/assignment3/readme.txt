***************************************

               assignment3  
 
***************************************
Prerequisites:
              Install MYSQLdb module for python  
			    sudo apt-get install python-mysqldb
              Install Linux LAMP Stack (Includes Php , Mysql, Apache ) in one package using command "sudo apt-get install lamp-server^"
              Install SNMPD
			    sudo apt-get install snmpd
			  Install Development tools python & perl
			   sudo apt-get install libperl-dev
			   sudo apt-get install python-setuptools
			  Install SNMP tool kit
			   sudo apt-get install snmp
			   
Procedure:
         1)In terminal type the following Command "sudo gedit /etc/default/snmpd"
           change the following "TRAPDRUN=no" to "TRAPDRUN=yes",save file.
         2) Add these lines to snmptrapd.conf file in /etc/snmp 
            "traphandle .1.3.6.1.4.1.41717.10.*  /home/trapDaemon.sh
             disableAuthorization yes
             snmpTrapdAddr udp:localhost:50162
             donotlogtraps false
             logOption f /var/log/traps.log"
             Don't include quotes
                   OR
            Replace snmptrapd.conf  file in /etc/snmp/ with snmptrapd.conf from assignment3 folder.
         PS: dont not change the paths in above lines
         3)Restart snmpd using "service snmpd restart". This will also restart snmptrapd. 
         4)Check using "service snmpd status". which gives snmpd as running and snmptrapd as running
         5)Fill in the database credentials in db.conf file.
         6) Give executable permission to scrits "backend.py","backend.sh".
         7)Run backend.sh using command "sudo ./backend.sh", change in server directory can be done by modifying ServerDirectory variable in 		   backend.py.
         8) All traps are logged in "/var/log/traps.log"
         9)Fail/danger traps will be sent to another manager configurable from Web page mentioned above please set the MoM details before 		 continuing. 
         10)Trap must have following format
           snmptrap -v 1 -c public <IP of assignment3 Running pc>:50162 .1.3.6.1.4.1.41717.10 <IP address from which trap is sent> 6 247 	    '' .1.3.6.1.4.1.41717.10.1 s <FQDN> .1.3.6.1.4.1.41717.10.2 i <Status message>
         11)Current status can be seen from web browser typing appropriate URLS.
      

