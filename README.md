# dec2_fly
## cleaning
for sample in Wt-1 Wt-2 Wt-3 DecWt-1 DecWt-2 DecWt-3 P384R-1 P384R-2 P384R-3; do echo $sample; python trim_galore_pipeline.py $sample; done

## mapping
### build hisat2 index
cd ~/db/Dmel/dmel_r6.39
extract_splice_sites.py dmel-all-r6.39.gtf > dmel-all-r6.39.gtf.ss
extract_exons.py dmel-all-r6.39.gtf > dmel-all-r6.39.gtf.exon
hisat2-build -p 32 --ss dmel-all-r6.39.gtf.ss --exon dmel-all-r6.39.gtf.exon dmel-all-chromosome-r6.39.fasta dmel-all-chromosome-r6.39.fasta_hisat2_index

### build salmon index
cd ~/db/Dmel/dmel_r6.39
~/software/salmon/salmon-1.6.0_linux_x86_64/bin/salmon index -p 32 \
    -t dmel-all-transcript-r6.39.fasta -i dmel-all-transcript-r6.39.fasta_hisat2_index

### hisat2 alignment
hisat2_fc_pipeline.py

### salmon alignment 
for sample in Wt-1 Wt-2 Wt-3 DecWt-1 DecWt-2 DecWt-3 P384R-1 P384R-2 P384R-3; do echo $sample; python salmon_aln.py $sample; done

### minimap2 alignments for nanopore
# minimap2 arguments from A comprehensive examination of Nanopore native RNA sequencing for characterization of complex transcriptomes (Nature 2019)
p=.80; N=100
threads=32
echo run minimap2 with salmon arguments p=$p `date`
minimap2 -t $threads -ax map-ont -p $p -N $N $transcript_fa $lib/$fq | samtools view -bh > $lib/$fq.transcript_aln.p$p.N$N.bam
samtools sort -@ $threads -o $lib/$fq.transcript_aln.p$p.N$N.sorted.bam $lib/$fq.transcript_aln.p$p.N$N.bam # Sort bam
samtools index -@ $threads $lib/$fq.transcript_aln.p$p.N$N.sorted.bam # Index the sorted bam
samtools view -@ $threads -b -h -F 2308 $lib/$fq.transcript_aln.p$p.N$N.sorted.bam > $lib/$fq.transcript_aln.p$p.N$N.sorted.primary.bam # Create bam with primary alignment only

## counts
### generate count files for cdna only - need to remove ncrna from salmon alignments
python salmon_counts.py

### hisat2 counts
python hisat2_counts.py

## dge
### create sample_info.txt to be used in DeSeq2
sample  Condition
WT_1    WT
WT_2    WT
WT_3    WT
DecWT_1 DecWT
DecWT_2 DecWT
DecWT_3 DecWT
P384R_1 P384R
P384R_2 P384R
P384R_3 P384R

### run dge_pipeline
python dge_pipeline.py # need to edit outdir in R script for this location
