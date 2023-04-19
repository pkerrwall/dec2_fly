#!/usr/bin/env python

import pyfastx
import os,sys,time
import pandas as pd
from datetime import datetime

if len(sys.argv) < 1:
    print("usage: python trim_galore_pipeline.py <sample>")
    sys.exit(1)

# pipeline for paired-end reads
sample = sys.argv[1]
start_time = datetime.now()
fastq_dir = '.'
trim_galore_exe = '~/software/TrimGalore/trim_galore'
cpu_num = 8

# change to directory
print(f"cd {fastq_dir}")
os.system(f"cd {fastq_dir}")

# trim adapters
print(f"{trim_galore_exe} -j {cpu_num} --paired {sample}_1.fq.gz {sample}_2.fq.gz")
os.system(f"{trim_galore_exe} -j {cpu_num} --paired {sample}_1.fq.gz {sample}_2.fq.gz")

# trim polyA
print(f"{trim_galore_exe} --polyA -j {cpu_num} --paired {sample}_1_val_1.fq.gz {sample}_2_val_2.fq.gz")
os.system(f"{trim_galore_exe} --polyA -j {cpu_num} --paired {sample}_1_val_1.fq.gz {sample}_2_val_2.fq.gz")

# rename final ouput files
os.system(f"mv {sample}_1_val_1_val_1.fq.gz {sample}_1.cleaned.fq.gz")
os.system(f"mv {sample}_2_val_2_val_2.fq.gz {sample}_2.cleaned.fq.gz")
os.system(f"mv {sample}_1.fq.gz_trimming_report.txt {sample}_1.cleaned.fq.gz.trimming_report_1.txt")
os.system(f"mv {sample}_1_val_1.fq.gz_trimming_report.txt {sample}_1.cleaned.fq.gz.trimming_report_2.txt")
os.system(f"mv {sample}_2.fq.gz_trimming_report.txt {sample}_2.cleaned.fq.gz.trimming_report_1.txt")
os.system(f"mv {sample}_2_val_2.fq.gz_trimming_report.txt {sample}_2.cleaned.fq.gz.trimming_report_2.txt")

# remove intermediate files
os.system(f"rm {sample}_1_val_1.fq.gz {sample}_2_val_2.fq.gz")

total_time = datetime.now() - start_time
print(f"total script excecution time = {total_time}")
