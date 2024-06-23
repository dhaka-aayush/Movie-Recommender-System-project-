import numpy as np
import pandas as pd
import ast

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