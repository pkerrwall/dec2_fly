import pandas as pd
import os

# create input directory and files for DeSeq2
dge_dir = '.'
os.chdir(dge_dir)
# samples = Wt DecWt P384R
# comparisons Wt_DecWt Wt_P384R DecWt_P384R
script = 'RunDeSeq2_with_args.R'

# N2 Spin salmon
command = 'Rscript ' + script + ' N2 Spin salmon'
print(command)
os.system(command)

# N2 Spin hisat2
command = 'Rscript ' + script + ' N2 Spin hisat2'
print(command)
os.system(command)

# N2 SVIP salmon
command = 'Rscript ' + script + ' N2 SVIP salmon'
print(command)
os.system(command)

# N2 SVIP salmon
command = 'Rscript ' + script + ' N2 SVIP hisat2'
print(command)
os.system(command)

# Spin SVIP salmon
command = 'Rscript ' + script + ' Spin SVIP salmon'
print(command)
os.system(command)

# Spin SVIP hisat2
command = 'Rscript ' + script + ' Spin SVIP hisat2'
print(command)
os.system(command)
