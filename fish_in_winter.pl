#!/usr/bin/perl
open(FISH,$ARGV[0]) or die "$!";
open(SEA,$ARGV[1]) or die "$!";
my @fish = <FISH>;
my @selfish;
for $i (0..$#fish){
	@line = split(/\t/,$fish[$i]);
	if ($line[1]=~/$ARGV[2]/){
	#$selfish=$selfish.$line[1];
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
		if ($head[$m]==$selfish[$n]){
			print "$txt[$n]\t";
		}
	}
	print"\n";
}

close FISH;
close SEA;
