import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)

gene_id_file = '~/db/Dmel/dmel_r6.39/dmel-all-r6.39.gtf.gene_id'
gene_ids = pd.read_csv(gene_id_file, header=None)[0].tolist() 

aln_dir = 'hisat2_alns'
df = pd.DataFrame(columns=['Geneid'])
for sample in ["Wt-1","Wt-2","Wt-3","DecWt-1","DecWt-2","DecWt-3","P384R-1","P384R-2","P384R-3"]:
    print(sample)
    bam_file = f"{aln_dir}/{sample}.bam"
    bam_file_name = sample + '.bam'
    count_file = f"{bam_file}.featureCounts.primary.counts"
    this_df = pd.read_csv(count_file, skiprows=1, sep='\t')[['Geneid',bam_file_name]]
    this_df.rename(columns={bam_file_name:sample}, inplace=True)
    this_df = this_df[this_df['Geneid'].isin(gene_ids)]
    #this_df[sample] = this_df[sample]/2 # novogene has half the counts - *** need to double check this - they are probably saying that paired-end = 2
    df = df.merge(this_df, on='Geneid', how='outer')
    
df = df.round(2)
df.rename(columns={'Geneid':'gene_id'}, inplace=True)
#print(df.head())

# output
out_dir = '.'
df.to_csv(out_dir + '/hisat2.gene_counts.tsv', sep='\t', index=False)
