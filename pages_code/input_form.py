import streamlit as st

def calculate_target_calories(age, weight, height, gender, activity_level):
    """Calculate target calories using a simplified BMR + activity multiplier"""
    bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender == 'Male' else -161)
    multiplier = {
        "Sedentary": 1.2,
        "Lightly active": 1.375,
        "Moderately active": 1.55,
        "Very active": 1.725,
        "Extra active": 1.9
    }
    return bmr * multiplier.get(activity_level, 1.2)

def show_input_form(user_data):
    st.header("📝 Enter Your Profile Details")

    user_data['age'] = st.number_input("Age", min_value=10, max_value=100, step=1)
    user_data['weight'] = st.number_input("Weight (kg)", min_value=30, max_value=200, step=1)
    user_data['height'] = st.number_input("Height (cm)", min_value=100, max_value=250, step=1)
    user_data['gender'] = st.selectbox("Gender", ["Male", "Female"], key="form_gender")
    user_data['activity_level'] = st.selectbox("Activity Level", [
        "Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"
    ], key="form_activity")
    user_data['diet_type'] = st.selectbox("Diet Type", ["Standard", "Keto", "Vegetarian", "High Protein"], key="form_diet")

    # ✅ Calculate target calories once all inputs are provided
    if all(k in user_data for k in ['age', 'weight', 'height', 'gender', 'activity_level']):
        user_data['target_calories'] = calculate_target_calories(
            user_data['age'], user_data['weight'], user_data['height'],
            user_data['gender'], user_data['activity_level']
        )
        st.success(f"🎯 Estimated Target Calories: {user_data['target_calories']:.0f} kcal/day")

    st.write("📦 Debug Info:", user_data)
