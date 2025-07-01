import streamlit as st
import pandas as pd

class NutritionChatbot:
    def __init__(self, faq_data):
        self.faq_df = pd.DataFrame(faq_data)

    def get_response(self, user_question):
        user_question = user_question.lower().strip()

        for _, row in self.faq_df.iterrows():
            if self._calculate_similarity(user_question, row['question'].lower()) > 0.3:
                return row['answer']

        if any(word in user_question for word in ['protein']):
            return "Good protein sources include chicken, fish, eggs, Greek yogurt, legumes, and quinoa."
        elif any(word in user_question for word in ['calories']):
            return "Men typically need 2200–2800 kcal/day and women need 1800–2200 kcal/day, depending on activity level."
        elif any(word in user_question for word in ['weight loss']):
            return "For healthy weight loss, reduce 500–750 kcal/day and include exercise, whole foods, and hydration."
        elif any(word in user_question for word in ['carbs']):
            return "Choose complex carbs like oats, brown rice, and fruits for better energy and fiber."
        elif any(word in user_question for word in ['fat']):
            return "Healthy fats include avocados, olive oil, nuts, and fatty fish like salmon."
        else:
            return "I'm here to help! Ask me about protein, calories, weight loss, healthy foods, or meal tips."

    def _calculate_similarity(self, text1, text2):
        words1 = set(text1.split())
        words2 = set(text2.split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union) if union else 0

def show_chatbot_page():
    st.title("💬 AI Nutrition Chatbot")
    st.markdown("Ask anything about health, nutrition, or food habits.")

    FAQ_DATA = pd.read_csv("data/faq_data.csv")

    bot = NutritionChatbot(FAQ_DATA)

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    for q, a in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(q)
        with st.chat_message("assistant"):
            st.write(a)

    user_question = st.chat_input("Ask a nutrition question...")

    if user_question:
        response = bot.get_response(user_question)
        st.session_state.chat_history.append((user_question, response))
        st.rerun()

    st.subheader("💡 Try asking:")
    for example in [
        "How many calories do I need?",
        "What is a good post-workout meal?",
        "How to gain muscle with vegetarian diet?"
    ]:
        if st.button(example, key=f"suggest_{example}"):
            response = bot.get_response(example)
            st.session_state.chat_history.append((example, response))
            st.rerun()
