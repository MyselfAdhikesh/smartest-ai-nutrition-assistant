import streamlit as st

class NutritionCalculator:
    @staticmethod
    def calculate_bmr(weight, height, age, gender):
        if gender.lower() == 'male':
            return 10 * weight + 6.25 * height - 5 * age + 5
        else:
            return 10 * weight + 6.25 * height - 5 * age - 161

    @staticmethod
    def calculate_tdee(bmr, activity_level):
        activity_multipliers = {
            'Sedentary': 1.2,
            'Lightly Active': 1.375,
            'Moderately Active': 1.55,
            'Very Active': 1.725,
            'Extremely Active': 1.9
        }
        return bmr * activity_multipliers.get(activity_level, 1.2)

    @staticmethod
    def adjust_calories_for_goal(tdee, goal):
        if goal == 'Lose Weight':
            return tdee - 500
        elif goal == 'Gain Weight':
            return tdee + 500
        return tdee

def show_calculator_page(user_data):
    st.title("🔢 Nutrition Calculator")
    calc = NutritionCalculator()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Personal Information")
        age = st.number_input("Age (years)", min_value=10, max_value=100, value=25)
        gender = st.selectbox("Gender", ["Male", "Female"], key="calc_gender")
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)

    with col2:
        st.subheader("Lifestyle & Goals")
        activity_level = st.selectbox("Activity Level", [
            "Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"
        ], key="calc_activity")
        goal = st.selectbox("Primary Goal", ["Maintain Weight", "Lose Weight", "Gain Weight"], key="calc_goal")
        diet_type = st.selectbox("Diet Preference", ["Balanced", "High Protein", "Low Carb", "Vegetarian"], key="calc_diet")

    if st.button("Calculate My Nutrition Needs", type="primary"):
        bmr = calc.calculate_bmr(weight, height, age, gender)
        tdee = calc.calculate_tdee(bmr, activity_level)
        target_calories = calc.adjust_calories_for_goal(tdee, goal)

        user_data.update({
            'age': age, 'gender': gender, 'weight': weight, 'height': height,
            'activity_level': activity_level, 'goal': goal, 'diet_type': diet_type,
            'bmr': bmr, 'tdee': tdee, 'target_calories': target_calories
        })

        st.success("✅ Calculations Complete!")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("BMR", f"{bmr:.0f} cal/day")
        with col2:
            st.metric("TDEE", f"{tdee:.0f} cal/day")
        with col3:
            st.metric("Target", f"{target_calories:.0f} cal/day")

        # Macronutrient breakdown
        st.subheader("📊 Recommended Macronutrients")
        protein_grams = weight * (1.2 if goal == "Gain Weight" else 1.0)
        protein_calories = protein_grams * 4
        fat_calories = target_calories * 0.25
        carb_calories = target_calories - protein_calories - fat_calories

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Protein", f"{protein_grams:.0f}g ({protein_calories:.0f} cal)")
        with col2:
            st.metric("Carbs", f"{carb_calories / 4:.0f}g ({carb_calories:.0f} cal)")
        with col3:
            st.metric("Fats", f"{fat_calories / 9:.0f}g ({fat_calories:.0f} cal)")
