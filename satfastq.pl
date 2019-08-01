#!usr/bin/perl

#open(FQ,$ARGV[0]) or die "$!";
foreach my $table(`ls ./5*fq`){
        #my $table = shift;
        open(FQ,"<$table") or die "$!";

open OUT,">./out.txt" or die "$!";

my$num;
my $i;

$line1 = <FQ>;
chomp $line1;
print OUT "$line1";

while(<FQ>){
	chomp $_;
	if($_ =~ /\@V300010089L2C\w+\/1/){
		print OUT "\n$_";
	}
	else{
		if($_ eq "+"){
			$num += 1;
		}
		else{
			if($_ =~ /[^ATCGN]/){
				@quality = split(//,$_);
				my $q20num = 0;
				my $q30num = 0;
				for $i (0..$#quality){
					$ASCII = ord($quality[$i]);
					if($ASCII > 53){
						$q20num += 1;	
					}
					if($ASCII > 63){
						$q30num += 1;
					}
				}
				$q20 = $q20num/$#quality;
				$q30 = $q30num/$#quality;
				print OUT "\nQ20 = $q20\tQ30 = $q30";

			}
			else{
				@reads = split(//,$_);
				my $CG = 0;
				my $N = 0;
				for $i (0..$#reads){
					if($reads[$i] eq "C" || $reads[$i] eq "G"){
						$CG += 1;
					}
					if($reads[$i] eq "N"){
						my $N += 1;	
					}
				}
				$precentCG = $CG/$#reads;
				$precentN = $N/$#reads;
				print OUT "\nCG_content = $precentCG\tN_content = $precentN\tbasenum = $#reads";
			}
		}
	}
}

print OUT "readsnum = $num\t ";
}
