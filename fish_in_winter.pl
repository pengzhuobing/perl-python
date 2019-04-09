#!/usr/bin/perl
#Match the first line of <SEA> according to the first column selected in <FISH>

if($#ARGV<2){
	die "Usage: perl fish_in_winter.pl <FISH> <SEA> <sel or none> 
Match the first line of <SEA> according to the first column selected in <FISH> \n"
}
open(FISH,$ARGV[0]) or die "$!";
open(SEA,$ARGV[1]) or die "$!";
my @fish = <FISH>;
my @selfish;
for $i (0..$#fish){
	@line = split(/\t/,$fish[$i]);
	if ($line[1]=~/$ARGV[2]/ || !$line[1]){
	push @selfish,$line[0];
	print "$line[0]\t";
	}
}
print"\n";

my @sea = <SEA>;
my@head = split(/\t/,$sea[0]);
for $m (1..$#sea){
	@txt =split(/\t/,$sea[$m]);
	for $n(0..$#selfish){
		if ($head[$m] eq $selfish[$n]){
			print "$txt[$n]\t";
		}
	}
	print"\n";
}

close FISH;
close SEA;
