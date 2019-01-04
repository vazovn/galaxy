#!/usr/bin/perl -w

use strict;
use Cwd;

my $i = "";

open (LOG, ">mirrorargs.log");

my $len = scalar(@ARGV);

 foreach $i (@ARGV)
 {
   print LOG "$i ";
 }

print LOG "\n";
print LOG "length: $len\n";

print LOG "working directory: ";
my $path = cwd ();
print LOG "$path";
print LOG "\n";


close(LOG);




