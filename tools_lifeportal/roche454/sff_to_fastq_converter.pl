#!/usr/bin/env perl

use warnings;
use strict;
use Getopt::Long;
use File::Basename;

# VALIDATE INPUT
die("Expected 3 args") unless @ARGV == 3;
my ($sff, $extra_files_path, $fastq) = @ARGV;

# DEFINE PATHS
mkdir($extra_files_path) unless -d $extra_files_path;
my $base  = basename($sff);
my $fasta = "$extra_files_path/$base.fasta";
my $qual  = "$extra_files_path/$base.qual";

# GENERATE FASTA, QUAL, FASTQ
my $outf;
my $out;
eval { $out=`sffinfo -seq $sff > $fasta` };
die("ERROR: $out") if $@;
print $out;
eval { $out=`sffinfo -qual $sff > $qual` };
die("ERROR: $out") if $@;
print $out;
eval { $out=`fasta_qual_to_fastq $fasta $qual $fastq` };
die("ERROR: $out") if $@;
print $out;
unlink($fasta, $qual);
exit 0;
