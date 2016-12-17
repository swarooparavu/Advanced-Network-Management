*************************************

               assignment2

*************************************

Prerequisites:
              Install Linux LAMP Stack (Includes Php , Mysql, Apache ) in one package using command "sudo apt-get install lamp-server^"
              Perl DBI module should be installed.
              Install Perl NETSNMP module
	      Install rrdtool 
			    sudo apt-get install rrdtool
              Install lynx 
			    sudo apt-get install lynx
              Install rrdtool php 
			    sudo apt-get install php5-rrd
              Install Php5-snmp (sudo apt-get install php5-snmp)
              PS: apache must be restarted after installing modules
              

Procedure: 
          1)Replace db.conf file with your own db file or change the credentials accordingly.
          2)Use "cd" command to change directory to assignment2 folder.
          3)Give executable permissions to backend.pl, backend2.py, backend.sh.
          4)Now run the script backend.sh using command "sudo ./backend.sh" its a daemon ( I suggest leave terminal while its running) We can 		  also send this as a background process.
          5)After running backend.sh , everything what software can do can be used from browser using appropriate URLs.
           
		  
Please see:  THE DEVICES FOR WHICH THE INTERFACE DISCOVERY FAILED WILL NOT BE MONITORED SO NO RRD FILES ARE GENERATED fOR THESE DEVICES          
