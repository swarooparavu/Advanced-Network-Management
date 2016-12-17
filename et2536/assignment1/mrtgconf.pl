#!/usr/bin/perl
#Database interface
use DBI;
#Accessing Config file
do '../db.conf';
#Collecting Server Directory from User
print "\nAll the Device monitoring can be accessed via browser and is present in /var/www/mrtg/ \n";
sleep 1;
print "\nI will create the folder for you\n";
#Connect to database
our $Connection = DBI->connect( "DBI:mysql:database=$database;host=$host;port=$port",$username,$password ) or die $DBI::errstr;
#Extract ID,IP,PORT,COMMUNTIY
my $select = $Connection->prepare("select id,IP,Port,Community from DEVICES");
$select->execute() or die $DBI::errstr;
#for each ID,IP,PORT ,COMMUNITY Create cfg file, demonize mrtg, crete an index page
print "\nGenrating Configuration files\n";
#index file for all index pages - user comfortability
eval{`mkdir -p /var/www/mrtg`};
sleep 1;
print "\nI am also creating index of all index files, open index.html first\n";
open(my $fh2, '>', "/var/www/mrtg/index.html");
print $fh2 "<html>
<head>
<title>INDEX OF ALL INDEX</title>
</head>
";
while (my ($ID,$IP,$PORT,$COMMUNITY) = $select->fetchrow_array()){
eval{`cfgmaker --global "RunAsDaemon: Yes " --global "Options[_]: growright" --output=/tmp/$ID.cfg $COMMUNITY\@$IP:$PORT   `}; 
eval{`env LANG=C mrtg /tmp/$ID.cfg`};
eval{`indexmaker --output=\/var\/www\/mrtg\/index$ID.html /tmp/$ID.cfg`};
print $fh2 "<p>click here:  <a href=\"index$ID.html\">index$ID</a></p>";
}
print $fh2 "<p>when interface discovery has failed you will see pagenot found error</p>";
print $fh2 "</html>";
close $fh2
