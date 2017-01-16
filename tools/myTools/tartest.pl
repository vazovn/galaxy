#!/usr/bin/perl -w

use strict;
use Cwd;


my $comnd = "";
my $logname = "";

$logname = $ARGV[0].".log";
open (LOG, ">$logname");

print LOG "working directory: ";
my $path = cwd ();
print LOG "$path";
print LOG "\n";

$comnd = "cp " . $ARGV[0] . " " . $ARGV[0] . ".new";
system("$comnd");
#system("sleep 60");
system("touch out1");
system("touch out2");
#system("touch out3");

close(LOG);





