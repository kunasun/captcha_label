import pandas as pd
import os
import csv
import numpy as np
import requests as req
import logging
import json

PATH_TO_CSV = os.path.join("..", "data", "Epidemic_all_debiased.csv")
PATH_TO_NEW_CSV = os.path.join("..", "data", "audio_with_descriptors.csv")
PATH_TO_JSON = os.path.join("..", "data", "audio_data.json")
PATH_TO_AUDIO_TESTS = os.path.join("..", "audio_tests")

def process_original_csv(csv_file, path_to_json):
    '''
    Takes the original 'Epidemic_alldebiased.csv' and only selects the url and epidemic_id columns
    Returns a dictionary 
    '''
    df = pd.read_csv(csv_file, sep=',', quotechar='"', skipinitialspace=True, encoding='utf-8', on_bad_lines='skip')
    df['id'] = df.index
    df = df[['url']]
    
    json_str = df.reset_index().to_json(orient='records', indent=4)
    data = json.loads(json_str)
    for dict in data:
        dict['descriptors'] = {}
    with open(path_to_json, 'w') as f:
        json.dump(data, f, indent=4)
    
def get_rand_audio_from_json(json_file, unique_descriptors_threshold=4):
    logging.info("Getting random audio...")
    with open(json_file, 'r') as f:
        data = json.load(f)
        # print(dict[:5])
        n_data = len(data)
        rand_data_n = np.random.randint(0, n_data)

        audio_url = data[rand_data_n]["url"]
        logging.info("Got audio url: %s", audio_url)
        audio_id = data[rand_data_n]['index']
        logging.info("Got audio id: %s", audio_id)
        audio_descriptors = data[rand_data_n]["descriptors"]
        num_descriptors = len(audio_descriptors)
        logging.info("Got audio_descriptors: %s with %d total descriptors", audio_descriptors, num_descriptors)

    logging.info("Finished getting random audio.")

    has_enough_descriptors = num_descriptors >= unique_descriptors_threshold

    return audio_url, audio_id, has_enough_descriptors

def add_description(description: str, audio_id: int, json_file=PATH_TO_JSON):
    with open(json_file, 'r') as f:
        data = json.load(f)
        row = data[audio_id]
        row['descriptors'][description] = dict.get(row['descriptors'], description, 0) + 1
        # if len(row['descriptors']) == 0:

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)    

def validate_description(description: str, audio_id: int, threshold: int=3, json_file=PATH_TO_JSON):
    with open(json_file, 'r') as f:
        data = json.load(f)
        row = data[audio_id]
        if len(row['descriptors']) == 1:
            add_description(description, audio_id)
            return
        valid_lst = np.array([i for i in row['descriptors'].keys() if row['descriptors'][i] > threshold])
        invalid_lst = np.array([i for i in row['descriptors'].keys() if row['descriptors'][i] <= threshold])
        logging.info("Valid list: %s", valid_lst)
        logging.info("Invalid list: %s", invalid_lst)

        if len(valid_lst) == 0 or len(invalid_lst) < 3:
            add_description(description, audio_id)
            return

        invalid_choices = np.random.choice(invalid_lst, size=3, replace=False)
        valid_choice = np.random.choice(valid_lst, size=1, replace=False)
        multiple_choice = np.concatenate((valid_choice, invalid_choices))
        np.random.shuffle(multiple_choice)
        logging.info("Multiple Choice Selections: %s", multiple_choice)
        return multiple_choice 


#preprocess the data such that no caps, spaces, etc (dictionary counts are accurate)
# def validate_description(description: str, audio_id: int, threshold: int=3):
#     df = pd.read_csv(PATH_TO_NEW_CSV, sep=',', quotechar='"', skipinitialspace=True, encoding='utf-8', on_bad_lines='skip')
#     row_numbers = df.index[df['epidemic_id'] == audio_id].values[0]
#     description_lst = df['descriptors'][row_numbers]
    
#     if len(description_lst) == 1:
#         add_description(description, audio_id)

#     valid_lst = {k: v for k, v in description_lst.items() if int(k) > threshold}
#     invalid_lst = {k: v for k, v in description_lst.items() if int(k) <= threshold}
    
#     rand_description_correct = np.random.randint(0, len(valid_lst))
#     rand_description_incorrects = np.random.randint(0, len(invalid_lst),min(3, len(invalid_lst)))

#     multiple_choice = [rand_description_correct]
#     multiple_choice.extend(rand_description_incorrects)
#     return multiple_choice 
    
    

def get_CAPTCHA():
    # return get_random_audio_from_csv(PATH_TO_NEW_CSV)
    return get_rand_audio_from_json(PATH_TO_JSON)

def main():
    process_original_csv(PATH_TO_CSV, PATH_TO_JSON)
    get_rand_audio_from_json(PATH_TO_JSON)
    add_description("swag", 1)
    add_description("swag", 1)
    add_description("swag", 1)
    add_description("bru", 1)
    add_description("stuff", 1)
    add_description("things", 1)
    validate_description("swag", 1)
    validate_description("swag", 1)
    add_description("a", 1)
    add_description("b", 1)
    add_description("c", 1)
    add_description("d", 1)
    add_description("bru", 1)
    add_description("bru", 1)
    add_description("bru", 1)
    validate_description("swag", 1)


    pass

if __name__ == "__main__":
    logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)
    logging.info("Started")
    main()
    logging.info("Ended")
