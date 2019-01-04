#!/usr/bin/perl -w

use strict;
use Cwd;


#########################################################################################
# Katerina Michalickova, Nov 2013
#
# adapt galaxy toolshed emboss xml files to lifeportal use
# 
#
###########################################################################################

my $xmlpath = "*.xml";
my @files = ();
my $listfile = "filelist";


@files = GetFileList($xmlpath);
ProcessAll(@files);


sub GetFileList
  {
    my ($path) = @_;
    my $list = "";
    my @read = ();
    my @files = ();

    system("echo $path > $listfile");
    if (!open(LIST, "$listfile"))
    {
      die "Cannot open $listfile\n";
    }
    @read = <LIST>;
    close LIST;
    system("rm $listfile");
    @files = split(/\s/,$read[0]);
    return @files;
  }
  
  

sub ProcessXML
  {
    my ($file) = @_;
    my $line = "";
    my $found = 0;
    
    my $newfilename = $file . "_orig";
    system("mv $file $newfilename");
    
    open(IN, $newfilename);
    open(OUT, "$file");
    
    while (<IN>)
     {
       $line = $_;
       if ($line =~ /\<command\>(*)\<\\command\>/)
        {
           $found = 1;
        }
       #print OUT $line;
     }
    if ($found == 0) 
    {
      print "$file not matching";
    }
   
    close(IN);
    close(OUT);
  }



sub ProcesAll
  {
   my(@files) = @_;
   my $file = "";
   
   foreach $file (@files)
   {
      ProcessXML($file);
   }
  }
  
  
  
  
  
  
  
  
