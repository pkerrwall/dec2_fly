#!/usr/bin/env python

import os, sys
from datetime import datetime

# pipeline is for paired-end sequences per sample
if len(sys.argv) < 1:
    print("usage: python salmon_aln.py <sample>")
    sys.exit(1)

# pipeline for paired-end reads
sample = sys.argv[1]
start_time = datetime.now()
fastq_dir = '.'
output_dir = '.'
salmon_index = '~/db/Dmel/dmel_r6.39/dmel-all-transcript-r6.39.fasta_hisat2_index'
salmon_exe = '~/software/salmon/salmon-1.9.0_linux_x86_64/bin/salmon'
gtf_file = '~/db/Dmel/dmel_r6.39/dmel-all-r6.39.gtf'
threads=32

# define input and output files
fq1_input = f"{fastq_dir}/{sample}_1.cleaned.fq.gz"
fq2_input = f"{fastq_dir}/{sample}_2.cleaned.fq.gz"
aln_output = f"{output_dir}/{sample}_salmon_quant"

print(f"{salmon_exe} quant \
    -l A -p {threads} \
    -i {salmon_index} \
    -1 {fastq_dir}/{sample}_1.cleaned.fq.gz -2 {fastq_dir}/{sample}_2.cleaned.fq.gz \
    --validateMappings -o {output_dir}/{sample}_salmon_quant \
    -g {gtf_file}")
os.system(f"{salmon_exe} quant \
    -l A -p {threads} \
    -i {salmon_index} \
    -1 {fastq_dir}/{sample}_1.cleaned.fq.gz -2 {fastq_dir}/{sample}_2.cleaned.fq.gz \
    --validateMappings -o {output_dir}/{sample}_salmon_quant \
    -g {gtf_file}")

total_time = datetime.now() - start_time
print(f"{sample} excecution time = {total_time}")
