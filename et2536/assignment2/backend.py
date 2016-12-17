#!/usr/bin/python
 # modules needed
import MySQLdb as db
import os
from multiprocessing import Process
import commands
import netsnmp
import sys
import re
import os
#retrieve conig file data
config=open('../db.conf','r')
A=config.read()
host=re.search(r'\s*\$host\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
username=re.search(r'\s*\$username\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]                                
password=re.search(r'\s*\$password\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
databasename=re.search(r'\s*\$database\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
port=re.search(r'\s*\$port\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
def HTTP(ID,IP,Port): #Monitors using http
 var=commands.getoutput("lynx -dump http://{0}:{1}/server-status | grep \"CPU Usage\" | awk '{{if (NR==1) {{print $3,$4}}else {{print $1,$4,$7}}}}' | tr -d 'u' |tr -d 's' | awk '{{if (NR==1) {{print $1+$2}} else {{print}}}}' ORS=' '".format(IP,Port))
 print "here is CPU",var 
 array=[]
 for word in var.split():
  array.append(word)
 var2=commands.getoutput("lynx -dump http://{0}:{1}/server-status?auto | grep \"ReqPerSec:\|BytesPerSec:\|BytesPerReq:\" | awk '{{print $2}}'".format(IP,Port)) #average cpu usage will be retrieved, to avoid this 2 request are sent
 for word in var2.split():
  array.append(word)
 if len(array)==4:
  print array #rrd condition
  l=os.system('rrdtool update {0}.rrd N:{1}:{2}:{3}:{4}'.format(ID,array[0],array[1],array[2],array[3]))
  if l!=0:
   os.system('rrdtool create  {0}.rrd --step 60  DS:CPUusage:GAUGE:120:U:U DS:reqpersec:GAUGE:120:U:U DS:bytespersec:GAUGE:120:U:U DS:bytesperreq:GAUGE:120:U:U RRA:AVERAGE:0.5:1:1440 '.format(ID))
   os.system('rrdtool update {0}.rrd N:{1}:{2}:{3}:{4} '.format(ID,array[0],array[1],array[2],array[3]))
 print ID,IP,array[0],array[1],array[2],array[3]
def DEVICE(ID,IP,Community,interface,port): #snmp device monitoring here
 Ain=[]
 Aout=[]
 for k in interface:
  Ain.append(netsnmp.Varbind('.1.3.6.1.2.1.2.2.1.10.'+k))
  Aout.append(netsnmp.Varbind('.1.3.6.1.2.1.2.2.1.16.'+k))
 print "A in is ",Ain
 print "Aout is",Aout
 #oid_in=netsnmp.Varbind(Ain)
 #oid_out=netsnmp.Varbind(Aout)
 ins=netsnmp.VarList(*Ain)
 outs=netsnmp.VarList(*Aout)
 IP=IP+":"+str(port)
 sess=netsnmp.Session(Version = 1, DestHost="%s" %IP, Community="%s" %Community)
 #inbytes=netsnmp.snmpwalk(oid_in, Version = 1, DestHost="%s" %IP, Community="%s" %Community )
 #outbytes=netsnmp.snmpwalk(oid_out,Version=1,DestHost="%s" %IP,Community="%s" %Community)
 inbytes=sess.get(ins)
 outbytes=sess.get(outs)
 print "inbytes",inbytes
 print "outbytes",outbytes
 totalin=0
 totalout=0
 rrdcreatestring=""
 rrdcreatestringout=""
 if len(inbytes)!=0:
  for i,j in zip(inbytes,outbytes):
   totalin=totalin+int(i)
   totalout=totalout+int(j)
  AggregateIN=int(totalin)
  AggregateOUT=int(totalout)
  for i in range(0,len(inbytes)):
   rrdcreatestring=rrdcreatestring+"DS:inbytes"+ins[i].iid+":COUNTER:120:U:U "
  for i in range(0,len(outbytes)):
   rrdcreatestringout=rrdcreatestringout+"DS:outbytes"+outs[i].iid+":COUNTER:120:U:U "
  inbyte=":".join(inbytes)
  outbyte=":".join(outbytes)
  print ID,IP,inbyte,outbyte,AggregateIN,AggregateOUT,rrdcreatestring
  l=os.system('rrdtool update {0}.rrd N:{1}:{2}:{3}:{4}'.format(ID,inbyte,outbyte,AggregateIN,AggregateOUT))
  if l!=0: #rrd condition 
   os.system('rrdtool create  {0}.rrd --step 60  {1} {2} DS:AggregateIN:COUNTER:120:U:U DS:AggregateOUT:COUNTER:120:U:U RRA:AVERAGE:0.5:1:1440'.format(ID,rrdcreatestring,rrdcreatestringout))
   os.system('rrdtool update {0}.rrd N:{1}:{2}:{3}:{4}'.format(ID,inbyte,outbyte,AggregateIN,AggregateOUT))
def SNMPSERVER(ID,IP,Community,port): #Apache server snmp monitoring here
 oid=netsnmp.Varbind('.1.3.6.1.4.1.8072.1.3.1.4.1.2.6.97.112.97.99.104.101')
 IP=IP+":"+str(port)
 val=netsnmp.snmpwalk(oid, Version = 1, DestHost="%s" %IP, Community="%s" %Community )
 if len(val)==4:
  l=os.system('rrdtool update {0}.rrd N:{1}:{2}:{3}:{4} '.format(ID,val[0],val[1],val[2],val[3]))
  if l!=0:#rrd condition
   os.system('rrdtool create  {0}.rrd --step 60  DS:CPUusage:GAUGE:120:U:U DS:reqpersec:GAUGE:120:U:U DS:bytespersec:GAUGE:120:U:U DS:bytesperreq:GAUGE:120:U:U RRA:AVERAGE:0.5:1:1440 '.format(ID))
   os.system('rrdtool update {0}.rrd N:{1}:{2}:{3}:{4} '.format(ID,val[0],val[1],val[2],val[3]))
  print ID,IP,val[0],val[1],val[2],val[3]
con = db.connect(host,username,password,databasename,int(port))
cur = con.cursor()
try: #creating table
 cur.execute('''use {0}; CREATE TABLE IF NOT EXISTS `lab3` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `IP` tinytext NOT NULL,
  `Community` tinytext,
  `Name` tinytext NOT NULL,
   `Type` tinytext NOT NULL,
  `Monitor` tinytext NOT NULL,
  `Interfacenumber` text NOT NULL,
 `Port` int(11) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1;'''.format(databasename))
except db.Error:
 pass
cur.close()
cur = con.cursor()
cur.execute('use {0};'.format(databasename))
cur.execute(' SELECT * FROM lab3;')
row=cur.fetchone()
print row
while row is not None: #condition checker here
 print row
 if row[4]=='Server':
  if row[5]=='HTTP':
   print "HTTP code here"
   p=Process(target=HTTP,args=(row[0],row[1],row[7]))
   p.start()
  else:
   r=Process(target=SNMPSERVER,args=(row[0],row[1],row[2],row[7]))
   r.start()
 else:
  print "Snmp device code here" 
  A=row[6].split(",")
  print "A is here",A
  q=Process(target=DEVICE,args=(row[0],row[1],row[2],A,row[7]))
  q.start()
 row=cur.fetchone()
