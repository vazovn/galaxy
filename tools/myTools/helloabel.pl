#!/usr/bin/perl -w

use strict;
use Sys::Hostname;

#open (IN, "<$ARGV[0]");
open(OUT, ">$ARGV[0]") or die "Can't open $ARGV[0]: $!\n";
# open (OUT, ">$ARGV[1]");

#sleep(100);
my $time = localtime();
my $hostname = hostname();
#my $usage = system("resusage > usage");

#foreach my $key (sort keys %ENV ){
#    print OUT "$key: $ENV{$key}\n";
#}


print  OUT "Hello from Abel!\nIt is $time on $hostname.\n\n";
print  OUT "Abel resources:\n";
close( OUT );
system("resusage >> $ARGV[0]");

#close( IN );
close( OUT );

exit 1;
