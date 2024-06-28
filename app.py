import streamlit as st
import pickle
import pandas as pd

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movie = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')

option = st.selectbox(
    'Type the movie name you want to search:', movie['title'].values
)