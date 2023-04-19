import pandas as pd

#make sure to cd to correct directory
aln_dir = '.'
df = pd.DataFrame(columns=['Name'])
libs = ['Wt','DecWt','P384R']
for lib in libs:
    for rep in [1, 2, 3]:
        print(f"{lib}-{rep}")
        this_df = pd.read_csv(f"{aln_dir}/{lib}-{rep}_salmon_quant/quant.genes.sf", sep='\t')
        this_df = this_df[['Name','NumReads']]
        this_df.rename(columns={'NumReads':f"{lib}_{rep}"}, inplace=True)
        #print(this_df.head(2))
        df = df.merge(this_df, how='outer', on='Name')
df.rename(columns={'Name':'gene_id'}, inplace=True)
#df.head()

df = df.sort_values(by='gene_id')
df.to_csv(aln_dir + '/salmon.gene_counts.tsv', sep='\t', index=False)
