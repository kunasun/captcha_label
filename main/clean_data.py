import pandas as pd
import os
import csv
import numpy as np
import requests as req
import logging
import json
from get_audio import process_original_csv

PATH_TO_CSV = os.path.join("..", "data", "Epidemic_all_debiased.csv")
PATH_TO_NEW_CSV = os.path.join("..", "data", "audio_with_descriptors.csv")
PATH_TO_JSON = os.path.join("..", "data", "audio_data.json")
PATH_TO_AUDIO_TESTS = os.path.join("..", "audio_tests")

process_original_csv(PATH_TO_CSV, PATH_TO_JSON)