#!/usr/bin/perl
if($#ARGV<1){
	die "Usage: perl fishing_and_classification.pl <fish> <sea>\n"
}

open(FISH,$ARGV[0]) or die "$!";
open(SEA,$ARGV[1]) or die "$!";

my @fish = <FISH>;
my @selfish;
my %dict = ();
for $i (1..$#fish){
	chomp$fish[$i];
	@line = split(/\t/,$fish[$i]);
	if (1){ #$line[1]=~/$ARGV[2]/ || ! $line[1]){
		#$selfish=$selfish.$line[1];
		if(! $dict{$line[1]}){
			$dict{$line[1]} = [];
		}
		push @{$dict{$line[1]}}, $line[0];
	}
}

@kk = keys %dict;
print "ID\t".join("\t", @kk)."\n";

$title = <SEA>;
chomp $title;
my@head = split(/\t/,$title);
while(<SEA>){
	chomp $_;
	@txt =split(/\t/,$_);
	print $txt[0];
	for $n(0..$#kk){
		$group = $kk[$n];
		@values = @{$dict{$group}};
		my$total = 0;
		for $m(0..$#txt){
			for $j(0..$#values){
				if($values[$j] eq $head[$m]){
					$total += $txt[$m];	
				}
			}
		}
		print "\t$total";

	}
	print"\n";
}

close FISH;
close SEA;
