import streamlit as st
import pandas as pd

# Import pages
from pages_code.auth import show_auth_page
from pages_code.calculator import show_calculator_page
from pages_code.chatbot import show_chatbot_page
from pages_code.input_form import show_input_form
from pages_code.meal_planner import show_meal_planner_page
from pages_code.home import show_home_page
from utils.meal_planner_utils import MealPlanner
from data.food_data import load_food_data

food_data = load_food_data()
planner = MealPlanner(food_data)

# Load data from CSV
@st.cache_data
def load_food_data():
    return pd.read_csv("data/food_data.csv")


# Load data from CSV
@st.cache_data
def load_food_data():
    return pd.read_csv("data/food_data.csv")

@st.cache_data
def load_faq_data():
    return pd.read_csv("data/faq_data.csv")

# Load datasets once and store in session_state
if 'FOOD_DATA' not in st.session_state:
    st.session_state.FOOD_DATA = load_food_data()
if 'FAQ_DATA' not in st.session_state:
    st.session_state.FAQ_DATA = load_faq_data()

# Main entry point
def main():
    # Initialize session variables
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None

    st.set_page_config(page_title="Smart AI Nutrition Assistant", page_icon="🥗", layout="wide")
    
    # Sidebar Navigation
    st.sidebar.title("🥗 Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Home", "Input Form", "Nutrition Calculator", "Meal Planner", "AI Chatbot", "Login/Register"]
    )

    # Routing
    user_data = st.session_state.user_data

    if page == "Home":
        show_home_page(user_data)
    elif page == "Input Form":
        show_input_form(user_data)
    elif page == "Nutrition Calculator":
        show_calculator_page(user_data)
    elif page == "Meal Planner":
        show_meal_planner_page(user_data, planner)


    elif page == "AI Chatbot":
        show_chatbot_page()
    elif page == "Login/Register":
        show_auth_page(user_data)

if __name__ == "__main__":
    main()
