import pandas as pd

class MealPlanner:
    def __init__(self, food_data):
        self.food_df = pd.DataFrame(food_data)

    def generate_meal_plan(self, target_calories, diet_type='Balanced'):
        breakfast = self._select_foods(target_calories * 0.25, ['protein', 'carbs', 'fruit'])
        lunch = self._select_foods(target_calories * 0.35)
        dinner = self._select_foods(target_calories * 0.30, ['protein', 'vegetable', 'carbs'])
        snack = self._select_foods(target_calories * 0.10)  # <-- removed max_calories
        return {
            'Breakfast': breakfast,
            'Lunch': lunch,
            'Dinner': dinner,
            'Snack': snack
        }

    def _select_foods(self, cal_limit, categories=None):
        selected = []
        remaining = cal_limit

        df = self.food_df.copy()

        # Filter by categories if provided
        if categories:
            df = df[df['category'].isin(categories)]

        # Drop rows where calories are zero or NaN
        df = df[pd.to_numeric(df['calories'], errors='coerce') > 0]

        if df.empty:
            return selected

        options = df.sample(n=min(4, len(df)))

        for _, food in options.iterrows():
            calories = food.get('calories', 0)
            if pd.isna(calories) or calories <= 0:
                continue

            if remaining <= 50:
                break

            try:
                portion = min(2.0, remaining / calories)
            except ZeroDivisionError:
                continue

            if portion >= 0.25:
                selected.append({
                    'name': food['name'],
                    'portion': round(portion, 2),
                    'calories': round(calories * portion),
                    'protein': round(food['protein'] * portion, 1),
                    'carbs': round(food['carbs'] * portion, 1),
                    'fat': round(food['fat'] * portion, 1)
                })
                remaining -= calories * portion

        return selected



