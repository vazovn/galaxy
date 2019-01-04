#!/usr/bin/perl -w

use strict;
use Cwd;

my $i = "";
my %pairs = ();
my $prev = "";
my $cur = "";
my $nexus = "";
my $line = "";
my $key = "";
my $count = 0;
my $modkey = "";

open (IN, "<$ARGV[0]");
open (OUT, ">nexus.out");
open (LOG, ">nexuspath.log");


my $len = scalar(@ARGV);
print LOG "length: $len\n";



 foreach $i (@ARGV)
 {
   print LOG "ARG: $i \n";
   $count = $count+1;
   if ($count == 1)
   {
     $nexus = $i;
   }
   elsif ($prev eq "")
   {
     $prev = $i;
   }
   else
   {
     $cur = $i;
     $pairs{$prev} = $cur;
     $prev = "";
     $cur = "";
   }
  }


foreach $key (keys %pairs)
{
   print LOG "key: $key  value: $pairs{$key}\n";
}


print LOG "working directory: ";
my $path = cwd ();
print LOG "$path";
print LOG "\n";


# replace filenames with the Galaxy ones
while (<IN>)
{
  $line = $_;
  chomp($line);
  foreach $key (keys %pairs)
  {
    $modkey = "=".$key;
    if ($line =~ $modkey)
    {
       $line =~ s/$key/$pairs{$key}/;
    }
  }
   print OUT "$line\n";
   
}


close(IN);
close(OUT);
close(LOG);




