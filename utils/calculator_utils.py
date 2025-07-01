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
        else:
            return tdee
