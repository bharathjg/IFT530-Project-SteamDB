import csv
import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import time
import sys


def load_JSONFile(fpath):
    file = open(fpath)
    try:
        file_json = json.load(file)
        print(f'Loaded file: {fpath}')
        return file_json
    except:
        sys.exit('Tried to load JSON file and failed')


def generate_dataframe(fpath):
    try:
        df = pd.read_csv(fpath)
        print(f'Loaded file: {fpath}')
        #game_genre_df = game_genre_df.drop('Unnamed: 0', axis=1)
        return df
    except:
        sys.exit('Tried to load CSV File (game genre DF) and failed')


def generate_dicts(fpath):
    try:
        with open(fpath, 'r') as csv_file:
            reader = csv.reader(csv_file)
            print(f'Loaded file: {fpath}')
            gameid_idx_dict = dict(reader)

            inverse_dict = {v: k for k, v in gameid_idx_dict.items()}

        return gameid_idx_dict, inverse_dict
    except:
        sys.exit('Tried to load CSV file (gameid - index) and failed')


def generate_TFIDFMatrix(game_genre_df):
    tfidf_vector = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vector.fit_transform(game_genre_df['Genres'])
    tfidf_np = tfidf_matrix.todense()
    return tfidf_np


def generate_SimilarityMatrix(TFIDF_Matrix_Dense, gameid_idx_dict, sample):
    user_gamelib_matrix = []

    for game in sample:
        try:
            idx = int(gameid_idx_dict[game])
            tfidf_score = TFIDF_Matrix_Dense[idx]
            tfidf_score = tfidf_score.tolist()
            # print(tfidf_score[0])
            user_gamelib_matrix.append(tfidf_score[0])
        except:
            print('Key Error detected')

    user_gamelib_matrix = np.asmatrix(user_gamelib_matrix)

    sim_matrix = linear_kernel(user_gamelib_matrix, TFIDF_Matrix_Dense)

    return sim_matrix


def generate_recommendations(sample, sim_matrix, inverse_dict, game_genre):
    all_recommendations = []
    pooled_recommendations = []

    print(f'Length of sample is {len(sample)}')
    for i in range(len(sample)):
        try:
            game_list = list(enumerate(sim_matrix[i]))
            similar_games = list(sorted(game_list, key=lambda x: x[1], reverse=True))
            all_recommendations.append(similar_games[0])
            all_recommendations.append(similar_games[1])
        except:
            print(f'Some Key Error with some Game ID, skipping over')

    print('All Recommendations')
    for i, s in all_recommendations:
        gameid = inverse_dict[str(i)]
        pooled_recommendations.append(game_genre[gameid]['game_name'])

    return pooled_recommendations


def main():
    start_time = time.time()

    dirpath = r"C:\Users\govin\Documents\GitHub\IFT530-Project-SteamDB\Datasets-JSON"
    fname_gamegenre = 'steamdb_gameswithgenre.json'
    fname_orders = 'steamdb_ordersV3_json.json'
    fname_gamelib = 'steamdb_user_game_lib.json'
    fname_gameindexdict = 'gameid_idx_dict.csv'
    fname_gamegenredf = 'steamdb_gamegenreDF.csv'

    game_genre = load_JSONFile(os.path.join(dirpath, fname_gamegenre))
    orders = load_JSONFile(os.path.join(dirpath, fname_orders))
    user_game_lib = load_JSONFile(os.path.join(dirpath, fname_gamelib))
    gameid_idx_dict, inverse_dict = generate_dicts(os.path.join(dirpath, fname_gameindexdict))
    game_genre_df = generate_dataframe(os.path.join(dirpath, fname_gamegenredf))

    sample = user_game_lib['868']

    tfidf_matrix_dense = generate_TFIDFMatrix(game_genre_df)
    sim_matrix = generate_SimilarityMatrix(
        tfidf_matrix_dense, gameid_idx_dict, sample)

    recommendations = generate_recommendations(
        sample, sim_matrix, inverse_dict, game_genre)
    print('Printing pooled recommendations:\n')
    for r in recommendations:
        print(r)
    
    end_time = time.time()

    print('Execution Time: ', end_time-start_time, "seconds")


if __name__ == "__main__":
    main()
