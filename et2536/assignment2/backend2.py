#!/usr/bin/python
#PHP files 
import sys
import os
import re
config=open('../db.conf','r')
A=config.read()
host=re.search(r'\s*\$host\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
username=re.search(r'\s*\$username\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]                                  
password=re.search(r'\s*\$password\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
databasename=re.search(r'\s*\$database\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
port=re.search(r'\s*\$port\s*=\s*\"(.*)\"\s*;',A).groups(0)[0]
f=open('add.html','w')
f.write('''<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>LAB 2 Add page</title>
</head>
<body>
<p><a href="addserver.html">Add a New Apache server to Monitoring list</a></p>
<p><a href="addndevice.html">Add a Network Device </a></p>''')
f.close()
f=open('index.html','w')
f.write('''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>LAB#2</title>
</head>
<body>
<p><strong>Lab-3 Web based front end</strong></p>
<p><a href="add.html">Add a New Server/Device to Monitor.</a></p>
<p><a href="remove.php">Remove Device/Server from Monitor.</a></p>
<p><a href="monitor.php">Clickhere for any monitering info.</a></p>
<p><a href="comparision.php">Clickhere for any comparing  info.</a></p>
<hr />
</body>
</html>''')
f.close()
f=open('addserver.html','w')
f.write('''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>LAB 2 Server page</title>
</head>
<body>
<p><a href="addserver.php/?Type=Server&Monitor=HTTP">Monitor Apache Server using HTTP </a></p>
Enable Server-status on the apache server 
 ''')
f.close()
f=open('addserver.php','w')
f.write('''<html>''')
f.write("<?php $con=mysqli_connect(\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\") ;".format(host,username,password,databasename,port))
f.write('''echo "<form name=\\"form1\\" method=\\"post\\" action=\\"\\">
Apache Server's Specifications:<br>
IP: <input type=\\"text\\" name=\\"IP\\" id=\\"IP\\"><br>
Name: <input type=\\"text\\" name=\\"Name\\"><br>
Port: <input type=\\"text\\" name=\\"port\\"><br>
<input type=\\"submit\\" value=\\"Add to Monitoring list\\">
</form>";
if($_SERVER['REQUEST_METHOD'] == "POST"){
if (!empty($_POST['IP'])){
mysqli_query($con,"INSERT into lab3 (IP,Name,Port,Type,Monitor)  values ( '".$_POST['IP']."','".$_POST['Name']."','".$_POST['port']."' , '".$_GET['Type']."','".$_GET['Monitor']."')");

$result = mysqli_query($con,"SELECT * FROM lab3");
echo "<table border='10'>
<tr>
<th> ID </th>
<th>IP</th> 
<th>Community</th>
<th> Name </th>
<th> Port </th>
<th> Type </th>
<th> Monitor </th>
<th> Interfacenumber </th>
</tr>";
while($row = mysqli_fetch_array($result))
{echo "<tr>";
  echo "<td>" . $row['ID'] . "</td>";
  echo "<td>" . $row['IP'] . "</td>";
echo "<td>" . $row['Community'] . "</td>";
echo "<td>" . $row['Name'] . "</td>";
echo "<td>" . $row['Port'] . "</td>";
echo "<td>" . $row['Type'] . "</td>";
echo "<td>" . $row['Monitor'] . "</td>";
echo "<td>" . $row['Interfacenumber'] . "</td>";
  echo "</tr>";
}
echo "</table>";
mysqli_close($con);
}
else
{ echo "wrong choice"; }
}

?> 

</html>''')
f.close()
f=open('adddevice.php','w')
f.write('''<html>''')
f.write("<?php $con=mysqli_connect(\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\") ;".format(host,username,password,databasename,port))
f.write('''echo "<form name=\\"form1\\" method=\\"post\\" action=\\"\\">
Apache Server's Specifications:<br>
IP: <input type=\\"text\\" name=\\"IP\\" id=\\"IP\\"><br>
Community: <input type=\\"text\\" name=\\"Community\\"><br>
Name: <input type=\\"text\\" name=\\"Name\\"><br>
Port: <input type=\\"text\\" name=\\"port\\"><br>
<input type=\\"submit\\" value=\\"Add to Monitoring list\\">
</form>";
if($_SERVER['REQUEST_METHOD'] == "POST"){
mysqli_query($con,"INSERT into lab3 (IP,Community,Name,Port,Type,Monitor)  values ( '".$_POST['IP']."','".$_POST['Community']."' ,'".$_POST['Name']."','".$_POST['port']."' , '".$_GET['Type']."','".$_GET['Monitor']."')");
$result = mysqli_query($con,"SELECT * FROM lab3");
echo "<table border='10'>
<tr>
<th> ID </th>
<th>IP</th> 
<th>Community</th>
<th> Name </th>
<th> Port </th>
<th> Type </th>
<th> Monitor </th>
<th> Interfacenumber </th>
</tr>";
while($row = mysqli_fetch_array($result))
{echo "<tr>";
  echo "<td>" . $row['ID'] . "</td>";
  echo "<td>" . $row['IP'] . "</td>";
echo "<td>" . $row['Community'] . "</td>";
echo "<td>" . $row['Name'] . "</td>";
echo "<td>" . $row['Port'] . "</td>";
echo "<td>" . $row['Type'] . "</td>";
echo "<td>" . $row['Monitor'] . "</td>";
echo "<td>" . $row['Interfacenumber'] . "</td>";
  echo "</tr>";
}
echo "</table>";
mysqli_close($con);
echo "<p><a href='index.html'>Back to Lab2 Main Page</a></p>";
}
?> 
</html>''')
f.close()
f=open('interfacedisc.php','w')
f.write('''<html>''')
f.write("<?php $con=mysqli_connect(\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\") ;".format(host,username,password,databasename,port))
f.write('''echo "SELECT intefaces to be monitored";
echo "<br> If at all the inface discovery failed then device will not be added to table</br>";
snmp_set_quick_print(TRUE);
$interface = snmpwalk($_GET['IP'].":".$_GET['port'], $_GET['Community'], '1.3.6.1.2.1.2.2.1.1');
echo "<form name=\\"form1\\" method=\\"post\\" action=\\"\\" >";
foreach ($interface as $val) {
echo "<br> Interface$val <input type=\\"checkbox\\" name=\\"par[]\\" id=\\"color\\" value=\\"$val\\"></br>";    
}
echo "<input type=\\"submit\\" value=\\"Add to Monitoring table\\">";
if($_SERVER['REQUEST_METHOD'] == "POST"){
$po=$_POST["par"];
$interfacenumber=implode (",", $po);
if (sizeof($po)!=0){
mysqli_query($con,"INSERT into lab3 (IP,Community,Name,Port,Interfacenumber,Type,Monitor)  values ( '".$_GET['IP']."','".$_GET['Community']."','".$_GET['Name']."','".$_GET['port']."', '".$interfacenumber."', 'Device','SNMP')");
}
$result = mysqli_query($con,"SELECT * FROM lab3");
echo "<table border='10'>
<tr>
<th> ID </th>
<th>IP</th> 
<th>Community</th>
<th> Name </th>
<th> Port </th>
<th> Type </th>
<th> Monitor </th>
<th> Interfacenumber </th>
</tr>";
while($row = mysqli_fetch_array($result))
{echo "<tr>";
  echo "<td>" . $row['ID'] . "</td>";
  echo "<td>" . $row['IP'] . "</td>";
echo "<td>" . $row['Community'] . "</td>";
echo "<td>" . $row['Name'] . "</td>";
echo "<td>" . $row['Port'] . "</td>";
echo "<td>" . $row['Type'] . "</td>";
echo "<td>" . $row['Monitor'] . "</td>";
echo "<td>" . $row['Interfacenumber'] . "</td>";
  echo "</tr>";
}
echo "</table>";
mysqli_close($con);
echo "<p><a href='index.html'>Back to Lab2 Main Page</a></p>";
}
?>
</html>''')
f.close()
f=open('addndevice.html','w')
f.write('''<html>''')
f.write('''<form name="form1" method="get" action="interfacedisc.php">
Device Specifications:<br>
IP: <input type="text" name="IP" id="IP"><br>
Community: <input type="text" name="Community" id="Community"><br>
Name: <input type="text" name="Name"><br>
Port: <input type="text" name="port"><br>
<input type="submit" value="Do interface discovery on the interface">
</form>
<p><a href='index.html'>Back to Lab2 Main Page</a></p>;
</html>''')
f.close()
f=open('remove.php','w')
f.write("<?php $con=mysqli_connect(\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\") ;".format(host,username,password,databasename,port))
f.write('''$result = mysqli_query($con,"SELECT * FROM lab3");
echo "<table border='10'>
<tr>
<th> ID </th>
<th>IP</th> 
<th>Community</th>
<th> Name </th>
<th> Port </th>
<th> Type </th>
<th> Monitor </th>
<th> Interfacenumber </th>
</tr>";
while($row = mysqli_fetch_array($result))
  {echo "<tr>";
  echo "<td>" . $row['ID'] . "</td>";
  echo "<td>" . $row['IP'] . "</td>";
echo "<td>" . $row['Community'] . "</td>";
echo "<td>" . $row['Name'] . "</td>";
echo "<td>" . $row['Port'] . "</td>";
echo "<td>" . $row['Type'] . "</td>";
echo "<td>" . $row['Monitor'] . "</td>";
echo "<td>" . $row['Interfacenumber'] . "</td>";
  echo "</tr>";
  }
echo "</table>";
echo "<form name=\\"form1\\" method=\\"post\\" action=\\"\\" >
Enter Device ID to be removed  : <input type=\\"text\\" name=\\"ID\\" id=\\"IP\\"><br>
<input type=\\"submit\\" value=\\"Remove device\\">";
if($_SERVER['REQUEST_METHOD'] == "POST"){
$ID = $_POST["ID"];
mysqli_query($con,"DELETE FROM lab3 WHERE ID='$ID'");
echo "<p>Refresh the page </p>";
unlink($ID.'.rrd');}
mysqli_close($con);
echo "<p><a href='index.html'>Back to Lab2 Main Page</a></p>";
?>''')
f.close()
f=open('monitor.php','w')
f.write('''<html>''')
f.write("<?php $con=mysqli_connect(\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\") ;".format(host,username,password,databasename,port))
f.write('''$result = mysqli_query($con,"SELECT * FROM lab3");
echo "<table border='10'>
<tr>
<th> ID </th>
<th>IP</th> 
<th>Community</th>
<th> Name </th>
<th> Port </th>
<th> Type </th>
<th> Monitor </th>
<th> Interfacenumber </th>
</tr>";
while($row = mysqli_fetch_array($result))
{echo "<tr>";
  echo "<td>" . $row['ID'] . "</td>";
  echo "<td>" . $row['IP'] . "</td>";
echo "<td>" . $row['Community'] . "</td>";
echo "<td>" . $row['Name'] . "</td>";
echo "<td>" . $row['Port'] . "</td>";
echo "<td>" . $row['Type'] . "</td>";
echo "<td>" . $row['Monitor'] . "</td>";
echo "<td>" . $row['Interfacenumber'] . "</td>";
  echo "</tr>";
}
echo "</table>";
echo "<p><a href=\\"monitorserver.php\\">Want to see monitoring information of a server</a></p>";
echo "<p><a href=\\"monitordevice.php\\">Want to see monitoring information of a device</a></p>";
echo "<p><a href='index.html'>Back to Lab2 Main Page</a></p>";
?>
</html>''')
f.close()
f=open('comparision.php','w')
f.write('''<html>''')
f.write("<?php $con=mysqli_connect(\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\") ;".format(host,username,password,databasename,port))
f.write('''$result = mysqli_query($con,"SELECT * FROM lab3");
echo "<form name=\\"form1\\" method=\\"post\\" action=\\"\\" >";
echo "<table border='10'>
<tr>
<th> ID </th>
<th> Mark Devices </th>
<th>IP</th> 
<th>Community</th>
<th> Name </th>
<th> Port </th>
<th> Type </th>
<th> Monitor </th>
<th> Interfacenumber </th>

</tr>";
while($row = mysqli_fetch_array($result))
{echo "<tr>";
  echo "<td>" . $row['ID'] . "</td>";
  echo "<td><input type=\\"checkbox\\" name=\\"idlist[]\\" id=\\"color\\" value=".$row['ID']."></td>";
  echo "<td>" . $row['IP'] . "</td>";
echo "<td>" . $row['Community'] . "</td>";
echo "<td>" . $row['Name'] . "</td>";
echo "<td>" . $row['Port'] . "</td>";
echo "<td>" . $row['Type'] . "</td>";
echo "<td>" . $row['Monitor'] . "</td>";
if ($row['Type']=="Device"){
$checkinter=explode(",",$row['Interfacenumber']);
echo "<td>";
for($m = 0; $m < count($checkinter); ++$m) {
echo "<br>".$checkinter[$m]."<input type=\\"checkbox\\" name=\\"interfaces".$row['ID']."[]\\" id=\\"color\\" value=".$checkinter[$m]."></br>";
}
}
else{
echo "<td>" . $row['Interfacenumber'] . "</td>";
}
  echo "</tr>";
}
echo "</table>";
echo "Start time: <input type=\\"text\\" name=\\"start\\" id=\\"start\\"><br>
stop default is now : <input type=\\"text\\" name=\\"stop\\" id=\\"stop\\"><br>
In bytes/sec<input type=\\"checkbox\\" name=\\"pard[]\\" id=\\"color\\" value=\\"inbytes\\">
Out bytes/sec<input type=\\"checkbox\\" name=\\"pard[]\\" id=\\"color\\" value=\\"outbytes\\">
<br>Aggregate In bytes/sec on all interfaces<input type=\\"checkbox\\" name=\\"pard[]\\" id=\\"color\\" value=\\"AggregateIN\\"></br>
<br>Aggregate Out bytes/sec on all interfaces<input type=\\"checkbox\\" name=\\"pard[]\\" id=\\"color\\" value=\\"AggregateOUT\\"></br>
CPU Usage<input type=\\"checkbox\\" name=\\"par[]\\" id=\\"color\\" value=\\"CPUusage\\">
Requests/sec<input type=\\"checkbox\\" name=\\"par[]\\" id=\\"color\\" value=\\"reqpersec\\">
Bytes/sec<input type=\\"checkbox\\" name=\\"par[]\\" id=\\"color\\" value=\\"bytespersec\\">
Bytes/request<input type=\\"checkbox\\" name=\\"par[]\\" id=\\"color\\" value=\\"bytesperreq\\">
<input type=\\"submit\\" value=\\"See Comparion info\\">";
if($_SERVER['REQUEST_METHOD'] == "POST"){
$ps=$_POST["par"];
$pd=$_POST["pard"];
$ID = $_POST["idlist"];
$start = $_POST["start"];
$stop = $_POST["stop"];
$dpsarray=array();
$dpsarea=array();
$CPU=array();
$rps=array();
$Bpr=array();
$Bps=array();
$color=array(2097151,4194303,6291455,8388607,10485759,12582911,14680063,16777215);
$interfacecolorin=0;    #change
$interfacecolorout=2000;
for ($i=0;$i < count($ID);++$i)
{ $result = mysqli_query($con,"SELECT * FROM lab3 where ID='$ID[$i]'");
  $row = mysqli_fetch_array($result);
  if ($row['Type']== "Server"){
for($j=0;$j<count($ps);++$j){
switch ($ps[$j]){
case "CPUusage":
 $CPU[]="DEF:".$ps[$j]."_".$ID[$i]."=".$ID[$i].".rrd:".$ps[$j].":AVERAGE";
 $CPU[]="LINE2:".$ps[$j]."_".$ID[$i]."#".strtoupper(dechex($color[1]-(($i*20000)))).":".$ps[$j]."_".$ID[$i];
break;
case "reqpersec":
$rps[]="DEF:".$ps[$j]."_".$ID[$i]."=".$ID[$i].".rrd:".$ps[$j].":AVERAGE";
 $rps[]="LINE2:".$ps[$j]."_".$ID[$i]."#".strtoupper(dechex($color[5]-(($i*20000)))).":".$ps[$j]."_".$ID[$i];
break;
case "bytespersec":
$Bps[]="DEF:".$ps[$j]."_".$ID[$i]."=".$ID[$i].".rrd:".$ps[$j].":AVERAGE";
 $Bps[]="LINE2:".$ps[$j]."_".$ID[$i]."#".strtoupper(dechex($color[1]-(($i*20000)))).":".$ps[$j]."_".$ID[$i];
break;
case "bytesperreq":
$Bpr[]="DEF:".$ps[$j]."_".$ID[$i]."=".$ID[$i].".rrd:".$ps[$j].":AVERAGE";
 $Bpr[]="LINE2:".$ps[$j]."_".$ID[$i]."#" .strtoupper(dechex($color[1]-(($i*20000)))).":".$ps[$j]."_".$ID[$i];
break;
}}
}
elseif ($row['Type']== "Device") {
$indexer="interfaces".$ID[$i]; #changes
$inter=$_POST[$indexer];
for($j=0;$j<count($pd);++$j){
if($pd[$j]!="inbytes" && $pd[$j]!="outbytes"){
$dpsarray[]="DEF:".$pd[$j]."_".$ID[$i]."=".$ID[$i].".rrd:".$pd[$j].":AVERAGE";
switch ($pd[$j]){
case "AggregateIN":
 $dpsarea[]="LINE2:".$pd[$j]."_".$ID[$i]."#".strtoupper(dechex($color[6]+((10000*($i+1)+(10000*$j))))).":".$pd[$j]."_".$ID[$i];
break;
case "AggregateOUT":
 $dpsarea[]="LINE2:".$pd[$j]."_".$ID[$i]."#" .strtoupper(dechex($color[2]+((10000*($i+1)+(10000*$j))))).":".$pd[$j]."_".$ID[$i];
break;
}}
else {
for($k = 0; $k < count($inter); ++$k) {
$dpsarray[]="DEF:".$pd[$j]."_".$ID[$i].$inter[$k]."=".$ID[$i].".rrd:".$pd[$j].$inter[$k].":AVERAGE";

switch($pd[$j]){
case "inbytes":
 $dpsarea[]="LINE2:".$pd[$j]."_".$ID[$i].$inter[$k]."#".strtoupper(dechex($color[0]+(($interfacecolorin)))).":".$pd[$j]."_".$ID[$i]."_".$inter[$k];
break;
case "outbytes":
 $dpsarea[]="LINE2:".$pd[$j]."_".$ID[$i].$inter[$k]."#".strtoupper(dechex($color[7]-(($interfacecolorout)))).":".$pd[$j]."_".$ID[$i]."_".$inter[$k];
break;}
$interfacecolorin=$interfacecolorin+7000;
$interfacecolorout=$interfacecolorout+5000; ##chnage
}
}
}
}
}
#rint_r($psarray);
#print_r($psarea);
$dopts = array(
	'--end',$stop,
	'--start',$start,'--vertical-label','Bytes per sec','--alt-y-grid','--alt-autoscale','--rigid','--width',1000,'--height',500);
$popts = array(
	'--end',$stop,
	'--start',$start,'--vertical-label','Percentage(%)','--alt-y-grid','--alt-autoscale','--rigid','--width',1000,'--height',500);
$qopts = array(
	'--end',$stop,
	'--start',$start,'--vertical-label','Requests per sec','--alt-y-grid','--alt-autoscale','--rigid','--width',1000,'--height',500);
$ropts = array(
	'--end',$stop,
	'--start',$start,'--vertical-label','Bytes per request','--alt-y-grid','--alt-autoscale','--rigid','--width',1000,'--height',500);
$sopts = array(
	'--end',$stop,
	'--start',$start,'--vertical-label','Bytes per sec','--alt-y-grid','--alt-autoscale','--rigid','--width',1000,'--height',500);
$sCPU=array_merge($popts,$CPU);
$srps=array_merge($qopts,$rps);
$sBpr=array_merge($ropts,$Bpr);
$sBps=array_merge($sopts,$Bps);
$dopts=array_merge($dopts,$dpsarray,$dpsarea);
$dgraph = tempnam('/tmp', 'dcompare');
$sgraphCPU = tempnam('/tmp', 'sCPU');
$sgraphrps = tempnam('/tmp', 'srps');
$sgraphBpr = tempnam('/tmp', 'sBpr');
$sgraphBps = tempnam('/tmp', 'sBps');
$dinfo=pathinfo($dgraph);
$sinfoCPU=pathinfo($sgraphCPU);
$sinforps=pathinfo($sgraphrps);
$sinfoBpr=pathinfo($sgraphBpr);
$sinfoBps=pathinfo($sgraphBps);
$dresult = rrd_graph($dgraph, $dopts);
$sresultCPU = rrd_graph($sgraphCPU, $sCPU);
$sresultrps = rrd_graph($sgraphrps, $srps);
$sresultBpr = rrd_graph($sgraphBpr, $sBpr);
$sresultBps = rrd_graph($sgraphBps,$sBps);
if ($dresult === false) {
	echo 'There was an error: ';
	echo rrd_error();
}
else {
	echo '<br>Devices comparision</br>';
echo "<br><img border=\\"0\\" src=\\"img.php?image=".$dinfo['filename']."\\"  width=\\"1000\\"height=\\"500\\"></br>";
}
if ($sresultCPU === false && count($CPU)!=0) {
	echo 'There was an error: ';
	echo rrd_error();
}
else if (count($CPU)!=0) {
	echo '<br>Server CPU comparision</br>';
echo "<br><img border=\\"0\\" src=\\"img.php?image=".$sinfoCPU['filename']."\\"  width=\\"1000\\"height=\\"500\\"></br>";
}
if ($sresultrps === false && count($rps)!=0 ){
	echo 'There was an error: ';
	echo rrd_error();
}
else if (count($rps)!=0) {
	echo '<br>Server requests per sec comparision</br>';
echo "<br><img border=\\"0\\" src=\\"img.php?image=".$sinforps['filename']."\\"  width=\\"1000\\"height=\\"500\\"></br>";
}
if ($sresultBpr === false && count($Bpr)!=0 ) {
	echo 'There was an error: ';
	echo rrd_error();
}
else if(count($Bpr)!=0) {
	echo '<br>Server Bytes per request comparision</br>';
echo "<br><img border=\\"0\\" src=\\"img.php?image=".$sinfoBpr['filename']."\\"  width=\\"1000\\"height=\\"500\\"></br>";
}
if ($sresultBps === false && count($Bps)!=0 ){
	echo 'There was an error: ';
	echo rrd_error();
}
else if (count($Bps)!=0){
	echo '<br> Bytes per sec comparision</br>';
echo "<br><img border=\\"0\\" src=\\"img.php?image=".$sinfoBps['filename']."\\"  width=\\"1000\\"height=\\"500\\"></br>";
}
}
echo "<p><a href='index.html'>Back to Lab2 Main Page</a></p>";
?>
</html>''')
f=open('monitordevice.php','w')
f.write('''<html>''')
f.write("<?php $con=mysqli_connect(\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\") ;".format(host,username,password,databasename,port))
f.write('''$result = mysqli_query($con,"SELECT * FROM lab3 where Type='Device'");
echo "<table border='10'>
<tr>
<th> ID </th>
<th>IP</th> 
<th>Community</th>
<th> Name </th>
<th> Port </th>
<th> Type </th>
<th> Monitor </th>
<th> Interfacenumber </th>
</tr>";
while($row = mysqli_fetch_array($result))
{echo "<tr>";
  echo "<td>" . $row['ID'] . "</td>";
  echo "<td>" . $row['IP'] . "</td>";
echo "<td>" . $row['Community'] . "</td>";
echo "<td>" . $row['Name'] . "</td>";
echo "<td>" . $row['Port'] . "</td>";
echo "<td>" . $row['Type'] . "</td>";
echo "<td>" . $row['Monitor'] . "</td>";
echo "<td>" . $row['Interfacenumber'] . "</td>";
  echo "</tr>";
}
echo "</table>";
echo "<form name=\\"form1\\" method=\\"post\\" action=\\"\\" >
Enter Device ID to view the monitoring info : <input type=\\"text\\" name=\\"ID\\" id=\\"IP\\"><br>
Start time: <input type=\\"text\\" name=\\"start\\" id=\\"start\\"><br>
stop default is now : <input type=\\"text\\" name=\\"stop\\" id=\\"stop\\"><br>
In bytes/sec<input type=\\"checkbox\\" name=\\"par[]\\" id=\\"color\\" value=\\"inbytes\\">
Out bytes/sec<input type=\\"checkbox\\" name=\\"par[]\\" id=\\"color\\" value=\\"outbytes\\">
<br>Aggreggate In bytes/sec on all interfaces<input type=\\"checkbox\\" name=\\"par[]\\" id=\\"color\\" value=\\"AggregateIN\\"></br>
<br>Aggregate Out bytes/sec on all interfaces<input type=\\"checkbox\\" name=\\"par[]\\" id=\\"color\\" value=\\"AggregateOUT\\"></br>
<input type=\\"submit\\" value=\\"See monitoring info\\">";
if($_SERVER['REQUEST_METHOD'] == "POST"){
$ID = $_POST["ID"];
$po=$_POST["par"];
$start = $_POST["start"];
$stop = $_POST["stop"];
$result = mysqli_query($con,"SELECT * FROM lab3 where ID='$ID'");
$row = mysqli_fetch_array($result);
if ($row['Type']== "Device")
{
$inter=explode(",",$row['Interfacenumber']);
for($i = 0; $i < count($po); ++$i) {
$opts = array(
	'--end',$stop,
	'--start',$start,'--vertical-label','Bytes per sec');
if($po[$i]=="inbytes" || $po[$i]=="outbytes"){
16777215/count($inter);
$temp=2097151;
for($j = 0; $j < count($inter); ++$j) {

$randomcolor = '#' . strtoupper(dechex(($temp-($j))));
array_push($opts,"DEF:x$inter[$j]=$ID.rrd:$po[$i]$inter[$j]:AVERAGE",
        "LINE2:x$inter[$j]$randomcolor:\\"$po[$i]$inter[$j]\\""
	);
$temp=$temp+3000; }}
else {
array_push($opts,"DEF:x=$ID.rrd:$po[$i]:AVERAGE",
        "LINE2:x#FF0000:\\"$po[$i]\\""
	);
}

$graph = tempnam('/tmp', 'Monitor'); #changes
$info=pathinfo($graph);
$result = rrd_graph($graph, $opts);
if ($result === false) {
	echo 'There was an error: ';
	echo rrd_error();
}
echo "<br><img border=\\"0\\" src=\\"img.php?image=\".$info['filename'].\"\\"  width=\\"497\\"height=\\"167\\"></br>";}

}
}
mysqli_close($con);
echo "<p><a href='index.html'>Back to Lab2 Main Page</a></p>";
?>
</html>

''')
f.close()
f=open('monitorserver.php','w')
f.write('''<html>''')
f.write("<?php $con=mysqli_connect(\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\") ;".format(host,username,password,databasename,port))
f.write('''$result = mysqli_query($con,"SELECT * FROM lab3 where Type='Server'");
echo "<table border='10'>
<tr>
<th> ID </th>
<th>IP</th> 
<th>Community</th>
<th> Name </th>
<th> Port </th>
<th> Type </th>
<th> Monitor </th>
<th> Interfacenumber </th>
</tr>";
while($row = mysqli_fetch_array($result))
{echo "<tr>";
  echo "<td>" . $row['ID'] . "</td>";
  echo "<td>" . $row['IP'] . "</td>";
echo "<td>" . $row['Community'] . "</td>";
echo "<td>" . $row['Name'] . "</td>";
echo "<td>" . $row['Port'] . "</td>";
echo "<td>" . $row['Type'] . "</td>";
echo "<td>" . $row['Monitor'] . "</td>";
echo "<td>" . $row['Interfacenumber'] . "</td>";
  echo "</tr>";
}
echo "</table>";
echo "<form name=\\"form1\\" method=\\"post\\" action=\\"\\" >
Enter Device ID to view the monitoring info : <input type=\\"text\\" name=\\"ID\\" id=\\"IP\\"><br>
Start time: <input type=\\"text\\" name=\\"start\\" id=\\"start\\"><br>
stop default is now : <input type=\\"text\\" name=\\"stop\\" id=\\"stop\\"><br>
CPU Usage<input type=\\"checkbox\\" name=\\"par[]\\" id=\\"color\\" value=\\"CPUusage\\">
Requests/sec<input type=\\"checkbox\\" name=\\"par[]\\" id=\\"color\\" value=\\"reqpersec\\">
Bytes/sec<input type=\\"checkbox\\" name=\\"par[]\\" id=\\"color\\" value=\\"bytespersec\\">
Bytes/request<input type=\\"checkbox\\" name=\\"par[]\\" id=\\"color\\" value=\\"bytesperreq\\">
<input type=\\"submit\\" value=\\"See monitoring info\\">";
if($_SERVER['REQUEST_METHOD'] == "POST"){
$ID = $_POST["ID"];
$po=$_POST["par"];
$start = $_POST["start"];
$stop = $_POST["stop"];
$result = mysqli_query($con,"SELECT * FROM lab3 where ID='$ID'");
$row = mysqli_fetch_array($result);
$legends= array(
    "CPUusage" => "CPU Usage %",
    "reqpersec" => "Requests per sec",
    "bytespersec" => "Bytes per sec",
    "bytesperreq" => "Bytes per request",
);
if ($row['Type']== "Server")
{ for($i = 0; $i < count($po); ++$i) {
$opts = array(
	'--end',$stop,
	'--start',$start,'--vertical-label',$legends[$po[$i]],
        "DEF:x=$ID.rrd:$po[$i]:AVERAGE",
        "LINE2:x#0000FF:\\"$po[$i]\\""
	); 
$graph = tempnam('/tmp', 'Monitor'); #changes
$info=pathinfo($graph);
$result = rrd_graph($graph, $opts);
echo "<br><img border=\\"0\\" src=\\"img.php?image=\".$info['filename'].\"\\"  width=\\"497\\"height=\\"167\\"></br>";}

}
}
mysqli_close($con);
echo "<p><a href='index.html'>Back to Lab2 Main Page</a></p>";
?>
</html>
''')
f.close()
f=open('img.php','w')
f.write('''<?php
$Image=$_GET['image'];
$Image='/tmp/'.$Image;
$im = imagecreatefrompng($Image);
header('Content-Type: image/png');
imagepng($im);
imagedestroy($im);
unlink($Image);
?>''')
f.close()
