import pandas as pd
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

def preprocessing():
	# obtain file names
	years = [2013,2014,2015,2016,2017,2018]
	file_directory = '/Users/yuxinchen/Documents/Research/data_projects/data/health_ranks_data/csv_files/*.csv'
	import glob
	files = sorted(glob.glob(file_directory, recursive=True))

	# obtain dataframes from the csv files and remove some unnecessary columns
	dfs = []
	df_columns = []
	unnecessary_columns = ['95% CI', 'Z-Score']
	for file in files:
	    df = pd.read_csv(file)
	    columns = df.columns.values
	    # remove unnecessary columns
	    for string in unnecessary_columns:
	        cols_to_keep = [c for c in df.columns.values if not string in c]        
	        df = df[cols_to_keep]
	#     # remove columns that have too many missing values
	#     num_nan = df.isna().sum()
	#     for ind in range(num_nan.shape[0]):
	#         perc_nan = num_nan[ind]/df.shape[0]
	#         if perc_nan > 0.6:
	#             df = df.drop(num_nan.index[ind],axis = 1)
	    dfs.append(df)

	# find intersectin of columns in dfs
	col_list = []
	for df in dfs:
	    col = df.columns.values
	    col_list.append(col)
	from functools import reduce
	common_cols = list(reduce(set.intersection, [set(item) for item in col_list ]))

	# remove the columns in each dataframe of dfs that are not in common_cols
	for ind, df in enumerate(dfs):
	    df = df.loc[:,common_cols]
	    dfs[ind] = df

	# combine all dataframes into one
	df = pd.concat(dfs)
	# drop duplicated columns
	df.drop(['Physically Unhealthy Days', 'Unnamed: 0', '# Some College', 'Dentist Ratio', '# Dentists','PCP Ratio', '# Households', '# Unemployed','# Uninsured','# Single-Parent Households', '# Limited Access'], axis = 1, inplace = True)


	# convert columns that have number into population percentage
	for col in df.columns.values:
	    if '#' in col:
	        df[col] = df[col]/df['Population']

	correlation = df.loc[:, (df.columns!='FIPS') & (df.columns!='Labor Force')].select_dtypes(include = [np.number]).corr()

	k = 16 #number of effective variables for heatmap
	cols = abs(correlation).nlargest(k, '% Fair/Poor')['% Fair/Poor'].index

	total = df.isnull().sum().sort_values(ascending=False)
	percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
	missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])


	# delete the variable with more than 15% missing data
	df = df.drop((missing_data[missing_data['Percent'] > 0.15]).index,1)

	# delete rows with missing data
	df.dropna(inplace=True)

	return cols, df

if __name__ == '__main__':
	main()
else:
	pass

