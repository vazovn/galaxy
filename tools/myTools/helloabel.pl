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


print  OUT "Abel is up and running. \nIt is $time on $hostname.\n\n";
print  OUT "Abel resources:\n";
close( OUT );
system("resusage >> $ARGV[0]");
system("echo >> $ARGV[0]");
system("echo 'Number of Lifeportal jobs on Cluster' >> $ARGV[0]");
system("squeue | grep galaxy | wc -l >> $ARGV[0]");



#close( IN );
close( OUT );

exit 1;
