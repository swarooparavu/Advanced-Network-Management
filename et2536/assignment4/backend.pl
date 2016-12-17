#!/usr/bin/perl
# Required Modules
use DBI;
use Data::Dumper;
use Net::SNMP;
#dont need rgb module perl
#reading Configuration file
do '../db.conf';
my $driver = "mysql"; 
my $IP_database= $host;
my $dsn = "DBI:$driver:database=$database;host=$IP_database;port=$port";
my $tabledevices= "DEVICES"; 
my $userid = $username; # user ID 
my $password = $password; # password
print ("Creating PHP files ");
$t="index";
open(my $fh, '>', "$t.php");
print $fh "<html><meta http-equiv=\"refresh\" content=\"20\"> <?php \$con=mysqli_connect(\"$IP_database\",\"$userid\",\"$password\",\"$database\",\"$port\");
\$result = mysqli_query(\$con,\"SELECT * FROM lab5\"); 
echo \"<table border='10'>
<tr>
<th> ID </th>
<th>IP</th>
<th>Community</th>
<th>Color</th>
</tr>\";
while(\$row = mysqli_fetch_array(\$result))
{echo \"<tr>\";
  echo \"<td>\" . \$row['ID'] . \"</td>\";
  echo \"<td><a href=\\\"redirect.php?IP=\".\$row['IP'].\"&Community=\".\$row['Community']. \"\\\">\". \$row['IP'] . \"</a></td>\";
  echo \"<td>\" . \$row['Community'] . \"</td>\";
  echo \"<td bgcolor=\".\$row['Color'].\" </td>\";
 echo \"</tr>\";
  }echo \"</table>\";
?> 
</html>
";
close $fh;
print "done creating lab5.php\n";
$t="redirect";
open(my $fh2, '>', "$t.php");
print $fh2 "<html><meta http-equiv=\"refresh\" content=\"20\"> <?php
\$IP=\$_GET['IP'];
\$Community=\$_GET['Community'];  \$con=mysqli_connect(\"$IP_database\",\"$userid\",\"$password\",\"$database\");\$Que=\"SELECT IP, Community, Lastreportedtime,totalsent,totallost,updated_at  FROM lab5 where IP=\\\"\$IP\\\" AND Community=\\\"\$Community\\\"\" ;
\$result = mysqli_query(\$con,\$Que);
echo \"<table border='10'>
<tr>
<th>IP</th>
<th>Community</th>
<th>Last Reported Time</th>
<th>Total Number of Request's sent</th>
<th>Total Number of Unanswered Request's</th>
<th>Last update time</th>
</tr>\";
while(\$row = mysqli_fetch_array(\$result))
{echo \"<tr>\";
 echo \"<td>\" . \$row['IP'] . \"</td>\";
  echo \"<td>\" . \$row['Community'] . \"</td>\";
  echo \"<td>\" . \$row['Lastreportedtime'] . \"</td>\";
echo \"<td>\" . \$row['totalsent'] . \"</td>\";
echo \"<td>\" . \$row['totallost'] . \"</td>\";
echo \"<td>\" . \$row['updated_at'] . \"</td>\";
 echo \"</tr>\";
}  
echo \"</table>\";
\$date = date('Y-m-d H:i:s');
echo \"local PC time\".\$date;
?> 
</html>";
close $fh2;
print ("Done creating redirect.php");
our $dbh = DBI->connect($dsn, $userid, $password ) or die $DBI::errstr;
my $sth = $dbh->prepare("CREATE TABLE IF NOT EXISTS `lab5` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `IP` tinytext NOT NULL,
  `PORT` tinytext NOT NULL,
  `Community` tinytext NOT NULL,
  `Color` tinytext NOT NULL,
  `Lastreportedtime` tinytext NOT NULL,
  `totalsent` int(11) NOT NULL DEFAULT '0',
  `totallost` int(11) NOT NULL DEFAULT '0',
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                     ON UPDATE CURRENT_TIMESTAMP,  
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1");
$sth->execute() or die $DBI::errstr;
my $kth= $dbh->prepare("INSERT INTO lab5 (ID,IP,PORT,COMMUNITY) SELECT id,IP,PORT,COMMUNITY FROM $tabledevices"); 
$kth->execute() or die $DBI::errstr;
my $OID_sysUpTime = '1.3.6.1.2.1.1.3.0';
my $sth = $dbh->prepare("select IP,Port,Community from $tabledevices");
$sth->execute() or die $DBI::errstr;
my @host_data=();
my @port=();
my @community=();
while (my @element = $sth->fetchrow_array()){
#print Dumper(@element);
push(@host_data,$element[0]);
push(@port,$element[1]);
push(@community,$element[2]);
}
our @number_lost;
our @number_cm;
our @number_sent;
foreach my $c (0..$#host_data)
{
push(@number_lost,0);
push(@number_cm,0);
push(@number_sent,0);
}

while(1) {
my $start_run = time();
print "\nstart time for  devices".$start_run."\n";
foreach $host (0..$#host_data) {
      my ($session, $error) = Net::SNMP->session(
         -hostname    => $host_data[$host],
         -port        => $port[$host],
         -community   => $community[$host],
         -nonblocking => 1,
         -timeout     => 1,
         
      );
#print (Dumper($session));
 if (!defined $session) {
         printf "ERROR: Failed to create session for host '%s': %s.\n",
                $host_data[$host], $error;
         next;
      }

      my $result = $session->get_request(
         -varbindlist => [ $OID_sysUpTime ],
         -callback    => [ \&get_callback, $host_data[$host], $port[$host],$host],
      );
#print "$number_sent[$host] sent \n";
#print "$port[$host]\n port number";
if (!defined $result) {
         printf "ERROR: Failed to queue get request for host '%s': %s.\n",
                $session->hostname(), $session->error();
      }

    
}


   # Now initiate the SNMP message exchange.

snmp_dispatcher();
my $end_run = time();
print "\nend time for  devices".$end_run."\n";
my $run_time = $end_run - $start_run;
print "\ntime taken to send  requests/responses for  devices ".$run_time."\n";
my $sleep_time =30-$run_time;

    sleep $sleep_time;}
   exit 0;
sub get_callback
   {

      my ($session, $IP,$port, $number) = @_;  
my $color;  
     $number_sent[$number]=$number_sent[$number]+1;
     my $result = $session->var_bind_list();
      if (!defined $result) {
   $number_lost[$number]=  $number_lost[$number]+1;
  print "\nCumulative Misses $number_cm[$number]  ,$IP\n";
  $number_cm[$number]=$number_cm[$number]+1;
        }
else{
      $number_cm[$number]=0;
      }
my $commu=$session->security->community;
     
if ($number_cm[$number]>=29){
   $number_cm[$number]=28;
    }
	$color=sprintf("%x",255-($number_cm[$number]*8)) x 2;
$color=uc($color);
$color='#FF'.$color;
print "\ncolor $color\n";
print "\nresult seems here $result->{$OID_sysUpTime}\n";
if ($result->{$OID_sysUpTime}!=''){
 my $cth= $dbh->prepare("update lab5 set Color=\'$color\', Lastreportedtime=\'$result->{$OID_sysUpTime}\', totalsent=\'$number_sent[$number]\', totallost=\'$number_lost[$number]\' where IP=\'$IP\' AND Community=\'$commu\'AND Port=\'$port\'");
$cth->execute() or die $DBI::errstr;}
else
{
 my $cth= $dbh->prepare("update lab5 set Color=\'$color\', totalsent=\'$number_sent[$number]\', totallost=\'$number_lost[$number]\' where IP=\'$IP\' AND Community=\'$commu\'AND Port=\'$port\'");
$cth->execute() or die $DBI::errstr;
}
my $date2=`date +%s`;
my $ID=$number+1;
print "\nresponse time  of". $ID ."is".$date2."\n";
}

