*************************************

               LAB1

*************************************

Part 1:

Prerequisites:
              Intall mrtg using command "sudo apt-get install mrtg"
              Install Linux LAMP Stack (Includes Php , Mysql, Apache ) in one package using command "sudo apt-get install lamp-server^"
              Perl DBI module should be installed
              
Procedure: 
          1)Replace db.conf file with your own db file or change the credentials accordingly.
          2)Use "cd" command to change directory to assignment1 folder.
          3)Run command "sudo perl mrtgconf.pl".
          4)Enter server director (default string to be entered is "/var/www/html")
          5)Open file  "/var/www/mrtg/index.html", using web browser
Part 2:


Prerequisites:
              Install development tools
                 sudo apt-get install libperl-dev
                 sudo apt-get install python-dev
              Install Php5-rrd 
                 sudo apt-get install php5-rrd
              Install php5-gd
                 sudo apt-get install php5-gd
              PS: Dont forget to restart apache2 for every module installed.     
              Install Linux LAMP Stack (Includes Php , Mysql, Apache ) in one package using command "sudo apt-get install lamp-server^"
              Perl DBI, Net::SNMP & RRD::Editor module should be installed
Procedure: 
          1)Replace db.conf file with your own db file or change the credentials accordingly.
          2)Use "cd" command to change directory to assignment1 folder.
          3)Give executable permissions for backend.sh, backend.pl files. 
          4)Set crontab for backend.pl for every five minutes or else you can also use backend.sh which will schedule it using command       		  "sudo ./backend.sh".
          5)Using browser open the appropriate URLs to access the web interface.
          6) Results of comparision are shown in the report.pdf  
          Please See : for setting up crontab, server directory must be given writeable permissions  
          Please See: backend.sh is an optional script only         
