def calculate_calorie_intake(weight, height, age, gender, activity_level, goal):
    # You can use various formulas to calculate daily calorie needs based on user input
    # This is a simplified example
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_multipliers = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9
    }

    calorie_intake = bmr * activity_multipliers.get(activity_level.lower(), 1.2)

    if goal.lower() == "lose":
        calorie_intake -= 500  # Create a caloric deficit for weight loss
    elif goal.lower() == "gain":
        calorie_intake += 500  # Create a caloric surplus for weight gain

    return calorie_intake

def meal_plan(calorie_intake):
    # This is a basic meal plan, you may want to customize it based on nutritional needs
    breakfast = "Scrambled eggs with spinach and whole grain toast"
    lunch = "Grilled chicken salad with quinoa and mixed vegetables"
    dinner = "Baked salmon with sweet potato and steamed broccoli"

    print("Meal Plan:")
    print("Breakfast:", breakfast)
    print("Lunch:", lunch)
    print("Dinner:", dinner)
    print("\nTotal Daily Caloric Intake:", calorie_intake)

def main():
    print("Welcome to the Meal Planning System!")
    weight = float(input("Enter your weight (kg): "))
    height = float(input("Enter your height (cm): "))
    age = int(input("Enter your age: "))
    gender = input("Enter your gender (Male/Female): ")
    activity_level = input("Enter your activity level (sedentary/lightly active/moderately active/very active/extra active): ")
    goal = input("What is your fitness goal? (Maintain/Lose/Gain): ")

    calorie_intake = calculate_calorie_intake(weight, height, age, gender, activity_level, goal)
    meal_plan(calorie_intake)

if __name__ == "__main__":
    main()
