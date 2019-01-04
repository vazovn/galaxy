#!/usr/bin/perl -w

use strict;
use Cwd;

my $line = "";

open (IN, "<$ARGV[0]");
open (OUT, ">postnexus.out");

print OUT "Postscout test.................\n";
while (<IN>)
{
  $line = $_;
  chomp($line);
  print OUT "$line\n";
}

close(IN);
close(OUT);
