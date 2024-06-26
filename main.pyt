import numpy as np
import pandas as pd
import pickle
import ast
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
ps = PorterStemmer()

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = movies.merge(credits,on='title')

# (genres , id , keywords , title , overview , cast , crew)

movies = movies[['genres','id','keywords','title','overview','cast','crew']]
movies.dropna(inplace=True)

# print(movies.duplicated().sum())   ,checked duplicates in database

def convert(obj):
    list1 = []
    for i in ast.literal_eval(obj):
        list1.append(i['name'])
    return list1

movies['genres']= movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

def convert3(obj):
    list1 = []
    count = 0
    for i in ast.literal_eval(obj):
        if count !=3 :
           list1.append(i['name'])
           count+=1
        else:
            break
    return list1

movies['cast'] = movies['cast'].apply(convert3)

def fetch_director(obj):
    list1 = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            list1.append(i['name'])
            break
    return list1

movies['crew'] = movies['crew'].apply(fetch_director)

movies['overview'] = movies['overview'].apply(lambda x:x.split())

movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])

movies['tags'] = movies['overview'] + movies['keywords'] + movies['genres'] + movies['crew'] + movies['cast']

new_movie_df = movies[['id' , 'title' , 'tags']]

new_movie_df['tags'] = new_movie_df['tags'].apply(lambda x:" ".join(x))

new_movie_df['tags'] = new_movie_df['tags'].apply(lambda x:x.lower())

cv = CountVectorizer(max_features=5000,stop_words='english')
vectors = cv.fit_transform(new_movie_df['tags']).toarray()

def stem(item):
    y = []
    for i in item.split():
        y.append(ps.stem(i))

    return " ".join(y)

new_movie_df['tags'] = new_movie_df['tags'].apply(stem)

similarity = cosine_similarity(vectors)

def recommend(movie):
    movie_index = new_movie_df[new_movie_df['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True , key = lambda x:x[1])[1:6]

    for i in movie_list:
        print(new_movie_df.iloc[i[0]].title)

pickle.dump(new_movie_df.to_dict(),open('movies_dict.pkl','wb'))