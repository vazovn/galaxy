#!/usr/bin/env perl

use warnings;
use strict;
use File::Copy;

# EXPECT 20 FILE HANDLES, SOME OF WHICH MAY BE 'None'
die("Missing arguments; expected at least 20, got ".scalar(@ARGV)."\n") unless @ARGV >= 20;
my $outdir=shift @ARGV;
my $newbler_metrics=shift @ARGV;
my $read_status=shift @ARGV;
my $trimmed_reads_fasta=shift @ARGV;
my $trimmed_reads_qual=shift @ARGV;
my $alignment_info=shift @ARGV;
my $all_contigs_fasta=shift @ARGV;
my $all_contigs_qual=shift @ARGV;
my $contigs_ace=shift @ARGV;
my $contigs_consed_ace=shift @ARGV;
my $contig_graph=shift @ARGV;
my $pair_align=shift @ARGV;
my $pair_status=shift @ARGV;
my $scaffolds_fasta=shift @ARGV;
my $scaffolds_qual=shift @ARGV;
my $scaffolds_agp=shift @ARGV;
my $contig_scaffolds_agp=shift @ARGV;
my $tag_pair_align=shift @ARGV;
my $trim_status=shift @ARGV;
my $large_contigs_fasta=shift @ARGV;
my $large_contigs_qual=shift @ARGV;

# REMOVE PARAMETERS FOR OPTIONAL FILES WHICH WERE NOT PROVIDED

my @cmd=removeUnusedOptions(@ARGV);

# RUN COMMAND
my $stderr;
eval { $stderr=`runAssembly @cmd 2>&1`; };
if ( $@ ) {
    print STDERR "Newbler ERROR: $stderr\n";
    `cat $outdir/assembly/454NewblerProgress.txt 1>&2`;
    die($@);
}

get_outfile("$outdir/454NewblerMetrics.txt", $newbler_metrics);
get_outfile("$outdir/454ReadStatus.txt", $read_status);
get_outfile("$outdir/454TrimmedReads.fna", $trimmed_reads_fasta);
get_outfile("$outdir/454TrimmedReads.qual", $trimmed_reads_qual);
get_outfile("$outdir/454AlignmentInfo.tsv", $alignment_info);
get_outfile("$outdir/454AllContigs.fna", $all_contigs_fasta);
get_outfile("$outdir/454AllContigs.qual", $all_contigs_qual);
get_outfile("$outdir/454Contigs.ace", $contigs_ace);
get_outfile("$outdir/consed/edit_dir/454Contigs.ace.1", $contigs_consed_ace);
get_outfile("$outdir/454ContigGraph.txt", $contig_graph);
get_outfile("$outdir/454PairAlign.txt", $pair_align);
get_outfile("$outdir/454PairStatus.txt", $pair_status);
get_outfile("$outdir/454Scaffolds.fna", $scaffolds_fasta);
get_outfile("$outdir/454Scaffolds.qual", $scaffolds_qual);
get_outfile("$outdir/454Scaffolds.txt", $scaffolds_agp);
get_outfile("$outdir/454ContigScaffolds.txt", $contig_scaffolds_agp);
get_outfile("$outdir/454TagPairAlign.txt", $tag_pair_align);
get_outfile("$outdir/454TrimStatus.txt", $trim_status);
get_outfile("$outdir/454LargeContigs.fna", $large_contigs_fasta);
get_outfile("$outdir/454LargeContigs.qual", $large_contigs_qual);
exit;

# EVERY 'None' ARG AND IT'S PRECEEDING OPTION TAG ARE DISCARDED
sub removeUnusedOptions {
    my @cmd=();
    my $prev;
    foreach (@_) {
        unless ($_ eq 'None') {
            push @cmd, $prev if defined($prev);
            $prev=$_;
        } else {
            $prev=undef;
        }
    }
    push @cmd, $prev if defined($prev);
    return @cmd;
}

sub get_outfile {
    my ($src, $dest)=@_;
    # make sure dest defined and src exist; skip if dest is 'None'
    if ( $dest and $dest ne 'None' and $src and -f $src ) {
        move($src,$dest);
    }
}

__END__
