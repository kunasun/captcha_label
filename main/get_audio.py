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
    

# def get_random_audio_from_csv(csv_file, unique_descriptors_threshold=4):
#     '''
#     Takes in a .csv file csv_file
#     Returns a .mp3 file, audio_id, and True/False if any descriptors exist
#     '''
#     logging.info("Getting random audio...")
#     df = pd.read_csv(csv_file, sep=',', quotechar='"', skipinitialspace=True, encoding='utf-8')
#     num_rows = len(df)
#     rand_row_n = np.random.randint(0, num_rows)
    
#     audio_url = df['url'][rand_row_n]
#     audio_id = df['epidemic_id'][rand_row_n]
#     audio_descriptors = df['descriptors'][rand_row_n]

#     has_enough_descriptors = not np.isnan(audio_descriptors) and len(audio_descriptors) >= unique_descriptors_threshold
#     logging.info("Got audio with: url=%s and id=%s and has_enough_descriptors=%s", audio_url, audio_id, has_enough_descriptors)
#     logging.info("Finished getting random audio.")

#     return audio_url, audio_id, has_enough_descriptors
    
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

#how do we know which row to update? use audio_id
def add_description(description: str, audio_id: int):
    '''
    Add a given description to the given audio_id or increment its count
    Increment total descriptors_count
    '''
    logging.info("Adding description %s to audio_id=%d", description, audio_id)
    df = pd.read_csv(PATH_TO_NEW_CSV, sep=',', quotechar='"', skipinitialspace=True, encoding='utf-8')
    print(df.head)
    row_number = df.index[df['epidemic_id'] == audio_id].values[0]
    print(df.iloc[row_number])
    if pd.isnull(df.iloc[row_number]['descriptors']):
        # df.loc[row_number, 'descriptors'] = [{description: 1}]
        print(df.iloc[row_number]['descriptors'])
        df.loc[row_number, 'descriptors'] = [{description: 1}]
    else:
        print("ELSE", df['descriptors'][row_number])
        print(df['descriptors'][row_number])
        dic = json.loads(df['descriptors'][row_number])
        dic[description] += 1
        df.loc[row_number, 'descriptors'] = [dic]
    df.loc[row_number, 'total_descriptors'] += 1
    print(df.iloc[row_number])
    print("ROW", df['descriptors'][row_number])
    logging.info("Finished adding description %s to audio_id=%d. Count is %d", description, audio_id, df['descriptors'][row_number][description])
    df.to_csv(PATH_TO_NEW_CSV, index=False)

#preprocess the data such that no caps, spaces, etc (dictionary counts are accurate)
def validate_description(description: str, audio_id: int, threshold: int=3):
    df = pd.read_csv(PATH_TO_NEW_CSV, sep=',', quotechar='"', skipinitialspace=True, encoding='utf-8', on_bad_lines='skip')
    row_numbers = df.index[df['epidemic_id'] == audio_id].values[0]
    description_lst = df['descriptors'][row_numbers]
    
    if len(description_lst) == 1:
        add_description(description, audio_id)

    valid_lst = {k: v for k, v in description_lst.items() if int(k) > threshold}
    invalid_lst = {k: v for k, v in description_lst.items() if int(k) <= threshold}
    
    rand_description_correct = np.random.randint(0, len(valid_lst))
    rand_description_incorrects = np.random.randint(0, len(invalid_lst),min(3, len(invalid_lst)))

    multiple_choice = [rand_description_correct]
    multiple_choice.extend(rand_description_incorrects)
    return multiple_choice 
    
    

def get_CAPTCHA():
    return get_random_audio_from_csv(PATH_TO_NEW_CSV)

def main():
    process_original_csv(PATH_TO_CSV, PATH_TO_JSON)
    get_rand_audio_from_json(PATH_TO_JSON)
    # get_random_audio_from_csv(PATH_TO_NEW_CSV)
    # add_description("swag", 130947)
    # add_description("swag", 130947)
    # add_description("swag", 130947)
    # add_description("bru", 130947)
    # add_description("stuff", 130947)
    # add_description("things", 130947)

    pass

if __name__ == "__main__":
    logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)
    logging.info("Started")
    main()
    logging.info("Ended")
