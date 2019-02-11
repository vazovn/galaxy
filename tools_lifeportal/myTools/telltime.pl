#!/usr/bin/perl -w

open (IN, "<$ARGV[0]");
open (OUT, ">$ARGV[1]");

#system("sleep 30");
my $time = localtime();
print OUT  "The time is $time\n";

close( IN );
close( OUT );
