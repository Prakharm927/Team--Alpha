from flask import Flask, render_template, request

app = Flask(__name__)

# ... (calculate_calorie_intake and generate_meal_plan functions from the second code snippet)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/meal_plan', methods=['POST'])
def meal_plan():
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    age = int(request.form['age'])
    gender = request.form['gender']
    activity_level = request.form['activity_level']
    goal = request.form['goal']

    calorie_intake = calculate_calorie_intake(weight, height, age, gender, activity_level, goal)
    meal_plan_text = generate_meal_plan(calorie_intake)

    return render_template('meal_plan.html', meal_plan_text=meal_plan_text)

if __name__ == "__main__":
    app.run(debug=True)
