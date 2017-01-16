#!/jgi/tools/bin/perl -w

use strict;
use File::Copy;

# EXPECT 21 FILE HANDLES, SOME OF WHICH MAY BE 'None'
die("Missing arguments; expected at least 21, got ".scalar(@ARGV)."\n") unless @ARGV >= 21;
my $outdir=shift @ARGV;
my $alignment_info=shift @ARGV;
my $all_contigs_fasta=shift @ARGV;
my $all_contigs_qual=shift @ARGV;
my $all_diffs=shift @ARGV;
my $all_struct_vars=shift @ARGV;
my $hc_diff=shift @ARGV;
my $hc_struct_vars=shift @ARGV;
my $mapping_qc=shift @ARGV;
my $newbler_metrics=shift @ARGV;
my $pair_align=shift @ARGV;
my $read_status=shift @ARGV;
my $ref_status=shift @ARGV;
my $tag_pair_align=shift @ARGV;
my $trim_status=shift @ARGV;
my $trimmed_reads_fasta=shift @ARGV;
my $trimmed_reads_qual=shift @ARGV;
my $contigs_ace=shift @ARGV;
my $contigs_bam=shift @ARGV;
my $large_contigs_fasta=shift @ARGV;
my $large_contigs_qual=shift @ARGV;
my $gene_status=shift @ARGV;

# REMOVE PARAMETERS FOR OPTIONAL FILES WHICH WERE NOT PROVIDED

my @cmd=removeUnusedOptions(@ARGV);

# RUN COMMAND
my $stderr;
eval { $stderr=`runMapping @cmd 2>&1`; };
if ( $@ ) {
    print STDERR "Newbler ERROR: $stderr\n";
    `cat $outdir/assembly/454NewblerProgress.txt 1>&2`;
    die($@);
}

get_outfile("$outdir/454AlignmentInfo.tsv", $alignment_info);
get_outfile("$outdir/454AllContigs.fna", $all_contigs_fasta);
get_outfile("$outdir/454AllContigs.qual", $all_contigs_qual);
get_outfile("$outdir/454AllDiffs.txt", $all_diffs);
get_outfile("$outdir/454AllStructVars.txt", $all_struct_vars);
get_outfile("$outdir/454HCDiff.txt", $hc_diff);
get_outfile("$outdir/454HCStructVars.txt", $hc_struct_vars);
get_outfile("$outdir/454MappingQC.xls", $mapping_qc);
get_outfile("$outdir/454NewblerMetrics.txt", $newbler_metrics);
get_outfile("$outdir/454PairAlign.txt", $pair_align);
get_outfile("$outdir/454ReadStatus.txt", $read_status);
get_outfile("$outdir/454RefStatus.txt", $ref_status);
get_outfile("$outdir/454TagPairAlign.txt", $tag_pair_align);
get_outfile("$outdir/454TrimStatus.txt", $trim_status);
get_outfile("$outdir/454TrimmedReads.fna", $trimmed_reads_fasta);
get_outfile("$outdir/454TrimmedReads.qual", $trimmed_reads_qual);
get_outfile("$outdir/454Contigs.ace", $contigs_ace);
get_outfile("$outdir/454Contigs.bam", $contigs_bam);
get_outfile("$outdir/454LargeContigs.fna", $large_contigs_fasta);
get_outfile("$outdir/454LargeContigs.qual", $large_contigs_qual);
get_outfile("$outdir/454GeneStatus.txt", $gene_status);
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
