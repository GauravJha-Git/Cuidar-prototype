# app.py
from flask import Flask, render_template, request, jsonify
import time
import re

app = Flask(__name__)

# Medical knowledge base
medical_database = {
    "headache": {
        "keywords": ["headache", "head pain", "migraine", "head hurts", "head ache"],
        "instant_remedy": "Drink water, rest in a dark quiet room, and take an over-the-counter pain reliever like acetaminophen or ibuprofen if needed.",
        "essential_remedies": [
            "Stay hydrated with 8-10 glasses of water daily",
            "Maintain regular sleep schedule (7-9 hours)",
            "Practice stress reduction techniques like deep breathing",
            "Limit screen time and take regular breaks",
            "Consider tracking triggers (certain foods, stress, lack of sleep)"
        ],
        "disclaimer": "Seek medical attention for severe, sudden, or persistent headaches."
    },
    "common cold": {
        "keywords": ["cold", "common cold", "runny nose", "stuffy nose", "sneezing", "cough", "sore throat"],
        "instant_remedy": "Rest, stay hydrated, and take over-the-counter cold medications to manage symptoms. Gargle with warm salt water for sore throat.",
        "essential_remedies": [
            "Drink warm liquids like herbal tea with honey",
            "Use a humidifier to add moisture to the air",
            "Take vitamin C supplements",
            "Get extra rest to support your immune system",
            "Use saline nasal spray to relieve congestion"
        ],
        "disclaimer": "Seek medical attention if symptoms worsen after 10 days or you develop high fever."
    },
    "upset stomach": {
        "keywords": ["upset stomach", "stomach ache", "nausea", "stomach pain", "indigestion", "diarrhea", "vomiting"],
        "instant_remedy": "Sip clear fluids slowly, avoid solid foods for a few hours, and try small amounts of bland foods like toast or rice when feeling better.",
        "essential_remedies": [
            "Drink ginger or peppermint tea",
            "Try the BRAT diet (bananas, rice, applesauce, toast)",
            "Avoid dairy, caffeine, and spicy foods temporarily",
            "Take probiotics to restore gut balance",
            "Apply a warm compress to abdomen for comfort"
        ],
        "disclaimer": "Seek medical attention for severe pain, vomiting blood, or symptoms lasting more than 2 days."
    },
    "fever": {
        "keywords": ["fever", "high temperature", "feeling hot", "chills", "sweating", "body temperature"],
        "instant_remedy": "Take acetaminophen or ibuprofen as directed, drink plenty of fluids, and rest. Use a cool compress on the forehead.",
        "essential_remedies": [
            "Stay hydrated with water, clear broth, or sports drinks",
            "Dress in lightweight clothing",
            "Keep room temperature comfortable (not too hot or cold)",
            "Take a lukewarm bath if temperature is high",
            "Monitor temperature regularly"
        ],
        "disclaimer": "Seek immediate medical attention for very high fevers (above 103°F/39.4°C) or if accompanied by severe headache, stiff neck, confusion, or difficulty breathing."
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_remedy', methods=['POST'])
def get_remedy():
    user_prompt = request.json.get('prompt', '').lower()
    
    # Simulate AI thinking time
    time.sleep(1)
    
    # Check for matching conditions in the prompt
    found_conditions = []
    
    for condition, data in medical_database.items():
        for keyword in data["keywords"]:
            if keyword in user_prompt:
                found_conditions.append(condition)
                break
    
    if found_conditions:
        # Return information for the first recognized condition
        condition = found_conditions[0]
        result = {
            "instant_remedy": medical_database[condition]["instant_remedy"],
            "essential_remedies": medical_database[condition]["essential_remedies"],
            "disclaimer": medical_database[condition]["disclaimer"]
        }
    else:
        # If no condition is recognized
        result = {
            "instant_remedy": "AI in under Process, you are using a prototype please contact doctor or if tester then developer.",
            "essential_remedies": [
                "This AI prototype has limited medical knowledge",
                "Always consult healthcare professionals for medical advice",
                "We're constantly improving our medical database"
            ],
            "disclaimer": "This is a prototype version with limited condition recognition capabilities."
        }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)