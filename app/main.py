'''
Pull down the imbd_movies dataset here and save to /data as imdb_movies_2000to2022.prolific.json
You will run this project from main.py, so need to set things up accordingly
'''

from pathlib import Path
import requests
from json_cleanup import cleanup
from analysis_network_centrality import centrality
from analysis_similar_actors_genre import similarity


# Ingest and save the imbd_movies dataset frpm https://raw.githubusercontent.com/cbuntain/umd.inst414/main/data/imdb_movies_2000to2022.prolific.json
def ingest():
    '''
    Ingest function to pull imbd json data from website and save it for analysis
    '''

    # Sets the url and download parameters to collect the raw JSON file
    url:str = 'https://raw.githubusercontent.com/cbuntain/umd.inst414/main/data/imdb_movies_2000to2022.prolific.json'
    download_settings:dict = {"downloadformat": "json"}

    # Requests data from imbd site
    response:requests = requests.get(url, params = download_settings, timeout = 90)

    # Creates reference to current folder, for use in providing relative folder references to other files
    main_folder:Path = Path(__file__).absolute().parent

    # Saves requested file in /data directory for processing and further use
    with open(main_folder / "../data/imdb_movies_2000to2022.prolific.json", mode = "wb") as file:
        file.write(response.content)


# Call functions / instanciate objects from the two analysis .py files
def main():
    '''
    Main function

    Runs through the steps to ingest, cleanup, and analyze imbd json data
    '''
    ingest()
    cleanup()
    centrality()
    similarity()



if __name__ == "__main__":
    main()