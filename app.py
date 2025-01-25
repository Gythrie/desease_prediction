from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

model = pickle.load(open('disease.pk1', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')  

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
       
        user_data = {
            'Fever': request.form['Fever'],
            'Cough': request.form['Cough'],
            'Fatigue': request.form['Fatigue'],
            'Difficulty_Breathing': request.form['Difficulty_Breathing'],
            'Age': request.form['Age'],
            'Blood_Pressure': request.form['Blood_Pressure'],
            'Cholesterol_Level': request.form['Cholesterol_Level']
        }

        symptoms_map = {'Yes': 1, 'No': 0}
        fever = symptoms_map.get(user_data['Fever'], -1) 
        cough = symptoms_map.get(user_data['Cough'], -1)
        fatigue = symptoms_map.get(user_data['Fatigue'], -1)
        difficulty_breathing = symptoms_map.get(user_data['Difficulty_Breathing'], -1)

        health_map = {'Low': 0, 'Normal': 5, 'High': 10}
        blood_pressure = health_map.get(user_data['Blood_Pressure'], -1)  
        cholesterol_level = health_map.get(user_data['Cholesterol_Level'], -1)

       
        try:
            age = int(user_data['Age'])
        except ValueError:
            age = -1  

        if any(value == -1 for value in [fever, cough, fatigue, difficulty_breathing, blood_pressure, cholesterol_level, age]):
            return "Invalid input! Please ensure that the symptoms and health information are correctly entered."

        print(f"Input features: {fever}, {cough}, {fatigue}, {difficulty_breathing}, {age}, {blood_pressure}, {cholesterol_level}")

        input_features = np.array([fever, cough, fatigue, difficulty_breathing, age, blood_pressure, cholesterol_level])

        prediction = model.predict(input_features.reshape(1, -1))[0]

        print(f"Prediction result: {prediction}")

        # Return the prediction result to the webpage
        return render_template('index.html', prediction_text=f"The predicted disease is: {prediction}")

if __name__ == '__main__':
    app.run(debug=True)
