import streamlit as st
import pandas as pd

class MealPlanner:
    def __init__(self, food_data):
        self.food_df = pd.DataFrame(food_data)
        self.food_df = self.food_df[self.food_df['calories'] > 0].dropna(subset=['calories'])

    def generate_meal_plan(self, target_calories, diet_type='Balanced'):
        breakfast_cals = target_calories * 0.25
        lunch_cals = target_calories * 0.35
        dinner_cals = target_calories * 0.30
        snack_cals = target_calories * 0.10

        return {
            'Breakfast': self._select_foods(breakfast_cals, 'breakfast', diet_type),
            'Lunch': self._select_foods(lunch_cals, 'lunch', diet_type),
            'Dinner': self._select_foods(dinner_cals, 'dinner', diet_type),
            'Snack': self._select_foods(snack_cals, 'snack', diet_type)
        }

    def _select_foods(self, cal_limit, meal_type, diet_type):
        selected = []
        remaining = cal_limit

        if meal_type == 'breakfast':
            options = self.food_df[self.food_df['category'].isin(['protein', 'carbs', 'fruit'])].sample(n=min(3, len(self.food_df)))
        elif meal_type == 'lunch':
            options = self.food_df.sample(n=min(4, len(self.food_df)))
        elif meal_type == 'dinner':
            options = self.food_df[self.food_df['category'].isin(['protein', 'vegetable', 'carbs'])].sample(n=min(3, len(self.food_df)))
        else:
            options = self.food_df[self.food_df['calories'] < 200].sample(n=min(2, len(self.food_df[self.food_df['calories'] < 200])))

        for _, food in options.iterrows():
            if food['calories'] == 0:
                continue  # Skip to avoid division by zero

            if remaining <= 50:
                break

            portion = min(2.0, remaining / food['calories'])
            if portion >= 0.25:
                selected.append({
                    'name': food['name'],
                    'portion': round(portion, 2),
                    'calories': round(food['calories'] * portion),
                    'protein': round(food['protein'] * portion, 1),
                    'carbs': round(food['carbs'] * portion, 1),
                    'fat': round(food['fat'] * portion, 1)
                })
                remaining -= food['calories'] * portion


# ✅ FIXED: Now receives the `planner` object correctly
def show_meal_planner_page(user_data, planner):
    st.title("🥗 Smart Meal Planner")

    if 'target_calories' not in user_data or 'diet_type' not in user_data:
        st.warning("Please enter your details using the Calculator or Form page first.")
        return

    st.success(f"🎯 Your Target: {user_data['target_calories']:.0f} kcal/day — {user_data['diet_type']} Diet")

    if st.button("Generate Meal Plan"):
        meal_plan = planner.generate_meal_plan(user_data['target_calories'], user_data['diet_type'])
        st.session_state.meal_plan = meal_plan

    if 'meal_plan' in st.session_state:
        meal_plan = st.session_state.meal_plan

        total_cal, total_protein, total_carb, total_fat = 0, 0, 0, 0

        for meal, items in meal_plan.items():
            st.subheader(f"🍴 {meal}")
            if not items:
                st.write("No items selected.")
                continue
            df = pd.DataFrame(items)
            st.dataframe(df, use_container_width=True)

            meal_cal = sum(x['calories'] for x in items)
            meal_protein = sum(x['protein'] for x in items)
            meal_carb = sum(x['carbs'] for x in items)
            meal_fat = sum(x['fat'] for x in items)

            st.write(f"**Meal Total:** {meal_cal:.0f} kcal | {meal_protein:.1f}g Protein | {meal_carb:.1f}g Carbs | {meal_fat:.1f}g Fat")
            total_cal += meal_cal
            total_protein += meal_protein
            total_carb += meal_carb
            total_fat += meal_fat

            st.markdown("---")

        st.subheader("📊 Daily Totals")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Calories", f"{total_cal:.0f}", f"{total_cal - user_data['target_calories']:.0f}")
        col2.metric("Protein", f"{total_protein:.1f}g")
        col3.metric("Carbs", f"{total_carb:.1f}g")
        col4.metric("Fat", f"{total_fat:.1f}g")
