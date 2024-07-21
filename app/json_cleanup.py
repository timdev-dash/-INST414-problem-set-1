'''
Due to apparent structural issues within the provided JSON, a cleanup method must be run to create data that is operable
'''

import json
from pathlib import Path

def cleanup():
    '''
    cleanup method
    
    Returns
    clean (list): list of data contained within the json that can now be read'''

    #Instanciate the list to be returned following data cleanup
    cleansed:list = []

    # Creates reference to current folder, for use in providing relative folder references to other files
    main_folder:Path = Path(__file__).absolute().parent

    # Opens requested file in /data directory to cleanup formatting
    with open(main_folder / "../data/imdb_movies_2000to2022.prolific.json", mode = "rb") as file:
        for line in file:
            cleansed.append(json.loads(line))

    newjson:str = json.dumps(cleansed)

    # Saves cleansed json to old file, replacing old formatting
    with open(main_folder / "../data/imdb_movies_2000to2022.prolific.json", mode = "w", encoding = 'UTF-8') as file:
        file.write(newjson)

if __name__ == '__main__':
    cleanup()