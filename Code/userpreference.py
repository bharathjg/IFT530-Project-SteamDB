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

start_time = time.time()

print('hello world')
dirpath = r"C:\Users\govin\Documents\GitHub\IFT530-Project-SteamDB\Datasets-JSON"

game_genre_file = open(os.path.join(dirpath,'steamdb_gameswithgenre.json'))
game_genre = json.load(game_genre_file)
game_genre_df = pd.read_csv(os.path.join(dirpath, 'steamdb_gamegenreDF.csv'))

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
        game_genre_df = game_genre_df.drop('Unnamed: 0', axis=1)
        return df
    except:
        sys.exit('Tried to load CSV File (game genre DF) and failed')

def generate_dicts(fpath):
    try:
        with open(fpath) as csv_file:
            reader=csv,reader(csv_file)
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

    sim_matrix = linear_kernel(user_gamelib_matrix, tfidf_np)

    return user_gamelib_matrix

def generate_recommendations(sample, sim_matrix, inverse_dict, game_genre):
    all_recommendations = []
    pooled_recommendations = []

    print(f'Length of sample is {len(sample1)}')
    for i in range(len(sample)):
        try:
            game_list = list(enumerate(sim_matrix[i]))
            # print(game_list)
            similar_games = list(
                sorted(game_list, key=lambda x: x[1], reverse=True))
            # print(similar_games)
            all_recommendations.append(similar_games[0])
            all_recommendations.append(similar_games[1])
            # all_recommendations.append(similar_games[2])
        except:
            print('Some Key Error with the Game ID')

    # for i, s in similar_games[:15]:
    print('All Recommendations')
    print(all_recommendations[0])
    for i, s in all_recommendations:
        gameid = inverse_dict[str(i)]
        pooled_recommendations.append(game_genre[gameid]['game_name'])
    
    return pooled_recommendations


def main():
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
    sim_matrix = generate_SimilarityMatrix(tfidf_matrix_dense, gameid_idx_dict, sample)

    recommendations = generate_recommendations(sample, sim_matrix, inverse_dict, game_genre)
    print('Printing pooled recommendations:\n')
    for r in recommendations:
        print(r)

if __name__ == "__main__":
    main()

#gameid_idx_dict={}
#with open(os.path.join(dirpath, 'steamdb_gamegenreDF.csv'), encoding='utf-8-sig') as csvf:
#    csvReader = csv.DictReader(csvf)
#    
#    for idx, rows in enumerate(csvReader):
#        gameid_idx_dict.update({rows['GameID']:idx})

#with open(os.path.join(dirpath, 'gameid_idx_dict.csv'), 'w') as csv_file:
#    writer = csv.writer(csv_file)
#    for key, value in gameid_idx_dict.items():
#       writer.writerow([key, value])

with open(os.path.join(dirpath, 'gameid_idx_dict.csv'), 'r') as csv_file:
    reader = csv.reader(csv_file)
    gameid_idx_dict = dict(reader)

inv_map = {v: k for k, v in gameid_idx_dict.items()}

#print(game_genre_df.head(10))
#game_genre_df = pd.DataFrame(columns= ['GameID', 'GameName', 'Genres'])
#for gameid in game_genre:
#    game_name = game_genre[gameid]['game_name']
#    genres = ' '.join(game_genre[gameid]['genres'])
#    if genres == ' ' or genres == '':
#        genres = 'none'
#    game_genre_df = game_genre_df.append({'GameID':gameid, 'GameName':game_name, 'Genres':genres}, ignore_index = True)
#game_genre_df.to_csv(os.path.join(dirpath, 'steamdb_gamegenreDF.csv'))

game_genre_df = game_genre_df.drop('Unnamed: 0', axis=1)
print(game_genre_df.head(15))

orders_file = open(os.path.join(dirpath,'steamdb_ordersV3_json.json'))
orders = json.load(orders_file)

user_game_lib_file = open(os.path.join(dirpath, 'steamdb_user_game_lib.json'))
user_game_lib=json.load(user_game_lib_file)

#for order in orders:
#    userid=orders[order]['customer_id']
#    gameid_list=orders[order]['items']
#    
#    if userid in user_game_lib:
#        games = user_game_lib[userid]
#        for game in games:
#            gameid_list.append(game)
#    
#    user_game_lib.update({userid:gameid_list})

sample1 = user_game_lib['868']
for game in sample1:
    try:
        print(game_genre[game]['genres'])
    except:
        print('Key Error detected')
tfidf_vector = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vector.fit_transform(game_genre_df['Genres'])

print(list(enumerate(tfidf_vector.get_feature_names_out())))
print(tfidf_matrix[:15])
print(tfidf_matrix.shape)
tfidf_np = tfidf_matrix.todense()

print(tfidf_np[0])

user_gamelib_matrix=[]
for game in sample1:
    try:
        idx = int(gameid_idx_dict[game])
        tfidf_score = tfidf_np[idx]
        tfidf_score = tfidf_score.tolist()
        #print(tfidf_score[0])
        user_gamelib_matrix.append(tfidf_score[0])
    except:
        print('Key Error detected')

user_gamelib_matrix = np.asmatrix(user_gamelib_matrix)
print(user_gamelib_matrix)

sim_matrix = linear_kernel(user_gamelib_matrix, tfidf_np)
#sim_matrix_T = linear_kernel(tfidf_np, user_gamelib_matrix)
#print(sim_matrix)
#gameidx = gameid_idx_dict[sample1[0]]
all_recommendations = []
print(f'Length of sample is {len(sample1)}')
for i in range(len(sample1)):
    try:
        game_list = list(enumerate(sim_matrix[i]))
        #print(game_list)
        similar_games = list(sorted(game_list, key=lambda x: x[1], reverse=True))
        #print(similar_games)
        all_recommendations.append(similar_games[0])
        all_recommendations.append(similar_games[1])
        #all_recommendations.append(similar_games[2])
    except:
        print('Some Key Error with the Game ID')
    
#for i, s in similar_games[:15]:
print('All Recommendations')
print(all_recommendations[0])
for i, s in all_recommendations:
   gameid = inv_map[str(i)]
   print(game_genre[gameid]['game_name'])

end_time = time.time()

print("Execution Time: ", end_time-start_time, "seconds")
#np.savetxt(os.path.join(dirpath, 'tfidf_matrix.csv'), tfidf_np, delimiter=',')
# create the cosine similarity matrix
#sim_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)
#print(sim_matrix)


#outfile_name = 'steamdb_user_game_lib.json'
#outfile_path = os.path.join(dirpath,outfile_name)

#with open(outfile_path , 'w', encoding='utf-8') as jsonf:
    #jsonf.write(json.dumps(user_game_lib, indent = 4))