'''
PART 2: SIMILAR ACTROS BY GENRE
Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

import pandas as pd
import networkx as nx
import json
from pathlib import Path
from datetime import datetime

# Setup of dataframe to contain actor/genre counts
actors_genres:pd = pd.DataFrame(columns = ['Actor_Name', 'Actor_ID'])
actors_genres.reset_index()

# Creates reference to current folder, for use in providing relative folder references to other files
main_folder:Path = Path(__file__).absolute().parent

# Opens requested file in /data directory to process genres
with open(main_folder / "../data/imdb_movies_2000to2022.prolific.json", mode = "r", encoding = 'UTF-8') as file:
    
    # Reading through the file to extract the list of movies for processing
    for items in file:

        movies = json.loads(items)

        # Reading through each movie to extract and save genre data
        for this_movie in movies:

                # Setting genre interator and loop length for genre adding loop
                genre:int = 0
                genre_list_length: int = len(this_movie['genres'])
                added_genres:list = []

                # Checking to see if this movie's genres already exist as columns
                while genre < genre_list_length:

                        # Setting the current genre in the loop
                        genre_name: str = this_movie['genres'][genre]

                        # Pulling the current list of column names for comparison and setting the column iterator
                        existing_genres:list = list(actors_genres.columns)
                        column:int = 0
                        number_of_columns = len(existing_genres)
                        genre_test:list = []

                        # Checking to see if the genre has already been added to the dataframe as a column
                        while column < number_of_columns:
                                if existing_genres[column] == genre_name:
                                        genre_test.append(True)
                                else:
                                        genre_test.append(False)

                                # Iterate the column number
                                column += 1

                        # Reviewing test results to determine if genre needs to be added
                        test_number:int = 0
                        number_of_tests:int = len(genre_test)
                        while test_number < number_of_tests:
                                if genre_test[test_number] is False:
                                        genre_needs_inclusion = True
                                else:
                                        genre_needs_inclusion = False
                                        break

                                test_number += 1


                        # If the genre has not yet been added to the dataframe as a column (genre_exits == False)
                        # add it as a new column
                        if genre_needs_inclusion:
                                actors_genres.insert(number_of_columns, genre_name, 0)
                                added_genres.append(genre_name)
                        else:
                                pass

                        # Iterate genre count
                        genre += 1

# Opens requested file in /data directory to process actors
with open(main_folder / "../data/imdb_movies_2000to2022.prolific.json", mode = "r", encoding = 'UTF-8') as file:

    # Reading through the file to extract the list of movies for processing
    for items in file:

        # Extracting movies from file
        movies = json.loads(items)

        # Building the default genre count for use when initially adding actors
        default_genre_length:int = len(added_genres)
        step:int = 0
        default_genre_count:dict = {}

        while step < default_genre_length:
               default_genre_count.update({added_genres[step] : 0})
               step += 1

        # Reading through each movie to extract and save actor data
        for this_movie in movies:

                # Setting actor iterator and loop length for actor adding and update loop
                actor:int = 0
                actors_list_length:int = len(this_movie['actors'])

                # Evaluate if actor needs to be added to dataframe, then update genre count
                while actor < actors_list_length:
                        
                        # Setting the current actor in the loop
                        actor_id:str = this_movie['actors'][actor][0]
                        actor_name:str = this_movie['actors'][actor][1]

                        # Pulling the current list of row names for comparison and setting the column iterator
                        existing_actors:int = actors_genres.shape[0]
                        row:int = 0
                        actor_test:list = []
                        actor_needs_inclusion:bool = True
                        
                        # Checking to see if the actor has already been added to the dataframe as a column
                        while row < existing_actors:
                                if actors_genres.loc[row,'Actor_Name'] == actor_name:
                                        actor_test.append(True)
                                else:
                                        actor_test.append(False)

                                # Iterate the column number
                                row += 1
                        
                        # Reviewing test results to determine if actor needs to be added
                        test_number:int = 0
                        number_of_tests:int = len(actor_test)
                        while test_number < number_of_tests:
                                if actor_test[test_number] is False:
                                        actor_needs_inclusion = True
                                else:
                                        actor_needs_inclusion = False
                                        break

                                test_number += 1


                        # If the actor has not yet been added to the dataframe as a row (actor_exits == False)
                        # add it as a new row
                        if actor_needs_inclusion:
                                
                                # Build the start of the new actor's row
                                dict_for_inclusion:dict = {'Actor_Name' : actor_name, 'Actor_ID': actor_id}

                                # Add the zero count for each genre to the row
                                dict_for_inclusion.update(default_genre_count)
                                row_for_inclusion = pd.DataFrame([dict_for_inclusion])
                                actors_genres = actors_genres._append(row_for_inclusion, ignore_index = True)
                        else:
                                pass
                        
                        # Update the genre count for the actor to account for this movie's genres

                        # Setup loop to review genres
                        genre:int = 0
                        genre_list_length: int = len(this_movie['genres'])

                        #### Use dataframe.loc using the actor name to recall, iterate and update the genre count value for each genre
                        # Loop through genres for this movie to recall, iterate, and update actor's count
                        while genre < genre_list_length:
                               
                               # Get the dataframe index for the current actor
                               actor_index: int = actors_genres[actors_genres['Actor_Name'] == actor_name].index[0]
                               
                               # Get the current count for the genre from the dataframe and increment it by 1
                               current_count:int = actors_genres[this_movie['genres'][genre]].loc[actors_genres.index[actor_index]]
                               new_count:int = current_count + 1

                               # Update the dataframe with the new count
                               actors_genres.loc[actors_genres['Actor_Name'] == actor_name, this_movie['genres'][genre]] = new_count

                               # Iterate the genre counter
                               genre += 1

                        # Iterate actor count
                        actor += 1
                # Iterate through the list of actors, generating all pairs
                i:int = 0
                
print(actors_genres.head(15))

# Setup complete relative location for '/data'
current_time:datetime = datetime.now()
file_time:str = current_time.strftime('%y%m%d_%H%M')
output_file_name:str = 'actor_genre_test_' + file_time + '.csv'

# Output the final dataframe to a CSV named 'network_centrality_{current_datetime}.csv' to `/data`
actors_genres.to_csv(main_folder / "../data" / output_file_name, sep = '\t', encoding =  'UTF-8')
