import pandas as pd
import streamlit as st

@st.cache_data
def load_food_data():
    df = pd.read_csv("data/food_data.csv")
    df = df.dropna(subset=['calories', 'protein', 'carbs', 'fat'])
    df = df[pd.to_numeric(df['calories'], errors='coerce') > 0]
    return df