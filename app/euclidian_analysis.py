'''
Setup to test the feature matrix using eucildian distance instead of cosine
'''

from pathlib import Path
from sklearn.metrics import DistanceMetric
from datetime import datetime
import pandas as pd

# Creates reference to current folder, for use in providing relative folder references to other files
main_folder:Path = Path(__file__).absolute().parent

# Opens requested file in /data directory to process genres
with open(main_folder / "../data/actor_genre_test_240725_0043.csv", mode = "r", encoding = 'UTF-8') as file:

    # Reads CSV file into dataframe
    euclidean_matrix:pd = pd.read_csv(file, sep = '\t')

# For testing Substituting Chris Hemsworth as the 'query' for testing
query_actor:str = 'Chris Hemsworth'

# Converting the query name to the Dataframe index for their line of data
query_index:int = euclidean_matrix.index.astype(int)[euclidean_matrix['Actor_Name'] == query_actor]

# Extracting query actor's data and removing Actor_Name and Actor_ID for distance analysis
query_matrix:pd = euclidean_matrix.loc[query_index]
query_matrix.drop(['Actor_Name', 'Actor_ID'], axis = 1, inplace = True)

# Create feature matrix and remove Actor_Name and Actor_ID for distance analysis
feature_matrix:pd = euclidean_matrix.copy()
feature_matrix.drop(['Actor_Name', 'Actor_ID'], axis = 1, inplace = True)

# Running euclidean DistanceMetric on matrices
euclidean_distance:DistanceMetric = DistanceMetric.get_metric('euclidean')
calculated_distances:int = euclidean_distance.pairwise(feature_matrix.to_numpy(), query_matrix.to_numpy())        

# Adding calculated distances back into euclidean_matrix dataframe
euclidean_matrix.loc[:,'Euclidean_Distances'] = calculated_distances

# Creating cosine Dataframe for output
cosine_results:pd = euclidean_matrix.copy()
cosine_results.sort_values('Cosine_Distances', inplace = True)

# Removing genre columns
existing_columns:list = list(euclidean_matrix.columns)
del existing_columns[0:2]
cosine_results.drop(existing_columns, axis = 1, inplace = True)

print(cosine_results.head(10))

# Setup complete relative location for '/data'
current_time:datetime = datetime.now()
file_time:str = current_time.strftime('%y%m%d_%H%M')
cosine_file_name:str = 'cosine_top_10_' + file_time + '.csv'

# Output the final dataframe to a CSV named 'cosine_top_10_{current_datetime}.csv' to `/data`
cosine_results.head(10).to_csv(main_folder / "../data" / cosine_file_name, sep = '\t', encoding =  'UTF-8')

# Creating eulcidian Dataframe for output
euclidean_results:pd = euclidean_matrix.copy()
euclidean_results.sort_values('Euclidean_Distances', inplace = True)

# Removing genre columns
existing_columns:list = list(euclidean_matrix.columns)
del existing_columns[0:2]
euclidean_results.drop(existing_columns, axis = 1, inplace = True)

print(euclidean_results.head(10))

# Setup complete relative location for '/data'
euclidean_file_name:str = 'euclidean_top_10_' + file_time + '.csv'

# Output the final dataframe to a CSV named 'cosine_top_10_{current_datetime}.csv' to `/data`
euclidean_results.head(10).to_csv(main_folder / "../data" / euclidean_file_name, sep = '\t', encoding =  'UTF-8')