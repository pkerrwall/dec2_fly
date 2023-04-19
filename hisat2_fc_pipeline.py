#!/usr/bin/env python

import os, sys
from datetime import datetime

hisat2_exe = '~/software/HISAT2/hisat2-2.2.1/hisat2/hisat2'
fastq_dir = '/home/shared/projects/dec2_illumina/fastq'
bam_dir = '/home/shared/projects/dec2_illumina/bam'
genome_index = '/home/shared/db/Dmel/dmel_r6.39/dmel-all-chromosome-r6.39.fasta_hisat2_index'
gtf_file = '/home/shared/db/Dmel/dmel_r6.39/dmel-all-r6.39.gtf'
splice_site_file = '/home/shared/db/Dmel/dmel_r6.39/dmel-all-r6.39.gtf.ss'
threads = 32

start_time = datetime.now()

libs = ['WT','DecWT','P384R']
#libs = ['WT']
for lib in libs:
    for rep in [1, 2, 3]:
    #for rep in [1]:
        # hisat2 alignment of each output file
        # define input and output files
        fq1_input = f"{fastq_dir}/{lib}_{rep}_1.cleaned.fq.gz"
        fq2_input = f"{fastq_dir}/{lib}_{rep}_2.cleaned.fq.gz"
        bam_file = f"{bam_dir}/{lib}_{rep}.bam"

        print(f"hisat2 -p {threads} --dta --rna-strandness RF --known-splicesite-infile {splice_site_file} -x {genome_index} -1 {fq1_input} -2 {fq2_input} | samtools view -@ {threads} -Shu - | samtools sort -n -@ {threads} -o {bam_file} -")
        #os.system(f"hisat2 -p {threads} --dta --rna-strandness RF --known-splicesite-infile {splice_site_file} -x {genome_index} -1 {fq1_input} -2 {fq2_input} | samtools view -@ {threads} -Shu - | samtools sort -n -@ {threads} -o {bam_file} -")
        
        # sort and index the bam file - not sure this is relevant for only differential expression analysis
        print(f"samtools sort -@ {threads} -o {bam_file}.sorted.bam {bam_file}")
        os.system(f"samtools sort -@ {threads} -o {bam_file}.sorted.bam {bam_file}")

        # Index the sorted bam
        print(f"samtools index -@ {threads} {bam_file}.sorted.bam")
        os.system(f"samtools index -@ {threads} {bam_file}.sorted.bam")
        
        # original bam and sorted bam give same count results
        bam_file = f"{bam_dir}/{lib}_{rep}.bam.sorted.bam" 
        
        # run featureCounts
        # featureCounts -R CORE -T 32 -t exon -g gene_id -L --primary -a gtf_in -o featureCounts.counts.txt bam_in
        # -R CORE gives detailed info on the read mapping
        # -L long read counting mode (only when sequencing nanopore)
        # --primary - If specified, only primary alignments will be counted.
                
        # all alignments - primary and all give same count results
        #print(f"/home/shared/software/subread/bin/featureCounts -p -R CORE -T 32 -a {gtf_file} -o {bam_file}.featureCounts.all.counts {bam_file}")
        #os.system(f"/home/shared/software/subread/bin/featureCounts -p -R CORE -T 32 -a {gtf_file} -o {bam_file}.featureCounts.all.counts {bam_file}")
        #os.system(f"mv {bam_file}.featureCounts {bam_file}.featureCounts.all")
        
        # only primary alignments
        print(f"/home/shared/software/subread/bin/featureCounts -p -R CORE -T 32 --primary -a {gtf_file} -o {bam_file}.featureCounts.primary.counts {bam_file}")
        os.system(f"/home/shared/software/subread/bin/featureCounts -p -R CORE -T 32 --primary -a {gtf_file} -o {bam_file}.featureCounts.primary.counts {bam_file}")
        os.system(f"mv {bam_file}.featureCounts {bam_file}.featureCounts.primary")
        
        # compress the main output file
        print(f"pigz {bam_file}.featureCounts.primary")
        os.system(f"pigz {bam_file}.featureCounts.primary")

# calculate and print the total run time
total_time = datetime.now() - start_time
print(f"total script excecution time = {total_time}")
