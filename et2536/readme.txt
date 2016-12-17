*******************************
       Common for all labs

*******************************
All lab assignments are designed to run on Ubuntu 14.04. They assume a working internet connection.

Prerequisites :
              Install perl & python development tools
		        sudo apt-get install libperl-dev
			sudo apt-get install python-setuptools
			sudo apt-get install python-dev
	      Install SNMP Daemon
	                sudo apt-get install snmpd  
              Install Linux LAMP Stack (Includes Php , Mysql, Apache ) in one package using command "sudo apt-get install lamp-server^"

Caution
Do not use any two assignments executions at any point of time as they may interfere giving non desirous results.
Only to provide ease dynamic content is generated from scripts not a conventional way of doing it.(For the sake of only one config file).
Almost all Labs are  periodic, please have patience while the changes are reflected(at least wait for the 2 periods).
          		
                  
Update packages
               "sudo apt-get update"
Upgrade packages
               "sudo apt-get upgrade"
			   
Procedure
          1)Extract tar package using command "tar -xvf et2536-nsku14.tar.gz" into DOCUMENT ROOT apache.
          2)Open db.conf file and fill in the database credentials.
	  3)DONT NOT MOVE "db.conf" FILE INTO ANY OTHER DIRECTORIES.
	  4)Each assignment is provided with a readme.txt file, which gives instruction towards execution.
          5)Each assignment gives index.html or index.php as the access point.       

Although there are instructions for each and every assignment
The user with following qualities will have ease. 
User expectations:
•User is expected to have basic kowledge of ubuntu and its directory structure
•Basic commands in terminal.eg:- (cd,cp,mv,executing scripts,giving appropriate permissions)
•Theoretical knowledge of SNMP touch with netsnmp tools.(snmpget,snmpwalk,snmptrap etc)
•Installing packages from sources and repositories.
