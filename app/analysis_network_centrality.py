'''
PART 1: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Guild a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to. 
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is line with the standards we're using in this class 
'''

import json
from pathlib import Path
import pandas as pd
import networkx as nx
from datetime import datetime

def centrality():
    '''
    Performs centrality analysis of actors contained in the imdb json dataset
    '''

    # Build the graph
    actors_graph:nx = nx.Graph()

    # Set up your dataframe(s) -> the df that's output to a CSV should include at least the columns 'left_actor_name', '<->', 'right_actor_name'
    actors_data:pd = pd.DataFrame(columns= [ 'left_actor_name' , '<->', 'right_actor_name'])
    actors_data.reset_index()

    # Creates reference to current folder, for use in providing relative folder references to other files
    main_folder:Path = Path(__file__).absolute().parent

    # Opens requested file in /data directory to process actors
    with open(main_folder / "../data/imdb_movies_2000to2022.prolific.json", mode = "r", encoding = 'UTF-8') as file:
        
        # Reading through the file to extract the list of movies for processing
        for items in file:

            movies = json.loads(items)

            # Reading through each movie to extract and save actor relationship data
            for this_movie in movies:
        
                # Setting actor iterator and loop length for node adding loop
                actor:int = 0
                actors_list_length:int = len(this_movie['actors'])

                # Create a node for every actor
                while actor < actors_list_length:
                    
                    # Setting the current actor in the loop
                    actor_id:str = this_movie['actors'][actor][0]
                    actor_name:str = this_movie['actors'][actor][1]

                    # Check to see if the actor has already been added to the graph as a node
                    if actor_name in actors_graph:
                        break
                    else:
                        # add the actor to the graph
                        actors_graph.add_node(actor_name, id = actor_id)
                    
                # Iterate through the list of actors, generating all pairs
                i:int = 0

                # Iterating through all but last actor to build out pairs
                while i < actors_list_length - 1:

                    # Setting values for first actor in pairs
                    left_actor_name:str = this_movie['actors'][i][1]

                    # Setting iterator value for right actor loop
                    j:int = i + 1

                    # Looping through remaining actors in the movie to create pairs
                    while j < actors_list_length:
                        
                        # Setting values for right actor in current pair
                        right_actor_name:str = this_movie['actors'][j][1]

                        # Adding the actor pair to the graph using the movie title as an edge label
                        actors_graph.add_edge( left_actor_name, right_actor_name, label=this_movie['title'])

                        # Adding the actor pair to the dataframe
                        ### actors_data.append([left_actor_name, '<->', right_actor_name], ignore_index = True)
                        actors_data.loc[len(actors_data.index)] = [left_actor_name, '<->', right_actor_name]

                        # Stepping the second actors iterator up by one
                        j += 1

                    # Stepping the first actor's interator up by one
                    i += 1

    # Print the info below
    print("Nodes:", len(actors_graph.nodes))

    # Creating dataframe for actor centrality
    list_of_centrality:list = []
    centrality_results:dict = nx.degree_centrality(actors_graph)

    # Looping through the graph to create list to bring into the dataframe
    index:int = 0

    for actor, centrality_rating in centrality_results.items():
        list_of_centrality.append([actor, centrality_rating])
        index += 1

    # Creation of the dataframe
    actor_centrality:pd = pd.DataFrame(list_of_centrality, columns=['Actor Name', 'Centrality'])

    # Deep copy to organize results by highest centrality
    most_central:pd = actor_centrality.copy()

    #Print the 10 the most central nodes
    print(most_central.head(10).sort_values(by = 'Centrality', ascending = False))

    # Setup complete relative location for '/data'
    current_time:datetime = datetime.now()
    file_time:str = current_time.strftime('%y%m%d_%H%M')
    output_file_name:str = 'network_centrality_' + file_time + '.csv'

    # Output the final dataframe to a CSV named 'network_centrality_{current_datetime}.csv' to `/data`
    actors_data.to_csv(main_folder / "../data" / output_file_name, sep = '\t', encoding =  'UTF-8')
