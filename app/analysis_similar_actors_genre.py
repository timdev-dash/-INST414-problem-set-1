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

# Setup of dataframe to contain actor/genre counts
actors_genres:pd = pd.DataFrame(columns = ['Actor_Name', 'Actor_ID'])
actors_genres.reset_index()

# Creates reference to current folder, for use in providing relative folder references to other files
main_folder:Path = Path(__file__).absolute().parent

# Opens requested file in /data directory to process actors
with open(main_folder / "../data/imdb_movies_2000to2022.prolific.json", mode = "r", encoding = 'UTF-8') as file:
       
    # Reading through the file to extract the list of movies for processing
    for items in file:

        movies = json.loads(items)

        # Reading through each movie to extract and save genre and actor data
        for this_movie in movies:

                # Setting genre interator and loop length for genre adding loop
                genre:int = 0
                genre_list_length: int = len(this_movie['genres'])

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
                                if genre_test[test_number] == False:
                                        genre_needs_inclusion = True
                                else:
                                        genre_needs_inclusion = False
                                        break

                                test_number += 1


                        # If the genre has not yet been added to the dataframe as a column (genre_exits == False)
                        # add it as a new column
                        if genre_needs_inclusion:
                                actors_genres.insert(number_of_columns, genre_name, 0)
                        else:
                                pass

                        # Iterate genre count
                        genre += 1
        
                # Setting actor iterator and loop lenght for node adding loop
                actor:int = 0
                actors_list_length:int = len(this_movie['actors'])

                # Checks to see if actor's name already exists in a row
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
                                if actor_test[test_number] == False:
                                        actor_needs_inclusion = True
                                else:
                                        actor_needs_inclusion = False
                                        break

                                test_number += 1


                        # If the actor has not yet been added to the dataframe as a row (actor_exits == False)
                        # add it as a new row
                        if actor_needs_inclusion:
                                row_for_inclusion = pd.DataFrame([{'Actor_Name' : actor_name, 'Actor_ID' : actor_id}])
                                actors_genres = actors_genres._append(row_for_inclusion, ignore_index = True)
                        else:
                                pass
                        
                        with open('log.txt', mode = 'a', encoding = 'UTF-8') as file:
                               file.write(actor_name + '\n')
                        # Iterate genre count
                        actor += 1
                # Iterate through the list of actors, generating all pairs
                i:int = 0
                

print(actors_genres.head(15))