#!/usr/bin/perl -w

use strict;
use Sys::Hostname;

#open (IN, "<$ARGV[0]");
open(OUT, ">$ARGV[0]") or die "Can't open $ARGV[0]: $!\n";
# open (OUT, ">$ARGV[1]");

#sleep(100);
my $time = localtime();
my $hostname = hostname();
my $user_email = $ARGV[1];
if(length($user_email)>=8){
 $user_email=substr $user_email, 0, 8;  
}


#my $userl = $ENV{'SLURM_JOB_USER'};
#my $usage = system("resusage > usage");

#foreach my $key (sort keys %ENV ){
#    print OUT "$key: $ENV{$key}\n";
#}

print  OUT "Abel is up and running.\n";
print  OUT "It is $time on $hostname\n\n";
print  OUT "Abel resources:";
close( OUT );
system("echo  >> $ARGV[0]");
system("resusage >> $ARGV[0]");
system("echo >> $ARGV[0]");
system("echo 'Your Lifeportal jobs on Cluster' >> $ARGV[0]");
system("squeue | grep $user_email  >> $ARGV[0]");
system("echo  >> $ARGV[0]");
system("echo 'Total number of Lifeportal jobs on Cluster' >> $ARGV[0]");
system("squeue | grep galaxy | wc -l >> $ARGV[0]");
system("echo  >> $ARGV[0]");
#system("echo $user_email >> $ARGV[0]");



#close( IN );
close( OUT );

exit 1;
