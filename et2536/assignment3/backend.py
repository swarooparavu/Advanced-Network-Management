#!/usr/bin/python
import MySQLdb as db
import commands
import time #different cursor or connection concept
import os # creates php file
import re
config=open('../db.conf','r')
A=config.read()
host=re.search(r'\s*\$host\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
username=re.search(r'\s*\$username\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]                                      # change this if needed
password=re.search(r'\s*\$password\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
databasename=re.search(r'\s*\$database\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
port=re.search(r'\s*\$port\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
f=open('index.php','w')
f.write('''<html><meta http-equiv="refresh" content="10">''')
f.write("<?php $con=mysqli_connect(\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\") ;".format(host,username,password,databasename,port))
f.write('''$result = mysqli_query($con,"SELECT IP,Hostname,Presentreportedtime,Presentreportedstatus FROM lab4"); 
echo  "<a href=\\"addmom.php\\">Edit Manager of managers</a>";
echo "<table border='10'>
<tr>
<th>IP</th>
<th>FQDN</th>
<th>Current UNIX reported time</th>
<th>Current Status reported</th>
</tr>";
while($row = mysqli_fetch_array($result))
{echo "<tr>";
  echo "<td>" . $row['IP'] . "</td>";
  echo "<td>" . $row['Hostname'] . "</td>";
    echo "<td>" . $row['Presentreportedtime'] . "</td>";
  echo "<td>" . $row['Presentreportedstatus'] . "</td>"; ##change
 echo "</tr>";
  }echo "</table>";
?>
<p>0:OK</p>
<p>1:PROBLEM</p>
<p>2:DANGER</p>
<p>3:FAIL</p>
<p>Every  min page updates </p>
</html>
''')
f.close()
f=open('addmom.php','w')
f.write('''<html><meta http-equiv="refresh" content="10">''')
f.write("<?php $con=mysqli_connect(\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\") ;".format(host,username,password,databasename,port))
f.write('''echo "<form name=\\"form1\\" method=\\"post\\" action=\\"\\">
Device credentials to which trap must be sent:<br>
IP: <input type=\\"text\\" name=\\"IP\\" id=\\"IP\\"><br>
Community: <input type=\\"text\\" name=\\"Community\\"><br>
Port: <input type=\\"text\\" name=\\"port\\"><br>
<input type=\\"submit\\" value=\\"Update device\\">
</form>";
if($_SERVER['REQUEST_METHOD'] == "POST"){
$table="CREATE TABLE IF NOT EXISTS `MoM` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
    `IP` tinytext NOT NULL,
   `Community` tinytext NOT NULL,
   `Port` int(11) NOT NULL,
 PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1;";
mysqli_query($con, $table);
$IP=$_POST['IP'];
$Community=$_POST['Community'];
$Port=$_POST['port'];
$entries=mysqli_query($con,"SELECT Count(*) FROM MoM");
$elements=mysqli_fetch_array($entries)[0];
if($elements==0)
{
$sql="insert into MoM (IP,Community,Port) values ('$IP','$Community','$Port')";
mysqli_query($con, $sql);
echo "Traps will be sent to device mentioned";
}
elseif ($elements==1)
{
$mql="update MoM set IP='$IP',Community='$Community',Port=$Port where ID=1";
mysqli_query($con, $mql);
echo "Traps will be sent to device mentioned";
}
}
?>
''')
f.close()




