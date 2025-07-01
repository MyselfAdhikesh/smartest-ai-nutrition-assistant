import streamlit as st
import json
import hashlib
import os
from datetime import datetime

# --- Utility Functions ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_user_data(username, password, user_info):
    try:
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                users = json.load(f)
        else:
            users = {}

        users[username] = {
            'password': hash_password(password),
            'info': user_info,
            'created_at': datetime.now().isoformat()
        }

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=2)
        return True
    except:
        return False

def verify_user(username, password):
    try:
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                users = json.load(f)

            if username in users and users[username]['password'] == hash_password(password):
                return users[username]['info']
        return None
    except:
        return None

# --- Auth Page ---
def show_auth_page(user_data):
    st.title("🔐 Login / Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login to Your Account")
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", type="primary"):
            user_info = verify_user(login_username, login_password)
            if user_info:
                st.session_state.logged_in = True
                st.session_state.current_user = login_username
                st.session_state.user_data = user_info
                st.success(f"Welcome back, {login_username}!")
                st.rerun()
            else:
                st.error("Invalid username or password!")

    with tab2:
        st.subheader("Create New Account")
        reg_username = st.text_input("Choose Username", key="reg_user")
        reg_password = st.text_input("Choose Password", type="password", key="reg_pass")
        reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_pass_confirm")

        # Basic user info for registration
        reg_age = st.number_input("Age", min_value=10, max_value=100, value=25, key="reg_age")
        reg_gender = st.selectbox("Gender", ["Male", "Female"], key="reg_gender")

        if st.button("Register", type="primary"):
            if reg_password != reg_password_confirm:
                st.error("Passwords don't match!")
            elif len(reg_password) < 6:
                st.error("Password must be at least 6 characters long!")
            elif len(reg_username) < 3:
                st.error("Username must be at least 3 characters long!")
            else:
                user_info = {
                    'age': reg_age,
                    'gender': reg_gender,
                    'weight': 70.0,
                    'height': 170.0,
                    'activity_level': 'Moderately Active',
                    'goal': 'Maintain Weight',
                    'diet_type': 'Balanced'
                }

                if save_user_data(reg_username, reg_password, user_info):
                    st.success("Account created successfully! Please login.")
                else:
                    st.error("Failed to create account. Username might already exist.")

    if st.session_state.get("logged_in"):
        st.success(f"✅ Logged in as: {st.session_state.current_user}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.user_data = {}
            st.rerun()
