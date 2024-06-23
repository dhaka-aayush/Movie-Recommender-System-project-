import numpy as np
import pandas as pd
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = movies.merge(credits,on='title')
print(movies.head())