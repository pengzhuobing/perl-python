#!usr/bin/perl

foreach my$table(`ls ./5*fq`){
	open(IN,$ARGV[0]) or die "$!";
	open OUT,"> ./out.txt" or die "$!";
	my $base = 0;
	my %hash = {};
	print OUT "readsname\tGC_content\tN_content\tQ20\tQ30";
	for(;;){
		my$line1=<IN>;
		my$line2=<IN>;
		my$line3=<IN>;
		my$line4=<IN>;
		chomp $line1;
		#print OUT "\n$line1";
		chomp $line2;
		@reads = split(//,$line2);	
		@quality = split(//,$line4);
		my $q20num =0;
		my $q30num =0;
		my $GC = 0;
		my $N = 0;
		for $i (0..$#reads){
			$base += 1;
			if($reads[$i] eq "C" || $reads[$i] eq "G"){
				$GC += 1;
			}
			else{
				if($reads[$i] eq "N"){
					$N += 1;
				}
			}
		}
		$GC_content = $GC/$#reads;
		$N_content = $N/$#reads;

		#print OUT "\t$GC_content\t$N_content";

		for $i (0..$#quality){
			my $ASCII = ord($quality[$i]);
			if($ASCII > 53){
				$q20num += 1;
			}
			if($ASCII > 63){
				$q30num += 1;
			}
		}
		$q20 = $q20num/$#quality;
		$q30 = $q30num/$#quality;
		#print OUT "\t$q20\t$q30";

		@value = ($GC_content,$N_content,$q20,$q30);
		$hash{$line1} = "@value";

		@a = split(/ /,$hash{$line1});
		if($a[0] < 0.65 || $a[0] > 0.4 || $a[1] == 0 || $a[2] > 0.9){
			$key =keys %hash;
			print OUT "\n$key\t$a[0]\t$a[1]\t$a[2]\t$a[3]";
		}

	}


	print OUT "\n$base";
	close IN;

}
