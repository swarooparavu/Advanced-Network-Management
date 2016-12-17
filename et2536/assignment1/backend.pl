#!/usr/bin/perl
#This file is executed using crontab
use DBI;
use Data::Dumper;
use Net::SNMP qw(snmp_dispatcher oid_lex_sort);
use RRD::Editor (); #use rrd editor module its faster than oo
do '../db.conf';
my $driver = "mysql";
my $IP_database= $host;
my $dsn = "DBI:$driver:database=$database;host=$IP_database;port=$port";
my $tabledevices= "DEVICES";
my $userid = $username;
my $password = $password; # password
our $dbh = DBI->connect($dsn, $userid, $password ) or die $DBI::errstr;
$img="img";
open(my $fh5, '>', "$img.php"); #PHP file generation for use of Dynamic web content
print $fh5 "<?php
\$Image=\$_GET['image'];
\$Image='/tmp/'.\$Image;
\$im = imagecreatefrompng(\$Image);
header('Content-Type: image/png');

imagepng(\$im);
imagedestroy(\$im);
unlink(\$Image);
?>";
close $fh5;
$Grapher="Grapher";
open($fh3, '>', "$Grapher.php"); #PHP file generation for use of Dynamic web content, Dont worry about variable names
print $fh3 "<?php
\$InterfaceID=\$_GET['IfID'];
\$DevID=\$_GET['ID'];
\$DevID=\$DevID.\".rrd\";  
\$opts_test= array(
	'--end',\"now\",
	'--start',\"now-600\",'--alt-y-grid','--alt-autoscale','--rigid','--width',500,'--height',250,
        \"DEF:inbyterate\$InterfaceID=\$DevID:InterfaceIN\$InterfaceID:AVERAGE\",
        \"DEF:outbyterate\$InterfaceID=\$DevID:InterfaceOUT\$InterfaceID:AVERAGE\",
        \"AREA:inbyterate\$InterfaceID#0000FF:IN bytes per sec\", 
        \"LINE2:outbyterate\$InterfaceID#FF0000:OUT bytes per sec\",
\"GPRINT:inbyterate\$InterfaceID:AVERAGE:IN AVG %6.2lf\\l\",
\"GPRINT:outbyterate\$InterfaceID:AVERAGE:OUT AVG %6.2lf\\l\",
\"GPRINT:inbyterate\$InterfaceID:MAX:IN MAX %6.2lf\\l\",
\"GPRINT:outbyterate\$InterfaceID:MAX:OUT MAX %6.2lf\\l\",
\"GPRINT:inbyterate\$InterfaceID:LAST:IN LAST %6.2lf\\l\",
\"GPRINT:outbyterate\$InterfaceID:LAST:OUT LAST %6.2lf\\l\"); #7FB37C
\$opts_day= array(
	'--end',\"now\",
	'--start',\"now-1d\",'--alt-y-grid','--alt-autoscale','--rigid','--width',500,'--height',250,
        \"DEF:inbyterate\$InterfaceID=\$DevID:InterfaceIN\$InterfaceID:AVERAGE\",
        \"DEF:outbyterate\$InterfaceID=\$DevID:InterfaceOUT\$InterfaceID:AVERAGE\",
        \"AREA:inbyterate\$InterfaceID#0000FF:IN bytes per sec\", 
        \"LINE2:outbyterate\$InterfaceID#FF0000:OUT bytes per sec\",
\"GPRINT:inbyterate\$InterfaceID:AVERAGE:IN AVG %6.2lf\\l\",
\"GPRINT:outbyterate\$InterfaceID:AVERAGE:OUT AVG %6.2lf\\l\",
\"GPRINT:inbyterate\$InterfaceID:MAX:IN MAX %6.2lf\\l\",
\"GPRINT:outbyterate\$InterfaceID:MAX:OUT MAX %6.2lf\\l\",
\"GPRINT:inbyterate\$InterfaceID:LAST:IN LAST %6.2lf\\l\",
\"GPRINT:outbyterate\$InterfaceID:LAST:OUT LAST %6.2lf\\l\"); #7FB37C
\$opts_week= array( # gprint can be associated i am bored
	'--end',\"now\",
	'--start',\"now-1w\",'--alt-y-grid','--alt-autoscale','--rigid','--width',500,'--height',250,
        \"DEF:inbyterate\$InterfaceID=\$DevID:InterfaceIN\$InterfaceID:AVERAGE\",
        \"DEF:outbyterate\$InterfaceID=\$DevID:InterfaceOUT\$InterfaceID:AVERAGE\",
         \"AREA:inbyterate\$InterfaceID#0000FF:IN bytes per sec\", 
        \"LINE2:outbyterate\$InterfaceID#FF0000:OUT bytes per sec\",
\"GPRINT:inbyterate\$InterfaceID:AVERAGE:IN AVG %6.2lf\\l\",
\"GPRINT:outbyterate\$InterfaceID:AVERAGE:OUT AVG %6.2lf\\l\",
\"GPRINT:inbyterate\$InterfaceID:MAX:IN MAX %6.2lf\\l\",
\"GPRINT:outbyterate\$InterfaceID:MAX:OUT MAX %6.2lf\\l\",
\"GPRINT:inbyterate\$InterfaceID:LAST:IN LAST %6.2lf\\l\",
\"GPRINT:outbyterate\$InterfaceID:LAST:OUT LAST %6.2lf\\l\" );
\$opts_month= array(
	'--end',\"now\",
	'--start',\"now-1m\",'--alt-y-grid','--alt-autoscale','--rigid','--width',500,'--height',250,
       \"DEF:inbyterate\$InterfaceID=\$DevID:InterfaceIN\$InterfaceID:AVERAGE\",
        \"DEF:outbyterate\$InterfaceID=\$DevID:InterfaceOUT\$InterfaceID:AVERAGE\",
         \"AREA:inbyterate\$InterfaceID#0000FF:IN bytes per sec\", 
        \"LINE2:outbyterate\$InterfaceID#FF0000:OUT bytes per sec\",
\"GPRINT:inbyterate\$InterfaceID:AVERAGE:IN AVG %6.2lf\\l\",
\"GPRINT:outbyterate\$InterfaceID:AVERAGE:OUT AVG %6.2lf\\l\",
\"GPRINT:inbyterate\$InterfaceID:MAX:IN MAX %6.2lf\\l\",
\"GPRINT:outbyterate\$InterfaceID:MAX:OUT MAX %6.2lf\\l\",
\"GPRINT:inbyterate\$InterfaceID:LAST:IN LAST %6.2lf\\l\",
\"GPRINT:outbyterate\$InterfaceID:LAST:OUT LAST %6.2lf\\l\" );
\$opts_year= array(
	'--end',\"now\",
	'--start',\"now-1y\",'--alt-y-grid','--alt-autoscale','--rigid','--width',500,'--height',250,
        \"DEF:inbyterate\$InterfaceID=\$DevID:InterfaceIN\$InterfaceID:AVERAGE\",
        \"DEF:outbyterate\$InterfaceID=\$DevID:InterfaceOUT\$InterfaceID:AVERAGE\",
         \"AREA:inbyterate\$InterfaceID#0000FF:IN bytes per sec\", 
        \"LINE2:outbyterate\$InterfaceID#FF0000:OUT bytes per sec\",
\"GPRINT:inbyterate\$InterfaceID:AVERAGE:IN AVG %6.2lf\\l\",
\"GPRINT:outbyterate\$InterfaceID:AVERAGE:OUT AVG %6.2lf\\l\",
\"GPRINT:inbyterate\$InterfaceID:MAX:IN MAX %6.2lf\\l\",
\"GPRINT:outbyterate\$InterfaceID:MAX:OUT MAX %6.2lf\\l\",
\"GPRINT:inbyterate\$InterfaceID:LAST:IN LAST %6.2lf\\l\",
\"GPRINT:outbyterate\$InterfaceID:LAST:OUT LAST %6.2lf\\l\");
\$graph_test = tempnam('/tmp', 'test'); #changes
\$graph_day = tempnam('/tmp', 'day');
\$graph_week = tempnam('/tmp', 'week');
\$graph_month = tempnam('/tmp', 'month');
\$graph_year = tempnam('/tmp', 'year');
\$result_test = rrd_graph(\$graph_test, \$opts_test); #change2
\$result_day = rrd_graph(\$graph_day, \$opts_day);
\$result_week = rrd_graph(\$graph_week, \$opts_week);
\$result_month = rrd_graph(\$graph_month, \$opts_month);
\$result_year = rrd_graph(\$graph_year, \$opts_year);
\$info_test=pathinfo(\$graph_test); #change3
\$info_day=pathinfo(\$graph_day);
\$info_week=pathinfo(\$graph_week);
\$info_month=pathinfo(\$graph_month);
\$info_year=pathinfo(\$graph_year);
if (\$result_test === false) {
	echo 'The interface might be loopback or there must be an error: ';
	echo rrd_error();
}
else {
echo \"10min test\";
echo \"<img border=\\\"0\\\" src=\\\"img.php?image=\".\$info_test['filename'].\"\\\"  width=\\\"500\\\"height=\\\"250\\\"><br>\";
}
if (\$result_day === false) {
	echo '<p>The interface might be loopback or there must be an error: test graph cannot be generated </p>';
	echo rrd_error();
}
else {
echo \"day graph\";
echo \"<img border=\\\"0\\\" src=\\\"img.php?image=\".\$info_day['filename'].\"\\\"  width=\\\"500\\\"height=\\\"250\\\"><br>\";
}
if (\$result_week === false) {
	echo '<p>The interface might be loopback or there must be an error: week graph cannot be generated </p> ';
	echo rrd_error();
}
else {
echo \"week graph\";
echo \"<img border=\\\"0\\\" src=\\\"img.php?image=\".\$info_week['filename'].\"\\\" width=\\\"500\\\"height=\\\"250\\\"><br>\";
}
if (\$result_month === false) {
	echo '<p>The interface might be loopback or there must be an error:month graph cannot be generated </p> ';
	echo rrd_error();
}
else {
echo \"month graph\";
echo \"<img border=\\\"0\\\" src=\\\"img.php?image=\".\$info_month['filename'].\"\\\"  width=\\\"500\\\"height=\\\"250\\\"><br>\";
}
if (\$result_year === false) {
	echo '<p>The interface might be loopback or there must be an error: year graph cannot be generated </p> ';
	echo rrd_error();
}
else {
echo \"year graph\";
echo \"<img border=\\\"0\\\" src=\\\"img.php?image=\".\$info_year['filename'].\"\\\"  width=\\\"500\\\"height=\\\"250\\\"><br>\";
}
?>";
close $fh3;
my $gth = $dbh->prepare("CREATE TABLE IF NOT EXISTS `lab2` (
  `ID` int(11) NOT NULL,
  `Interfaces` text NOT NULL
) ENGINE=MyISAM  DEFAULT CHARSET=latin1");
$gth->execute() or die $DBI::errstr;
#handles changing database
my $sth = $dbh->prepare("select ID from $tabledevices");
$sth->execute() or die $DBI::errstr;
my @Mhost_ID=();
while (my @element = $sth->fetchrow_array()){
push(@Mhost_ID,$element[0]);
}
my @IDC=();
my $cth = $dbh->prepare("select ID from lab2");
$cth->execute() or die $DBI::errstr;
while (my @element = $cth->fetchrow_array()){
push(@IDC,$element[0]);
}
$flag=0;
@diff=();
foreach $i(0..$#Mhost_ID){
foreach $j (0..$#IDC){
if ($Mhost_ID[$i]!=$IDC[$j]){
$flag++;}
}
if ($flag==$#IDC+1){
push(@diff,$Mhost_ID[$i]);
}
$flag=0;
}
if (scalar @diff!=0){
print "Data is modified in the database\n";
print "Interface discovery will be performed on modifications\n";
InterfaceDisc(\@diff);}
#diff=Array1-(array1 instersection array2)
POLL(\@Mhost_ID);
#this collects the interfaces info
sub POLL{
 my ($loID)=@_;
my @loID=@$loID;
foreach my $ghost (0..$#loID){
$loID[$ghost]= 'ID='.$loID[$ghost];
}
my $QUERY="select ID,IP,Port,Community from $tabledevices where ".join(" or ", @loID);
my $dth = $dbh->prepare($QUERY);
$dth->execute() or die $DBI::errstr;
my @host_ID=();
my @host_data=();
my @port=();
my @community=();
while (my @element = $dth->fetchrow_array()){
#print Dumper(@element);
push(@host_ID,$element[0]);
push(@host_data,$element[1]);
push(@port,$element[2]);
push(@community,$element[3]);
}
$index="index";
open(my $fh0, '>', "$index.html");
print $fh0 "<html xmlns=\"http://www.w3.org/1999/xhtml\">
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />
<title>LAB2</title>

</head>
<body>";
foreach $ghost (0..$#host_data) {
print $fh0 "<a href=\"$host_data[$ghost]_$host_ID[$ghost].html\">Click here for  IP=$host_data[$ghost] ID=$host_ID[$ghost] </a><br>";} 
print $fh0 "</body></html>";
close $fh0;
print "Index file has been modified/created in server directory specified";
foreach $host (0..$#host_ID) {
      my ($session, $error) = Net::SNMP->session(
         -hostname    => $host_data[$host],
         -port        => $port[$host],
         -community   => $community[$host],
         -timeout     => 10,
         -nonblocking => 1,
      );
$session->max_msg_size(5000);
print "max size".$session->max_msg_size()."\n";
if (!defined $session) {
         printf "ERROR: Failed to create session for host '%s': %s.\n",
                $host_data[$host], $error;
         next;
      }
my $eth= $dbh->prepare("Select Interfaces from lab2 where ID=\'$host_ID[$host]\'");
$eth->execute() or die $DBI::errstr;
my $temp=$eth->fetchrow_array();
my @interfaces = split(':', $temp);
my @ininterfaces=();
my @outinterfaces=();
#tester
#$#interfaces=11;
#@interfaces=(1..$#interfaces+1);
foreach $k (0..$#interfaces){
$ininterfaces[$k]='1.3.6.1.2.1.2.2.1.10.'.$interfaces[$k];
$outinterfaces[$k]='1.3.6.1.2.1.2.2.1.16.'.$interfaces[$k];
}
print Dumper(@ininterfaces);
#@ininterfaces[1]='1.3.6.1.2.1.2.2.1.10.1';
print "Pollable IDs ". $host_ID[$host]. "\n";

if($#interfaces<=10){ ####less than ten interfaces so in and out makes twenty
if (!defined ($session->get_request(
         -varbindlist => [ @ininterfaces,@outinterfaces, ],
         -callback    => [ \&get_callback, $host_data[$host],$host_ID[$host],$port[$host],$host],))) { 
  printf "ERROR: Failed to get  interface values session error '%s': %s.\n",
                $session->hostname(), $session->error();
      }}
else{
#code to handle large number of interfaces
@interfaceIDpart=();
@incounterspart=();
@outcounterspart=();
my $lower=0;
my $upper=$#interfaces%10;
#print "\nUpeer  is $upper";
for (;$upper<=$#interfaces;){ 
my @inpart=@ininterfaces[$lower..$upper]; 
my @outpart=@outinterfaces[$lower..$upper];
$lower=$upper+1;
$upper= $lower+9;
#print Dumper(@inpart);
#print Dumper(@outpart);
# global variables for intergrating
if (!defined ($session->get_request(
         -varbindlist => [ @inpart,@outpart, ],
         -callback    => [ \&Break_Integrate, $host_data[$host],$host_ID[$host],$port[$host],$host],))) { 
  printf "ERROR: Failed to get  interface values session error '%s': %s.\n",
                $session->hostname(), $session->error();
      }
@inpart=();
@outpart=();
}
snmp_dispatcher();
print "\n IN Couters @incounterspart\n"; 
print "\n OUT Counters @outcounterspart\n";
print "\n Interface IDs @interfaceIDpart\n";
#RRD entrance break integrate
my $rrd = RRD::Editor->new();
my $update="N:".join(":", @incounterspart).":".join(":",@outcounterspart);
print $update;
#print "Update string ".$update."\n";
my $check=eval{$rrd->open("$host_ID[$host].rrd")}; # RRD handlers include dynamic Data source handling
if(!$check){
my $string="DS:InterfaceIN$interfaceIDpart[0]:COUNTER:600:U:U ";
for (my $i=1;$i<=$#interfaceIDpart;$i++){
$string=$string."DS:InterfaceIN$interfaceIDpart[$i]:COUNTER:600:U:U ";
}
for(my $i=0;$i<=$#interfaceIDpart;$i++){
$string=$string."DS:InterfaceOUT$interfaceIDpart[$i]:COUNTER:600:U:U ";}
$string=$string."RRA:AVERAGE:0.5:1:30 RRA:AVERAGE:0.5:30:48 RRA:AVERAGE:0.5:1440:30 RRA:AVERAGE:0.5:43200:12 RRA:MAX:0.5:1:30 RRA:MAX:0.5:30:48 RRA:MAX:0.5:1440:30 RRA:MAX:0.5:43200:12 RRA:LAST:0.5:1:30 RRA:LAST:0.5:30:48 RRA:LAST:0.5:1440:30 RRA:LAST:0.5:43200:12";
if ($#incounterspart!=-1){
$rrd->create($string);
$rrd->save("$host_ID[$host].rrd");
$rrd->update($update);
print "\nRRD Updated\n";
}}
else {
if ($#incounterspart!=-1){
$rrd->update($update);
print "\nRRD Updated\n";
}}
sub Break_Integrate{
my ($session,$IP,$ID,$port, $number) = @_;
foreach my $k (oid_lex_sort(keys(%{$session->var_bind_list()}))){
my $v=$session->var_bind_list()->{$k};
if(index($k,'1.3.6.1.2.1.2.2.1.10.') != -1)
{ my $interfacenumber = substr( $k, rindex( $k, '.' ) + 1 );
 push(@interfaceIDpart,$interfacenumber); push(@incounterspart,$v);
}elsif(index($k,'1.3.6.1.2.1.2.2.1.16.') != -1) { push(@outcounterspart,$v); } 
}
}

}}
snmp_dispatcher();
sub get_callback
  {
 my ($session,$IP,$ID,$port, $number) = @_;
print "\nCallback for ID  ". $ID. " entered \n";
 my @names = $session->var_bind_names();
print "Results will be pushed to rrd files\n";
#print Dumper($octect);
my @interfaceID=();
my @incounters=();
my @outcounters=();
foreach my $k (oid_lex_sort(keys(%{$session->var_bind_list()}))){
my $v=$session->var_bind_list()->{$k};
#print "\nHeart $k"." $v\n";
if(index($k,'1.3.6.1.2.1.2.2.1.10.') != -1)
{ $interfacenumber = substr( $k, rindex( $k, '.' ) + 1 );
 push(@interfaceID,$interfacenumber); push(@incounters,$v);
} elsif(index($k,'1.3.6.1.2.1.2.2.1.16.') != -1) { push(@outcounters,$v); } 
}
print "\n IN Couters @incounters\n";   ##sort by keys which sorts all interfaces
print "\n OUT Counters @outcounters\n";
print "\n Interface IDs @interfaceID\n";
my $rrd = RRD::Editor->new();
my $update="N:".join(":", @incounters).":".join(":",@outcounters);
#print "Update string ".$update."\n";
my $check=eval{$rrd->open("$ID.rrd")}; # RRD handlers include dynamic Data source handling
if(!$check){
my $string="DS:InterfaceIN$interfaceID[0]:COUNTER:600:U:U ";
for (my $i=1;$i<=$#interfaceID;$i++){
$string=$string."DS:InterfaceIN$interfaceID[$i]:COUNTER:600:U:U ";
}
for(my $i=0;$i<=$#interfaceID;$i++){
$string=$string."DS:InterfaceOUT$interfaceID[$i]:COUNTER:600:U:U ";}
$string=$string."RRA:AVERAGE:0.5:1:30 RRA:AVERAGE:0.5:30:48 RRA:AVERAGE:0.5:1440:30 RRA:AVERAGE:0.5:43200:12 RRA:MAX:0.5:1:30 RRA:MAX:0.5:30:48 RRA:MAX:0.5:1440:30 RRA:MAX:0.5:43200:12 RRA:LAST:0.5:1:30 RRA:LAST:0.5:30:48 RRA:LAST:0.5:1440:30 RRA:LAST:0.5:43200:12";
if ($#incounters!=-1){
$rrd->create($string);
$rrd->save("$ID.rrd");
$rrd->update($update);
}}
else {
if ($#incounters!=-1){
$rrd->update($update);
}}
}}
#interface discovery along with  ifspeed loopback and operational status.
sub InterfaceDisc
{
 my ($hID) = @_;
my @ho_ID=@$hID;
print "Interface Discovery will be done for IDs,@ho_ID\n";
#print Dumper(@ho_ID);
foreach $host (0..$#ho_ID){
$ho_ID[$host]= 'ID='.$ho_ID[$host];
}
my $QUERY="select ID,IP,Port,Community from $tabledevices where ".join(" or ", @ho_ID);

my $dth = $dbh->prepare($QUERY);
$dth->execute() or die $DBI::errstr;
my @host_ID=();
my @host_data=();
my @port=();
my @community=();
while (my @element = $dth->fetchrow_array()){
#print Dumper(@element);
push(@host_ID,$element[0]);
push(@host_data,$element[1]);
push(@port,$element[2]);
push(@community,$element[3]);
}
#print Dumper(@host_data);
foreach $host (0..$#host_data) {
      my ($session, $error) = Net::SNMP->session(
         -hostname    => $host_data[$host],
         -port        => $port[$host],
         -community   => $community[$host],
         -nonblocking => 1,
      );
if (!defined $session) {
         printf "ERROR: Failed to create session for host '%s': %s.\n",
                $host_data[$host], $error;
         next;
      }
$interfaces_speed='1.3.6.1.2.1.2.2.1.5';
if (!defined ($session->get_table(-baseoid  => $interfaces_speed,
                                 -callback => [\&results_cb, $host_data[$host],$host_ID[$host],$port[$host],$host]))) {
         printf "ERROR: Failed to queue get next  IN request for host '%s': %s.\n",
                $session->hostname(), $session->error();
      }

}

snmp_dispatcher();
# Loop back interface removal
foreach $host (0..$#host_data) {
      my ($session_l, $error) = Net::SNMP->session(
         -hostname    => $host_data[$host],
         -port        => $port[$host],
         -community   => $community[$host],
         -nonblocking => 1,
      );
$loopback='1.3.6.1.2.1.4.20.1.2.127.0.0.1';
if (!defined $session_l) {
         printf "ERROR: Failed to create session for host '%s': %s.\n",
                $host_data[$host], $error;
         next;
      }
if (!defined ($session_l->get_request(
         -varbindlist => [ $loopback ],
        -callback    => [ \&get_callback_Loop, $host_data[$host],$host_ID[$host],$port[$host],$host],))) { 
  printf "ERROR: Failed to get loopback interface '%s': %s.\n",
                $session_l->hostname(), $session_l->error();
      }
}
snmp_dispatcher();
foreach $host (0..$#host_data) {
      my ($session_k, $error) = Net::SNMP->session(
         -hostname    => $host_data[$host],
         -port        => $port[$host],
         -community   => $community[$host],
         -nonblocking => 1,
      );

$ifoperationalstatus='1.3.6.1.2.1.2.2.1.8';
if (!defined $session_k) {
         printf "ERROR: Failed to create session for host '%s': %s.\n",
                $host_data[$host], $error;
         next;
      }
if (!defined ($session_k->get_table(-baseoid  => $ifoperationalstatus,
                                 -callback => [\&results_cbd, $host_data[$host],$host_ID[$host],$port[$host],$host]))) {
         printf "ERROR: Failed to queue get next  IN request for host '%s': %s.\n",
                $session->hostname(), $session->error();
      }
}
snmp_dispatcher();

} #Interfacce discovery loop end
#


sub get_callback_Loop
   {
my ($session, $IP,$ID,$port, $number) = @_;
my $result = $session->var_bind_list();
$loopnot=scalar keys $result;
if($loopnot!=0 ){
print "LOOP BACK $result->{$loopback} \n";
my $zth= $dbh->prepare("Select Interfaces from lab2 where ID=\'$ID\'");
$zth->execute() or die $DBI::errstr;
my $temp=$zth->fetchrow_array();
my @values = split(':', $temp);
if (grep( /^$result->{$loopback}$/, @values )){
my $index = 0;
$index++ until $values[$index]==$result->{$loopback};
splice(@values, $index, 1);
print "Removed loopbacks\n";
my $datafeed=join(":", @values);
my $fth= $dbh->prepare("update lab2 set  Interfaces=\'$datafeed\' where ID=\'$ID\'");
$fth->execute() or die $DBI::errstr;}}
}
#operational status
sub results_cbd # call : one is up two means down
   {
      my ($session, $IP,$ID,$port, $number) = @_;
my @downinterfacesID=();
if (!defined($session->var_bind_list())) {
      printf("ERROR: %s.\n", $session->error());
   } else {
print "\nInterface operational status done on " .$ID."\n";
foreach (oid_lex_sort(keys(%{$session->var_bind_list()}))) { 
if($session->var_bind_list()->{$_}!=1){  #ifoperational status not one
push(@downinterfacesID,substr( $_, rindex( $_, '.' ) + 1 ));
         }}
my $zth= $dbh->prepare("Select Interfaces from lab2 where ID=\'$ID\'");
$zth->execute() or die $DBI::errstr;
my $temp=$zth->fetchrow_array();
my @values = split(':', $temp);
my $flag=0;
my @differ=();
foreach $i(0..$#values){
foreach $j (0..$#downinterfacesID){
if ($values[$i]!=$downinterfacesID[$j]){
$flag++;}
}
if ($flag==$#downinterfacesID+1){
push(@differ,$values[$i]);
}
$flag=0;
}
open(my $fh, '>', "$IP\_$ID.html");
print $fh "<html xmlns=\"http://www.w3.org/1999/xhtml\">
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />
<title>Untitled Document</title>
</head>
<body>";
for (my $i=0;$i<=$#differ;$i++){
print $fh "<a href=\"Grapher.php?ID=$ID&IfID=$differ[$i]\">Click here for  Interface ID $differ[$i]</a><br>";} 
print $fh "</body></html>";
close $fh;
my $datafeed=join(":", @differ);
my $fth= $dbh->prepare("update lab2 set  Interfaces=\'$datafeed\' where ID=\'$ID\'");
$fth->execute() or die $DBI::errstr;
}
}# end of operational elimination

sub results_cb # call : not to block any requests
   {
      my ($session, $IP,$ID,$port, $number) = @_;
my @interfacesID=();
if (!defined($session->var_bind_list())) {
      printf("ERROR: %s.\n", $session->error());
   } else {
print "\nInterface discovery done on ID " .$ID."\n";
foreach (oid_lex_sort(keys(%{$session->var_bind_list()}))) { 
if($session->var_bind_list()->{$_}!=0){  #ifspeed zero has been eliminated
push(@interfacesID,substr( $_, rindex( $_, '.' ) + 1 ));
         }}
my $datafeed=join(":", @interfacesID);


print "Datafeed".$datafeed."\n";
my $bth= $dbh->prepare("INSERT INTO lab2
                       (ID,Interfaces)
                        values
                       (\'$ID\',\'$datafeed\')");
$bth->execute() or die $DBI::errstr;
$bth->finish();
}}

