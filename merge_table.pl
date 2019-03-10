#!/usr/bin/perl
my (@samples, %spe_sample_value);
foreach my $table(`ls /ifshk5/BC_COM_P11/F18FTSNCWLJ1137/pengzhuobing/*/Profile/Disease*_10gene_genus_abundance_profile.xls`){
    save_table($table);
}
output();
sub save_table(){
    my $table = shift;
    my @AOA;
    open (DATA,"<$table") or die "$!";
    #@samples = <DATA>;
    my $len = 0;
    while(<DATA>){
        my @tmp =split;
        $len = $#tmp;
        push @AOA,\@tmp;
    }

    for $i (1..$len){
        push @samples, $AOA[0][$i];
    }

    for $n (1..$#AOA){
        for $m (1..$len){
            $spe_sample_value{$AOA[$n][0]}{$AOA[0][$m]} = $AOA[$n][$m];
        }
    }
    close DATA;
}
#------------------------------------------------------------------	
sub output(){
#	open OUT,">HTN_OB_T2D_heatmap_input.txt" or die $!;
	open OUT,">$ARGV[0]" or die $!;
	my @sample_sort = sort @samples;
	print OUT "ID\t".join("\t", @sample_sort)."\n";
	foreach my $spe(sort keys %spe_sample_value){
		my $outline = "$spe";
		foreach my $sample(@sample_sort){
			if(exists $spe_sample_value{$spe}{$sample}){
				$outline .= "\t$spe_sample_value{$spe}{$sample}";
			}else{
				$outline .=  "\t0";
			}
		}
		$outline .= "\n";
		print OUT $outline;
	}
	close OUT;
}
