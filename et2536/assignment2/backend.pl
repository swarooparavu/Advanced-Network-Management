#!/usr/bin/perl
use DBI;
use Data::Dumper;
use Net::SNMP qw(snmp_dispatcher oid_lex_sort); #use rrd editor module its faster than oo
do '../db.conf';
my $driver = "mysql";
my $IP_database= $host;
my $dsn = "DBI:$driver:database=$database;host=$IP_database;port=$port";
my $tabledevices= "DEVICES";
my $userid = $username;
my $password = $password; # password
our $dbh = DBI->connect($dsn, $userid, $password ) or die $DBI::errstr;
my $gth = $dbh->prepare("CREATE TABLE IF NOT EXISTS `lab3` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `IP` tinytext NOT NULL,
  `Community` tinytext NOT NULL,
  `Name` tinytext NOT NULL,
   `Type` tinytext NOT NULL,
  `Monitor` tinytext NOT NULL,
  `Interfacenumber` text NOT NULL,
 `Port` int(11) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1;");
$gth->execute() or die $DBI::errstr;
my $sth = $dbh->prepare("select * from lab3");
$sth->execute() or die $DBI::errstr;
while (my @element = $sth->fetchrow_array()){
$ID=$element[0];
$IP=$element[1];
$port=$element[7];
$community=$element[2];
if ($element[4] eq "Server" )
{
if ($element[5] eq "HTTP"){
my @temp=();
print "\nHttp code here\n";
my $cpu=`lynx -dump http://$IP:$port/server-status | grep "CPU Usage" | awk '{if (NR==1) {print \$3,\$4} else {print \$1,\$4,\$7}}' | tr -d 'u' |tr -d 's' | awk '{if (NR==1) {print \$1+\$2} else {print}}' ORS=' '`;
$cpu =~ s/\s+$//;
print "CPU is ".$cpu;
@a=`lynx -dump http://$IP:$port/server-status?auto | grep "ReqPerSec:\\|BytesPerSec:\\|BytesPerReq:" | awk '{print \$2}'`;
chomp(@a);
push(@temp,$cpu);
push(@temp,@a);
print "\nresult @temp\n";
if (scalar(@temp)==4){
$cpu=$temp[0];
my $Req=$temp[1];
my $bytes=$temp[2];
my $bytesperreq=$temp[3];
my $l=system("rrdtool update $ID.rrd N:$cpu:$Req:$bytes:$bytesperreq");
if ($l)
{
system("rrdtool create  $ID.rrd --step 60  DS:CPUusage:GAUGE:120:U:U DS:reqpersec:GAUGE:120:U:U DS:bytespersec:GAUGE:120:U:U DS:bytesperreq:GAUGE:120:U:U RRA:AVERAGE:0.5:1:1440 ");
system("rrdtool update $ID.rrd N:$cpu:$Req:$bytes:$bytesperreq");
print "\nRRD updated\n";
}
}
}
}
elsif($element[4] eq "Device"){
print "\nDevice code\n";
@interfaces=split(",",$element[6]);
my @ininterfaces=();
my @outinterfaces=();
foreach $k (0..$#interfaces){
$ininterfaces[$k]='1.3.6.1.2.1.2.2.1.10.'.$interfaces[$k];
$outinterfaces[$k]='1.3.6.1.2.1.2.2.1.16.'.$interfaces[$k];
}
 
my ($session, $error) = Net::SNMP->session(
         -hostname    => $IP,
         -port        => $port,
         -community   => $community,
         -timeout     => 3,
         -nonblocking => 1,);
$session->max_msg_size(5000);
print "max size".$session->max_msg_size()."\n";
if (!defined $session) {
         printf "ERROR: Failed to create session for host '%s': %s.\n",
                $IP, $error;
         next;}
if($#interfaces<=10){ ####else condition must be there
if (!defined ($session->get_request(
         -varbindlist => [ @ininterfaces,@outinterfaces, ],
         -callback    => [ \&get_callback, $IP,$ID,$port],))) { 
  printf "ERROR: Failed to get  interface values session error '%s': %s.\n",
                $session->hostname(), $session->error();
      }}
else{#code to handle large number of interfaces
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
if (!defined ($session->get_request(
         -varbindlist => [ @inpart,@outpart, ],
         -callback    => [ \&Break_Integrate, $IP,$ID,$port]))) { 
  printf "ERROR: Failed to get  interface values session error '%s': %s.\n",
                $session->hostname(), $session->error(); }
@inpart=();
@outpart=();
}
snmp_dispatcher();
print "\n IN Couters @incounterspart\n"; 
print "\n OUT Counters @outcounterspart\n";
print "\n Interface IDs @interfaceIDpart\n";
my $totalin=0;
my $totalout=0;
foreach my $num (@incounterspart){
    $totalin = $totalin + $num;
}
foreach my $num (@outcounterspart){
    $totalout = $totalout + $num;
}
print "\n$totalin,$totalout\n";
my $string="DS:inbytes$interfaceIDpart[0]:COUNTER:120:U:U ";
for (my $i=1;$i<=$#interfaceIDpart;$i++){
$string=$string."DS:inbytes$interfaceIDpart[$i]:COUNTER:120:U:U "; }
for(my $i=0;$i<=$#interfaceIDpart;$i++){
$string=$string."DS:outbytes$interfaceIDpart[$i]:COUNTER:120:U:U ";}
$string=$string." DS:AggregateIN:COUNTER:120:U:U DS:AggregateOUT:COUNTER:120:U:U ";
$string=$string."RRA:AVERAGE:0.5:1:1440";
print "\n$ID,$IP,@incounterspart,@outcounterspart,$totalin,$totalout\n";
my $update="N:".join(":", @incounterspart).":".join(":",@outcounterspart);
my $l=system("rrdtool update $ID.rrd $update:$totalin:$totalout");
if ($l)
{
system("rrdtool create  $ID.rrd --step 60  $string");
system("rrdtool update $ID.rrd $update:$totalin:$totalout");
print "\nRRD created\n";
}
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
}}}
snmp_dispatcher();
sub get_callback
  {
 my ($session,$IP,$ID,$port) = @_;
print "\nCallback for ID  ". $ID. " entered \n";
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
my $totalin=0;
my $totalout=0;
foreach my $num (@incounters){
    $totalin = $totalin + $num;
}
foreach my $num (@outcounters){
    $totalout = $totalout + $num;
}
print "\n$totalin,$totalout\n";
print "\n IN Couters @incounters\n";   ##sort by keys which sorts all interfaces
print "\n OUT Counters @outcounters\n";
print "\n Interface IDs @interfaceID\n";
my $string="DS:inbytes$interfaceID[0]:COUNTER:120:U:U ";
for (my $i=1;$i<=$#interfaceID;$i++){
$string=$string."DS:inbytes$interfaceID[$i]:COUNTER:120:U:U "; }
for(my $i=0;$i<=$#interfaceID;$i++){
$string=$string."DS:outbytes$interfaceID[$i]:COUNTER:120:U:U ";}
$string=$string." DS:AggregateIN:COUNTER:120:U:U DS:AggregateOUT:COUNTER:120:U:U ";
$string=$string."RRA:AVERAGE:0.5:1:1440";
print "\n$ID,$IP,@incounters,@outcounters,$totalin,$totalout\n";
my $update="N:".join(":", @incounters).":".join(":",@outcounters);
my $l=system("rrdtool update $ID.rrd $update:$totalin:$totalout");
if ($l)
{
system("rrdtool create  $ID.rrd --step 60  $string");
system("rrdtool update $ID.rrd $update:$totalin:$totalout");
print "\nRRD created\n";
}}


