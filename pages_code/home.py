import streamlit as st

def show_home_page(user_data):
    st.set_page_config(page_title="Smart AI Nutrition Assistant", page_icon="🥗")
    st.title("🧠 Smart AI Nutrition Assistant")
    st.markdown("### Your Personalized Health & Nutrition Companion")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        #### 🔢 Calorie Calculator
        Calculate your daily calorie needs based on your personal information and fitness goals.
        """)
        st.image("https://img.icons8.com/fluency/96/000000/nutritional-info.png", width=80)

    with col2:
        st.markdown("""
        #### 🥗 Meal Planner
        Get personalized meal plans that match your calorie and macronutrient requirements.
        """)
        st.image("https://img.icons8.com/color/96/meal.png", width=80)

    with col3:
        st.markdown("""
        #### 💬 AI Chatbot
        Ask nutrition questions and get instant, expert-backed answers.
        """)
        st.image("https://img.icons8.com/fluency/96/chatbot.png", width=80)

    st.markdown("---")
    st.markdown("""
    ## 🎯 Features:
    - **Personalized Nutrition**: Tailored recommendations based on your goals
    - **Smart Meal Planning**: AI-generated meal plans with macro tracking
    - **Expert Chatbot**: Get answers to your nutrition questions instantly
    - **Multiple Diet Types**: Support for various dietary preferences
    - **Progress Tracking**: Save and monitor your nutrition journey
    """)

    st.info("👈 Use the sidebar to explore each feature module.")
