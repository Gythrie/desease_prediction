from flask import Flask, render_template, request
import numpy as np
import pickle


app = Flask(__name__)
disease_data = {
  "Influenza": {
    "details": "Influenza is a viral infection that attacks your respiratory system.",
    "selfCare": "Rest, stay hydrated, and take over-the-counter pain relievers to reduce fever and aches."
  },
  "Common Cold": {
    "details": "A common viral infection of the nose and throat.",
    "selfCare": "Drink plenty of fluids, rest, and use saline nasal sprays or lozenges for relief."
  },
  "Eczema": {
    "details": "Eczema causes the skin to become inflamed or irritated.",
    "selfCare": "Keep your skin moisturized, avoid harsh soaps, and use over-the-counter anti-itch creams."
  },
  "Asthma": {
    "details": "Asthma is a condition in which your airways narrow and swell.",
    "selfCare": "Avoid triggers, practice breathing exercises, and use prescribed inhalers."
  },
  "Hyperthyroidism": {
    "details": "A condition where the thyroid gland produces too much thyroid hormone.",
    "selfCare": "Avoid iodine-rich foods, reduce stress, and ensure regular follow-ups with your doctor."
  },
  "Allergic Rhinitis": {
    "details": "An allergic reaction causing sneezing, congestion, and a runny nose.",
    "selfCare": "Use antihistamines, avoid allergens, and keep indoor air clean with filters."
  },
  "Anxiety Disorders": {
    "details": "Characterized by excessive fear or worry.",
    "selfCare": "Practice relaxation techniques, exercise regularly, and maintain a balanced diet."
  },
  "Diabetes": {
    "details": "A metabolic disease that causes high blood sugar.",
    "selfCare": "Monitor your blood sugar levels, follow a healthy diet, and exercise regularly."
  },
  "Gastroenteritis": {
    "details": "Inflammation of the stomach and intestines causing diarrhea and vomiting.",
    "selfCare": "Stay hydrated, eat bland foods like rice and bananas, and avoid dairy and caffeine."
  },
  "Pancreatitis": {
    "details": "Inflammation of the pancreas causing abdominal pain.",
    "selfCare": "Avoid alcohol, eat a low-fat diet, and rest until symptoms improve."
  },
  "Rheumatoid Arthritis": {
    "details": "An autoimmune disease causing joint inflammation and pain.",
    "selfCare": "Use heat or cold packs, perform gentle exercises, and rest during flare-ups."
  },
  "Depression": {
    "details": "A mood disorder causing persistent sadness and loss of interest.",
    "selfCare": "Engage in activities you enjoy, stay connected with loved ones, and exercise regularly."
  },
  "Liver Cancer": {
    "details": "A type of cancer that begins in the liver.",
    "selfCare": "Eat a healthy diet, avoid alcohol, and seek medical guidance for treatment options."
  },
  "Stroke": {
    "details": "Occurs when blood flow to the brain is interrupted.",
    "selfCare": "Rehabilitation therapies and maintaining a healthy lifestyle are crucial post-stroke."
  },
  "Urinary Tract Infection": {
    "details": "An infection in any part of the urinary system.",
    "selfCare": "Drink plenty of water, avoid irritants like caffeine, and use a heating pad for discomfort."
  },
  "Dengue Fever": {
    "details": "A mosquito-borne viral infection causing fever and severe muscle pain.",
    "selfCare": "Rest, stay hydrated, and take acetaminophen to reduce fever and pain."
  },
  "Hepatitis": {
    "details": "Inflammation of the liver caused by viruses or toxins.",
    "selfCare": "Avoid alcohol, eat a healthy diet, and get plenty of rest."
  },
  "Kidney Cancer": {
    "details": "A type of cancer that starts in the kidneys.",
    "selfCare": "Maintain a healthy weight, stay hydrated, and follow your doctor's treatment plan."
  },
  "Migraine": {
    "details": "A severe headache often accompanied by nausea and sensitivity to light and sound.",
    "selfCare": "Rest in a dark, quiet room, use cold compresses, and stay hydrated."
  },
  "Muscular Dystrophy": {
    "details": "A group of diseases causing progressive muscle weakness.",
    "selfCare": "Engage in physical therapy, maintain a healthy diet, and use assistive devices as needed."
  },
  "Sinusitis": {
    "details": "Inflammation of the sinuses causing congestion and pain.",
    "selfCare": "Use saline nasal sprays, steam inhalation, and stay hydrated."
  },
  "Ulcerative Colitis": {
    "details": "A chronic inflammatory condition of the colon and rectum.",
    "selfCare": "Eat smaller meals, stay hydrated, and avoid trigger foods like spicy or fatty dishes."
  },
  "Bipolar Disorder": {
    "details": "A mental health condition characterized by extreme mood swings.",
    "selfCare": "Maintain a regular sleep schedule, avoid alcohol, and engage in stress-reducing activities."
  },
  "Bronchitis": {
    "details": "Inflammation of the bronchial tubes causing cough and mucus production.",
    "selfCare": "Drink warm fluids, use a humidifier, and rest your voice to soothe symptoms."
  },
  "Cerebral Palsy": {
    "details": "A group of disorders affecting movement and muscle tone or posture.",
    "selfCare": "Engage in physical therapy, maintain a healthy diet, and use mobility aids as needed."
  },
  "Colorectal Cancer": {
    "details": "A type of cancer that starts in the colon or rectum.",
    "selfCare": "Eat a high-fiber diet, stay active, and follow up with recommended screenings."
  },
  "Hypertensive Heart Disease": {
    "details": "Heart conditions caused by high blood pressure.",
    "selfCare": "Reduce salt intake, exercise regularly, and monitor blood pressure."
  },
  "Multiple Sclerosis": {
    "details": "A disease affecting the central nervous system causing nerve damage.",
    "selfCare": "Practice gentle exercises, stay hydrated, and manage stress levels."
  },
  "Myocardial Infarction": {
    "details": "Also known as a heart attack, it occurs when blood flow to the heart is blocked.",
    "selfCare": "Adopt a heart-healthy diet, avoid smoking, and engage in regular physical activity."
  },
  "Osteoporosis": {
    "details": "A condition causing bones to become weak and brittle.",
    "selfCare": "Ensure adequate calcium and vitamin D intake, and perform weight-bearing exercises."
  },
  "Atherosclerosis": {
    "details": "Hardening and narrowing of the arteries due to plaque buildup.",
    "selfCare": "Adopt a healthy diet, avoid smoking, and engage in regular exercise."
  },
  "Psoriasis": {
    "details": "A skin condition causing red, itchy, and scaly patches.",
    "selfCare": "Use moisturizers, avoid triggers like stress, and take soothing baths."
  },
  "Rubella": {
    "details": "A contagious viral infection causing a red rash.",
    "selfCare": "Rest, stay hydrated, and take over-the-counter medications to reduce fever."
  },
  "Cirrhosis": {
    "details": "Scarring of the liver caused by long-term liver damage.",
    "selfCare": "Avoid alcohol, eat a balanced diet, and follow your doctor’s recommendations."
  },
  "Conjunctivitis": {
    "details": "Also known as pink eye, it causes inflammation of the conjunctiva.",
    "selfCare": "Use warm compresses, avoid touching your eyes, and keep the area clean."
  },
  "Liver Disease": {
    "details": "A general term for conditions affecting the liver.",
    "selfCare": "Avoid alcohol, eat a balanced diet, and exercise regularly."
  },
  "Malaria": {
    "details": "A mosquito-borne disease causing fever and chills.",
    "selfCare": "Rest, stay hydrated, and take prescribed medications promptly."
  },
  "Chickenpox": {
    "details": "A contagious viral infection causing an itchy rash.",
    "selfCare": "Apply calamine lotion, avoid scratching, and take cool baths to soothe itching."
  },
  "Coronary Artery Disease": {
    "details": "A condition where the coronary arteries are narrowed or blocked.",
    "selfCare": "Adopt a heart-healthy diet, exercise regularly, and manage stress effectively."
  },
  "Fibromyalgia": {
    "details": "A condition causing widespread pain and fatigue.",
    "selfCare": "Practice relaxation techniques, engage in gentle exercises, and maintain a sleep schedule."
  },
  "Hemophilia": {
    "details": "A rare disorder causing the blood to not clot properly.",
    "selfCare": "Avoid injuries, follow a healthy diet, and consult your doctor for treatment options."
  },
  "Hypoglycemia": {
    "details": "Low blood sugar levels causing dizziness and shakiness.",
    "selfCare": "Consume fast-acting carbohydrates like fruit juice or glucose tablets immediately."
  },
  "Lymphoma": {
    "details": "A type of cancer that affects the lymphatic system.",
    "selfCare": "Maintain a healthy lifestyle, stay active, and follow your doctor’s treatment plan."
  },
    "Tuberculosis": {
      "details": "An infectious disease caused by bacteria, primarily affecting the lungs.",
      "selfCare": "Ensure good ventilation, maintain proper hygiene, and follow a healthy diet while adhering to prescribed medications."
    },
    "Hypothyroidism": {
      "details": "A condition in which the thyroid gland doesn't produce enough hormones.",
      "selfCare": "Consume a diet rich in iodine, exercise regularly, and take prescribed thyroid hormone replacement therapy."
    },
    "Autism Spectrum Disorder": {
      "details": "A developmental disorder that affects communication and behavior.",
      "selfCare": "Engage in structured routines, sensory-friendly activities, and consider therapy or support groups."
    },
    "Crohn's Disease": {
      "details": "A chronic inflammatory bowel disease affecting the gastrointestinal tract.",
      "selfCare": "Follow a low-fiber diet during flare-ups, manage stress, and stay hydrated."
    },
    "Hyperglycemia": {
      "details": "A condition characterized by high blood sugar levels.",
      "selfCare": "Monitor blood sugar regularly, eat a balanced diet, and exercise under medical supervision."
    },
    "Ovarian Cancer": {
      "details": "A type of cancer that begins in the ovaries.",
      "selfCare": "Maintain a healthy diet, stay active, and adhere to prescribed treatments."
    },
    "Spina Bifida": {
      "details": "A birth defect where the spine and spinal cord don't form properly.",
      "selfCare": "Ensure proper nutrition, engage in physical therapy, and maintain skin care to prevent sores."
    },
    "Turner Syndrome": {
      "details": "A genetic disorder affecting females, characterized by the partial or complete absence of one X chromosome.",
      "selfCare": "Follow hormone therapy, maintain a healthy diet, and seek regular medical checkups."
    },
    "Zika Virus": {
      "details": "A mosquito-borne virus causing fever, rash, and joint pain.",
      "selfCare": "Rest, stay hydrated, and use mosquito repellent to prevent further bites."
    },
    "Cataracts": {
      "details": "A condition where the lens of the eye becomes cloudy, impairing vision.",
      "selfCare": "Wear sunglasses to reduce glare and ensure regular eye checkups."
    },
    "Scoliosis": {
      "details": "A condition characterized by an abnormal lateral curvature of the spine.",
      "selfCare": "Practice good posture, engage in physical therapy, and avoid heavy lifting."
    },
    "Sickle Cell Anemia": {
      "details": "A genetic blood disorder causing misshapen red blood cells.",
      "selfCare": "Stay hydrated, avoid extreme temperatures, and manage pain with prescribed medications."
    },
    "Tetanus": {
      "details": "A bacterial infection causing muscle stiffness and spasms.",
      "selfCare": "Keep wounds clean and ensure vaccination is up to date."
    },
    "Anemia": {
      "details": "A condition characterized by a lack of healthy red blood cells.",
      "selfCare": "Consume iron-rich foods, take iron supplements if prescribed, and avoid excessive caffeine."
    },
    "Cholera": {
      "details": "An infectious disease causing severe diarrhea and dehydration.",
      "selfCare": "Drink oral rehydration solutions and consume clean, boiled water."
    },
    "Endometriosis": {
      "details": "A condition where tissue similar to the uterine lining grows outside the uterus.",
      "selfCare": "Apply heat to relieve pain, practice relaxation techniques, and maintain a healthy diet."
    },
    "Sepsis": {
      "details": "A life-threatening condition caused by the body's response to infection.",
      "selfCare": "Seek immediate medical attention and follow prescribed treatments."
    },
    "Sleep Apnea": {
      "details": "A sleep disorder where breathing repeatedly stops and starts.",
      "selfCare": "Maintain a healthy weight, avoid alcohol before bedtime, and use a CPAP machine if prescribed."
    },
    "Down Syndrome": {
      "details": "A genetic disorder caused by the presence of an extra chromosome 21.",
      "selfCare": "Encourage structured routines, engage in therapy, and foster a supportive environment."
    },
    "Ebola Virus": {
      "details": "A severe viral disease causing fever, bleeding, and organ failure.",
      "selfCare": "Follow isolation protocols and seek immediate medical attention."
    },
    "Lyme Disease": {
      "details": "A tick-borne disease causing fever, rash, and joint pain.",
      "selfCare": "Use tick repellents, remove ticks promptly, and complete prescribed antibiotics."
    },
    "Pancreatic Cancer": {
      "details": "A type of cancer that begins in the pancreas.",
      "selfCare": "Follow prescribed treatments, maintain a healthy diet, and seek emotional support."
    },
    "Pneumothorax": {
      "details": "A collapsed lung caused by air in the chest cavity.",
      "selfCare": "Avoid strenuous activities and follow medical advice during recovery."
    },
    "Appendicitis": {
      "details": "Inflammation of the appendix, often requiring surgical removal.",
      "selfCare": "Seek immediate medical attention for surgical intervention."
    },
    "Esophageal Cancer": {
      "details": "A cancer that forms in the esophagus.",
      "selfCare": "Maintain a healthy diet, avoid tobacco and alcohol, and adhere to prescribed treatments."
    },
    "HIV/AIDS": {
      "details": "A virus that attacks the immune system, leading to immune deficiency.",
      "selfCare": "Take antiretroviral therapy, eat a balanced diet, and maintain regular medical checkups."
    },
    "Marfan Syndrome": {
      "details": "A genetic disorder affecting connective tissue.",
      "selfCare": "Avoid strenuous physical activity and follow regular medical monitoring."
    },
    "Parkinson's Disease": {
      "details": "A progressive neurological disorder affecting movement.",
      "selfCare": "Engage in physical therapy, practice relaxation techniques, and follow prescribed medications."
    },
    "Polycystic Ovary Syndrome": {
      "details": "A hormonal disorder causing irregular periods and ovarian cysts.",
      "selfCare": "Maintain a healthy weight, follow a balanced diet, and exercise regularly."
    },
    "Typhoid Fever": {
      "details": "A bacterial infection causing fever, weakness, and abdominal pain.",
      "selfCare": "Consume clean, boiled water, eat easily digestible foods, and complete prescribed antibiotics."
    },
    "Measles": {
      "details": "A viral infection causing fever, rash, and respiratory symptoms.",
      "selfCare": "Rest, stay hydrated, and manage fever with over-the-counter medications."
    },
    "Osteomyelitis": {
      "details": "An infection in the bone.",
      "selfCare": "Complete prescribed antibiotics and follow wound care instructions."
    },
    "Polio": {
      "details": "A viral infection that can affect the nervous system and cause paralysis.",
      "selfCare": "Ensure vaccination and follow rehabilitation exercises if needed."
    },
    "Chronic Kidney Disease": {
      "details": "A condition characterized by the gradual loss of kidney function.",
      "selfCare": "Follow a kidney-friendly diet, stay hydrated, and adhere to prescribed medications."
    },
    "Hepatitis B": {
      "details": "A viral infection that affects the liver.",
      "selfCare": "Avoid alcohol, eat a healthy diet, and follow antiviral treatment if prescribed."
    },
    "Prader-Willi Syndrome": {
      "details": "A genetic disorder causing obesity, intellectual disability, and short stature.",
      "selfCare": "Follow a controlled diet, engage in physical activity, and ensure regular medical checkups."
    },
    "Thyroid Cancer": {
      "details": "A cancer that forms in the thyroid gland.",
      "selfCare": "Adhere to prescribed treatments, maintain a healthy diet, and follow regular checkups."
    },
    "Bladder Cancer": {
      "details": "A type of cancer that begins in the bladder.",
      "selfCare": "Avoid smoking, drink plenty of fluids, and follow prescribed treatments."
    },
    "Otitis Media": {
      "details": "An infection or inflammation of the middle ear.",
      "selfCare": "Apply warm compresses, stay hydrated, and complete prescribed antibiotics."
    },
    "Tourette Syndrome": {
      "details": "A neurological disorder causing repetitive movements or sounds.",
      "selfCare": "Reduce stress, engage in therapy, and maintain a structured routine."
    },
    "Alzheimer's Disease": {
      "details": "A progressive disease causing memory loss and cognitive decline.",
      "selfCare": "Engage in memory exercises, maintain a healthy diet, and stay socially active."
    },
    "Dementia": {
      "details": "A group of conditions causing memory loss and cognitive impairment.",
      "selfCare": "Establish routines, engage in mental stimulation, and seek caregiver support."
    },
    "Diverticulitis": {
      "details": "Inflammation or infection of small pouches in the digestive tract.",
      "selfCare": "Follow a low-fiber diet during flare-ups and gradually reintroduce fiber as advised."
    },
    "Lung Cancer": {
      "details": "A type of cancer that begins in the lungs.",
      "selfCare": "Avoid smoking, eat a balanced diet, and adhere to prescribed treatments."
    },
    "Mumps": {
      "details": "A viral infection causing swollen salivary glands.",
      "selfCare": "Rest, apply cold compresses, and stay hydrated."
    },
    "Prostate Cancer": {
      "details": "A cancer that occurs in the prostate gland.",
      "selfCare": "Maintain a healthy diet, stay physically active, and follow prescribed treatments."
    },
    "Schizophrenia": {
      "details": "A mental health disorder characterized by distorted thinking and behavior.",
      "selfCare": "Follow prescribed medications, engage in therapy, and maintain a supportive environment."
    },
    "Gout": {
      "details": "A type of arthritis caused by excess uric acid in the blood.",
      "selfCare": "Avoid purine-rich foods, stay hydrated, and use cold compresses for pain relief."
    },
    "Testicular Cancer": {
      "details": "A type of cancer that occurs in the testicles.",
      "selfCare": "Perform regular self-examinations and follow prescribed treatments."
    },
    "Tonsillitis": {
      "details": "Inflammation of the tonsils caused by viral or bacterial infection.",
      "selfCare": "Gargle with warm salt water, stay hydrated, and rest."
    },
    "Williams Syndrome": {
      "details": "A genetic disorder characterized by developmental delays and cardiovascular issues.",
      "selfCare": "Engage in therapy, monitor heart health, and ensure a supportive environment."
    }
  }
  

model = pickle.load(open('disease.pk1', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/about')
def about_us():
    return render_template('about.html') 
@app.route('/doctor')
def doctor_info():
    return render_template('doctor.html')

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
        result = disease_data.get(prediction, {
        "details": "Details not available for this disease.",
        "selfCare": "No self-care tips available for this disease."
    })

       # print(f"Prediction result: {prediction}")

        # Return the prediction result to the webpage
    return render_template('result.html', prediction_text=f"The predicted disease is: {prediction}",
                details=result["details"],
                self_care=result["selfCare"])

if __name__ == '__main__':
    app.run(debug=True)
