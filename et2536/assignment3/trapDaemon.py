#!/usr/bin/python
import os
import MySQLdb as db 
import re
config=open('/home/db.conf','r')
A=config.read()
host=re.search(r'\s*\$host\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
ServerDirectory="/var/www/html/"                                      # change this if needed
username=re.search(r'\s*\$username\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
password=re.search(r'\s*\$password\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
databasename=re.search(r'\s*\$database\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
port=re.search(r'\s*\$port\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
ip=os.environ['vars']  #receives parameters from trapDaemon.sh
community=os.environ['mars']
hostname=os.environ['hostnam']
laststatus=os.environ['lstatus']
lasttime=os.environ['ltime']
con = db.connect(host,username,password,databasename,int(port)) 
cur = con.cursor()
try: # Creates database with necessary tables with respective colomn 
 cur.execute('''use {0}; CREATE TABLE IF NOT EXISTS `lab4` (
   `IP` tinytext NOT NULL,
   `Hostname` tinytext NOT NULL,
   `Presentreportedtime` int(11) NOT NULL,
  `Presentreportedstatus` int(11) NOT NULL,
   `Previousstatus` int(11) NOT NULL,
    `Previousstatustime` int(11) NOT NULL   
  
) ENGINE=MyISAM  DEFAULT CHARSET=latin1;'''.format(databasename))
except db.Error:
 pass
#starts here
cur = con.cursor()
cur.execute("use {0};".format(databasename))
cur.execute("SELECT COUNT(*) FROM lab4 where Hostname='{0}';".format(hostname))
temp=cur.fetchone()
cur.close()
if temp[0]==1:
 cur = con.cursor()
 cur.execute("use {0};update lab4 set  Previousstatus=Presentreportedstatus, Previousstatustime=Presentreportedtime, Presentreportedtime='{1}', Presentreportedstatus='{2}'  where Hostname='{3}' ;".format(databasename,lasttime,laststatus,hostname))
 cur.close()
else:
 cur = con.cursor()
 cur.execute("use {0};insert into lab4 (IP,Hostname,Presentreportedtime,Presentreportedstatus,Previousstatus,Previousstatustime) values ('{1}','{2}','{3}','{4}','4','0')".format(databasename,ip,hostname,lasttime,laststatus))
 cur.close()
if laststatus=='3':
 cur= con.cursor()
 cur.execute("SELECT Previousstatus,Previousstatustime from lab4 where Hostname='{0}';".format(hostname))
 failrow=cur.fetchone()
 print "hello"
 cur2 = con.cursor()
 cur2.execute("select IP,Community,Port from MoM where ID=1")
 MoM=cur2.fetchone()
 cur2.close()
 while failrow is not None:
  if failrow[0]!=4:
   print 'snmptrap -v 1 -c {0} {1}:{2} .1.3.6.1.4.1.41717.10 {3}  6 247 \'\'  .1.3.6.1.4.1.41717.20.1 s {4} .1.3.6.1.4.1.41717.20.2 i {5}  .1.3.6.1.4.1.41717.20.3 i {6}  .1.3.6.1.4.1.41717.20.4 i {7} '.format(MoM[1],MoM[0],MoM[2],ip,hostname,lasttime,failrow[0],failrow[1])
   os.system('snmptrap -v 1 -c {0} {1}:{2} .1.3.6.1.4.1.41717.10 {3}  6 247 \'\'  .1.3.6.1.4.1.41717.20.1 s {4} .1.3.6.1.4.1.41717.20.2 i {5}  .1.3.6.1.4.1.41717.20.3 i {6}  .1.3.6.1.4.1.41717.20.4 i {7} '.format(MoM[1],MoM[0],MoM[2],ip,hostname,lasttime,failrow[0],failrow[1]))
  else:
   os.system('snmptrap -v 1 -c {0} {1}:{2} .1.3.6.1.4.1.41717.10 {3}  6 247 \'\'  .1.3.6.1.4.1.41717.20.1 s {4} .1.3.6.1.4.1.41717.20.2 i {5} '.format(MoM[1],MoM[0],MoM[2],ip,hostname,lasttime))
  failrow=cur.fetchone()
  cur.close()
if laststatus=='2':
 cur= con.cursor()
 cur.execute("SELECT Count(*) FROM lab4 where Presentreportedstatus=2")
 COUNT=cur.fetchone()
 if COUNT[0]>1:
  cur= con.cursor()
  cur.execute("SELECT IP,Hostname,Presentreportedtime,Previousstatus,Previousstatustime FROM lab4 where Presentreportedstatus=2")
  Danger=cur.fetchone()
  print Danger
  cur2 = con.cursor()
  cur2.execute("select IP,Community,Port from MoM where ID=1")
  MoM=cur2.fetchone()
  i=1
  part1=''
  party="snmptrap -v 1 -c "+str(MoM[1])+" "+str(MoM[0])+":"+str(MoM[2])+" .1.3.6.1.4.1.41717.30 "+str(Danger[0])+" 6 247 '' "
  while Danger is not None: # already danger devices are bound
   part1=part1+".1.3.6.1.4.1.41717.30."+str(i)+" s \""+str(Danger[1])+"\""
   i=i+1
   part1=part1+" .1.3.6.1.4.1.41717.30."+str(i)+" i "+str(Danger[2])+" ";
   i=i+1
   if Danger[3]!=4:
    part1=part1+" .1.3.6.1.4.1.41717.30."+str(i)+" i "+str(Danger[3]);
    i=i+1
    part1=part1+" .1.3.6.1.4.1.41717.30."+str(i)+" i "+str(Danger[4])+" "; 
    i=i+1
   else:
    i=i+2
   Danger=cur.fetchone()
  part=party+part1
  print part
  os.system(part)


