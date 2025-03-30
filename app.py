from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import time
import re
import numpy as np
from datetime import datetime, timedelta
#text Analyzer
from text_analyzer import MedicalTextAnalyzer
import nltk
nltk.download('stopwords')

app = Flask(__name__)
analyzer = MedicalTextAnalyzer()
CORS(app)

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
    },
    "sore throat": {
        "keywords": ["sore throat", "throat pain", "scratchy throat", "throat irritation"],
        "instant_remedy": "Gargle with warm salt water and drink warm tea with honey. Use lozenges or throat sprays for relief.",
        "essential_remedies": [
            "Drink warm fluids like herbal tea",
            "Use a humidifier to keep air moist",
            "Avoid smoking or exposure to smoke",
            "Rest your voice and avoid excessive talking",
            "Take honey and ginger for natural relief"
        ],
        "disclaimer": "Seek medical attention if the sore throat lasts more than a week or is accompanied by high fever and swollen lymph nodes."
    },
    "allergies": {
        "keywords": ["allergy", "sneezing", "itchy eyes", "runny nose", "seasonal allergies"],
        "instant_remedy": "Take an antihistamine and avoid allergen exposure. Use a saline nasal rinse for relief.",
        "essential_remedies": [
            "Keep windows closed during allergy season",
            "Use an air purifier to reduce allergens",
            "Take vitamin C and quercetin supplements",
            "Try a honey-based remedy to build immunity",
            "Wash hands and face after coming from outdoors"
        ],
        "disclaimer": "Seek medical help if experiencing difficulty breathing or severe allergic reactions (anaphylaxis)."
    },
    "acid reflux": {
        "keywords": ["acid reflux", "heartburn", "GERD", "acidic burps", "burning chest pain"],
        "instant_remedy": "Drink a glass of cold milk or take an antacid. Avoid lying down immediately after eating.",
        "essential_remedies": [
            "Eat smaller, frequent meals",
            "Avoid spicy, fatty, and acidic foods",
            "Sleep with head elevated",
            "Limit caffeine and alcohol intake",
            "Chew gum to increase saliva production"
        ],
        "disclaimer": "Consult a doctor if symptoms persist for weeks or worsen over time."
    },
    "constipation": {
        "keywords": ["constipation", "hard stool", "difficulty pooping", "bloating", "not passing stool"],
        "instant_remedy": "Drink warm water with lemon and eat high-fiber foods like prunes or flaxseeds.",
        "essential_remedies": [
            "Increase fiber intake with fruits and vegetables",
            "Drink 8-10 glasses of water daily",
            "Exercise regularly to stimulate bowel movement",
            "Avoid processed and low-fiber foods",
            "Try probiotics for gut health"
        ],
        "disclaimer": "Seek medical advice if constipation persists for more than two weeks or is accompanied by severe pain."
    },
    "diarrhea": {
        "keywords": ["diarrhea", "loose stool", "frequent bowel movement", "stomach cramps"],
        "instant_remedy": "Drink an oral rehydration solution (ORS) or coconut water to replace lost fluids.",
        "essential_remedies": [
            "Follow the BRAT diet (bananas, rice, applesauce, toast)",
            "Avoid dairy, caffeine, and high-fat foods",
            "Drink ginger tea for digestive relief",
            "Take probiotics to restore gut balance",
            "Rest and avoid overexertion"
        ],
        "disclaimer": "Seek medical attention if diarrhea persists for more than 2 days or includes blood."
    },
    "back pain": {
        "keywords": ["back pain", "lower back pain", "spinal pain", "stiff back","pain in back"],
        "instant_remedy": "Apply a hot or cold compress and rest in a comfortable position.",
        "essential_remedies": [
            "Maintain good posture while sitting and standing",
            "Stretch and exercise regularly",
            "Use ergonomic chairs and mattresses",
            "Avoid heavy lifting or sudden movements",
            "Massage or apply topical pain relief creams"
        ],
        "disclaimer": "Seek medical help if back pain is severe, persistent, or accompanied by numbness."
    },
    "muscle cramps": {
        "keywords": ["muscle cramp", "leg cramps", "muscle pain", "spasm"],
        "instant_remedy": "Gently stretch and massage the muscle. Drink water with electrolytes.",
        "essential_remedies": [
            "Stay hydrated throughout the day",
            "Eat potassium-rich foods like bananas",
            "Warm up properly before exercising",
            "Apply heat or cold packs as needed",
            "Take magnesium supplements if deficient"
        ],
        "disclaimer": "Consult a doctor if cramps occur frequently or are extremely painful."
    },
    "dizziness": {
        "keywords": ["dizziness", "lightheaded", "vertigo", "feeling faint"],
        "instant_remedy": "Sit or lie down immediately and drink water. Breathe deeply to stabilize yourself.",
        "essential_remedies": [
            "Avoid sudden head movements",
            "Stay hydrated and eat balanced meals",
            "Limit caffeine and alcohol intake",
            "Practice deep breathing exercises",
            "Get adequate rest and avoid overexertion"
        ],
        "disclaimer": "Seek medical help if dizziness is frequent, severe, or accompanied by vision issues."
    },
    "toothache": {
        "keywords": ["toothache", "tooth pain", "cavity pain", "sensitive teeth"],
        "instant_remedy": "Rinse with warm salt water and apply a cold compress to reduce swelling.",
        "essential_remedies": [
            "Brush and floss regularly",
            "Avoid extremely hot or cold foods",
            "Use clove oil for natural pain relief",
            "Stay away from sugary and acidic foods",
            "Visit a dentist for proper diagnosis"
        ],
        "disclaimer": "Seek dental care if pain persists or there is swelling in the jaw."
    },
    "earache": {
        "keywords": ["earache", "ear pain", "blocked ear", "ear infection"],
        "instant_remedy": "Apply a warm compress to the ear and take a mild pain reliever if necessary.",
        "essential_remedies": [
            "Avoid inserting objects into the ear",
            "Use over-the-counter ear drops",
            "Stay hydrated to keep mucus thin",
            "Sleep with the affected ear elevated",
            "Avoid exposure to cold drafts"
        ]
    },
    "insomnia": {
        "keywords": ["insomnia", "can't sleep", "trouble sleeping", "sleeplessness"],
        "instant_remedy": "Drink warm milk or chamomile tea and try deep breathing exercises.",
        "essential_remedies": [
            "Maintain a regular sleep schedule",
            "Avoid screens at least an hour before bed",
            "Keep your bedroom cool and dark",
            "Limit caffeine intake in the evening",
            "Practice relaxation techniques like meditation"
        ],
        "disclaimer": "Seek medical advice if insomnia persists for weeks or affects daily life."
    },
    "sinusitis": {
        "keywords": ["sinusitis", "sinus infection", "blocked nose", "sinus headache"],
        "instant_remedy": "Inhale steam with essential oils like eucalyptus and use a saline nasal spray.",
        "essential_remedies": [
            "Drink plenty of warm fluids",
            "Use a humidifier to keep nasal passages moist",
            "Apply warm compresses to the sinuses",
            "Avoid allergens that trigger sinus issues",
            "Take vitamin C to boost immunity"
        ],
        "disclaimer": "Consult a doctor if symptoms persist for more than 10 days or worsen."
    },
    "dry skin": {
        "keywords": ["dry skin", "itchy skin", "flaky skin", "rough skin"],
        "instant_remedy": "Apply a moisturizer with aloe vera or shea butter immediately after a shower.",
        "essential_remedies": [
            "Drink plenty of water to stay hydrated",
            "Use fragrance-free moisturizers",
            "Avoid long hot showers",
            "Use a humidifier in dry climates",
            "Consume omega-3 fatty acids for skin health"
        ],
        "disclaimer": "Seek medical help if dry skin becomes cracked, painful, or infected."
    },
    "eye strain": {
        "keywords": ["eye strain", "tired eyes", "burning eyes", "blurred vision"],
        "instant_remedy": "Rest your eyes using the 20-20-20 rule (every 20 minutes, look 20 feet away for 20 seconds).",
        "essential_remedies": [
            "Reduce screen brightness and use blue light filters",
            "Blink frequently to keep eyes moist",
            "Maintain proper lighting while reading",
            "Use artificial tears if eyes feel dry",
            "Get regular eye check-ups"
        ],
        "disclaimer": "Consult an eye specialist if strain persists or vision worsens."
    },
    "bad breath": {
        "keywords": ["bad breath", "halitosis", "mouth odor", "smelly breath"],
        "instant_remedy": "Chew sugar-free gum or rinse with a mouthwash containing antibacterial properties.",
        "essential_remedies": [
            "Brush and floss twice daily",
            "Stay hydrated to prevent dry mouth",
            "Avoid foods that cause odor (garlic, onions)",
            "Use tongue scrapers to remove bacteria",
            "Eat probiotic-rich foods for gut health"
        ],
        "disclaimer": "Consult a dentist if bad breath persists despite proper oral hygiene."
    },
    "hives": {
        "keywords": ["hives", "skin rash", "itchy bumps", "allergic rash"],
        "instant_remedy": "Take an antihistamine and apply a cold compress to relieve itching.",
        "essential_remedies": [
            "Identify and avoid allergy triggers",
            "Wear loose-fitting clothing",
            "Take oatmeal baths for skin relief",
            "Use calamine lotion to soothe irritation",
            "Stay cool and avoid overheating"
        ],
        "disclaimer": "Seek immediate medical help if hives are accompanied by breathing difficulty."
    },
    "food poisoning": {
        "keywords": ["food poisoning", "vomiting", "diarrhea", "stomach cramps"],
        "instant_remedy": "Drink oral rehydration solution (ORS) and avoid solid foods for a few hours.",
        "essential_remedies": [
            "Stick to bland foods like toast and bananas",
            "Avoid dairy and caffeine until fully recovered",
            "Stay hydrated with electrolyte-rich drinks",
            "Get plenty of rest",
            "Wash hands and food items properly to prevent recurrence"
        ],
        "disclaimer": "Seek medical help if symptoms include high fever, blood in stool, or prolonged vomiting."
    },
    "burns": {
        "keywords": ["burns", "skin burn", "heat burn", "scalding"],
        "instant_remedy": "Run cool water over the burn for at least 10 minutes and apply aloe vera gel.",
        "essential_remedies": [
            "Keep burn area clean and dry",
            "Avoid popping blisters",
            "Apply antibiotic ointment to prevent infection",
            "Cover with a sterile bandage",
            "Take pain relievers if needed"
        ],
        "disclaimer": "Seek emergency care for severe burns, electrical burns, or burns covering large areas."
    },
    "sunburn": {
        "keywords": ["sunburn", "red skin", "skin burn", "sun damage"],
        "instant_remedy": "Apply aloe vera gel and drink plenty of water.",
        "essential_remedies": [
            "Stay out of direct sunlight until healed",
            "Use cool compresses to relieve pain",
            "Wear loose, breathable clothing",
            "Moisturize skin frequently",
            "Apply SPF 30+ sunscreen to prevent future burns"
        ],
        "disclaimer": "Seek medical attention for severe blistering or dehydration symptoms."
    },
    "motion sickness": {
        "keywords": ["motion sickness", "car sickness", "nausea in vehicles"],
        "instant_remedy": "Sit in the front seat, keep your gaze fixed on the horizon, and chew ginger gum.",
        "essential_remedies": [
            "Avoid heavy meals before travel",
            "Use motion sickness wristbands",
            "Take deep breaths to relax",
            "Try acupressure techniques",
            "Stay hydrated and avoid alcohol"
        ],
        "disclaimer": "Consult a doctor if motion sickness is frequent or severe."
    },
    "cold sores": {
        "keywords": ["cold sores", "lip blisters", "herpes simplex", "mouth blisters"],
        "instant_remedy": "Apply an antiviral cream and avoid touching the affected area.",
        "essential_remedies": [
            "Keep lips moisturized",
            "Avoid direct sunlight on lips",
            "Boost immunity with vitamin C",
            "Avoid sharing utensils and lip balms",
            "Apply ice to reduce swelling"
        ],
        "disclaimer": "Seek medical help if cold sores persist or worsen."
    },
    "hangover": {
        "keywords": ["hangover", "alcohol sickness", "morning after drinking", "headache from alcohol"],
        "instant_remedy": "Drink coconut water or electrolyte drinks and eat a light breakfast.",
        "essential_remedies": [
            "Stay hydrated with water and sports drinks",
            "Eat before drinking to slow alcohol absorption",
            "Avoid excessive alcohol consumption",
            "Take vitamin B and zinc supplements",
            "Get enough sleep to aid recovery"
        ],
        "disclaimer": "Seek medical help if symptoms include confusion, seizures, or severe dehydration."
    },
    "puffy eyes": {
        "keywords": ["puffy eyes", "swollen eyes", "under-eye bags", "eye puffiness"],
        "instant_remedy": "Apply cold tea bags or cucumber slices over closed eyes.",
        "essential_remedies": [
            "Get adequate sleep (7-9 hours)",
            "Reduce salt intake to prevent water retention",
            "Use an under-eye roller with caffeine",
            "Stay hydrated to flush toxins",
            "Avoid rubbing your eyes frequently"
        ]
    },
    "chapped lips": {
        "keywords": ["chapped lips", "dry lips", "cracked lips", "lip peeling"],
        "instant_remedy": "Apply a hydrating lip balm with beeswax or coconut oil.",
        "essential_remedies": [
            "Drink plenty of water to stay hydrated",
            "Avoid licking your lips frequently",
            "Use a humidifier in dry weather",
            "Apply aloe vera or honey for healing",
            "Use SPF lip balm to prevent sun damage"
        ],
        "disclaimer": "Seek medical attention if lips are severely cracked, bleeding, or infected."
    },
    "bronchitis": {
        "keywords": ["bronchitis", "chest congestion", "persistent cough", "mucus buildup"],
        "instant_remedy": "Drink warm tea with honey and inhale steam for relief.",
        "essential_remedies": [
            "Stay hydrated to thin mucus",
            "Avoid smoking and polluted air",
            "Use a humidifier for easier breathing",
            "Take rest to allow the body to heal",
            "Try ginger or turmeric tea for anti-inflammatory effects"
        ],
        "disclaimer": "Seek medical attention if symptoms persist for more than 3 weeks or worsen."
    },
    "anemia": {
        "keywords": ["anemia", "low iron", "fatigue", "weakness", "pale skin"],
        "instant_remedy": "Eat iron-rich foods like spinach and red meat or take an iron supplement.",
        "essential_remedies": [
            "Consume vitamin C to enhance iron absorption",
            "Eat leafy greens, nuts, and legumes",
            "Avoid tea and coffee with meals as they inhibit iron absorption",
            "Take iron supplements as prescribed",
            "Get regular blood tests to monitor levels"
        ],
        "disclaimer": "Seek medical advice if experiencing severe fatigue, dizziness, or heart palpitations."
    },
    "menstrual cramps": {
        "keywords": ["menstrual cramps", "period pain", "PMS", "stomach cramps"],
        "instant_remedy": "Apply a heating pad on the lower abdomen and drink warm ginger tea.",
        "essential_remedies": [
            "Exercise regularly to reduce severity",
            "Increase magnesium intake through nuts and seeds",
            "Stay hydrated to prevent bloating",
            "Avoid caffeine and salty foods",
            "Practice relaxation techniques like yoga"
        ],
        "disclaimer": "Consult a doctor if cramps are severe and interfere with daily life."
    },
    "UTI (urinary tract infection)": {
        "keywords": ["UTI", "burning urination", "frequent urination", "urinary infection"],
        "instant_remedy": "Drink plenty of water and take cranberry juice to help flush bacteria.",
        "essential_remedies": [
            "Urinate frequently to clear bacteria",
            "Avoid holding urine for long periods",
            "Maintain proper hygiene",
            "Wear breathable cotton underwear",
            "Avoid excessive sugar intake"
        ],
        "disclaimer": "Seek medical help if symptoms persist or worsen."
    },
    "sciatica": {
        "keywords": ["sciatica", "nerve pain", "lower back pain", "leg pain"],
        "instant_remedy": "Apply a cold pack for inflammation, followed by a warm compress for relief.",
        "essential_remedies": [
            "Practice stretching exercises",
            "Maintain good posture while sitting",
            "Use ergonomic furniture",
            "Avoid heavy lifting",
            "Try acupuncture or chiropractic therapy"
        ],
        "disclaimer": "Seek medical advice if pain persists or causes numbness."
    },
    "bloating": {
        "keywords": ["bloating", "gas", "stomach fullness", "abdominal swelling"],
        "instant_remedy": "Drink peppermint tea or take a short walk to relieve gas.",
        "essential_remedies": [
            "Eat slowly and chew food properly",
            "Avoid carbonated drinks",
            "Limit salt intake to reduce water retention",
            "Consume probiotic-rich foods",
            "Reduce intake of beans and cruciferous vegetables if sensitive"
        ],
        "disclaimer": "Consult a doctor if bloating is persistent or painful."
    },
    "athlete's foot": {
        "keywords": ["athlete's foot", "foot fungus", "itchy feet", "scaly skin"],
        "instant_remedy": "Apply antifungal cream and keep feet dry.",
        "essential_remedies": [
            "Wear breathable socks and shoes",
            "Change socks regularly",
            "Use foot powder to keep feet dry",
            "Avoid walking barefoot in public places",
            "Soak feet in vinegar or saltwater"
        ],
        "disclaimer": "Seek medical help if the infection spreads or worsens."
    },
    "hiccups": {
        "keywords": ["hiccups", "persistent hiccups", "diaphragm spasm"],
        "instant_remedy": "Hold your breath for 10 seconds or drink a glass of cold water slowly.",
        "essential_remedies": [
            "Eat slowly and avoid gulping air",
            "Try sucking on a lemon or sugar cube",
            "Breathe into a paper bag for a few seconds",
            "Gargle with cold water",
            "Avoid carbonated drinks and excessive alcohol"
        ],
        "disclaimer": "Seek medical attention if hiccups persist for more than 48 hours."
    },
    "nosebleed": {
        "keywords": ["nosebleed", "bleeding nose", "nasal bleeding", "epistaxis"],
        "instant_remedy": "Pinch your nose and lean forward slightly while breathing through your mouth.",
        "essential_remedies": [
            "Keep nasal passages moist with saline spray",
            "Use a humidifier in dry weather",
            "Avoid excessive nose blowing",
            "Apply a cold compress on the nose bridge",
            "Stay hydrated to prevent dryness"
        ],
        "disclaimer": "Seek medical help if the bleeding lasts longer than 20 minutes or is very heavy."
    },
    "swimmer's ear": {
        "keywords": ["swimmer's ear", "ear infection", "water in ear", "ear pain after swimming"],
        "instant_remedy": "Tilt your head to let trapped water drain out and dry the ear with a towel.",
        "essential_remedies": [
            "Use earplugs while swimming",
            "Avoid inserting objects into the ear",
            "Dry ears properly after bathing",
            "Apply vinegar and alcohol ear drops",
            "Keep ears clean but avoid excessive cleaning"
        ],
        "disclaimer": "Seek medical help if pain or discharge occurs."
    },
    "tennis elbow": {
        "keywords": ["tennis elbow", "elbow pain", "joint pain", "forearm pain"],
        "instant_remedy": "Apply ice to reduce inflammation and rest the affected arm.",
        "essential_remedies": [
            "Perform stretching exercises",
            "Use a brace to reduce strain",
            "Avoid repetitive arm motions",
            "Strengthen forearm muscles",
            "Massage with essential oils"
        ],
        "disclaimer": "Consult a doctor if pain persists for weeks."
    },
    "ingrown toenail": {
        "keywords": ["ingrown toenail", "toe pain", "swollen toe", "toe infection"],
        "instant_remedy": "Soak your foot in warm water and gently lift the nail edge with a cotton ball.",
        "essential_remedies": [
            "Wear comfortable, well-fitted shoes",
            "Trim toenails straight across",
            "Keep feet dry and clean",
            "Apply antibiotic ointment",
            "Avoid picking or digging at the toenail"
        ]
    }
}   
    

class SugarLevelTracker:
    def __init__(self):
        self.sugar_levels = []
        self.healthy_range = {
            'fasting_min': 70,
            'fasting_max': 100,
            'post_meal_min': 70,
            'post_meal_max': 140
        }

    def add_sugar_level(self, fasting_sugar, post_meal_sugar):
        self.sugar_levels.append({
            'fasting_sugar': fasting_sugar,
            'post_meal_sugar': post_meal_sugar,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def calculate_averages(self):
        if len(self.sugar_levels) == 0:
            return {
                'fasting_average': 0,
                'post_meal_average': 0,
                'fasting_levels': [],
                'post_meal_levels': [],
                'timestamps': []
            }
        elif len(self.sugar_levels) < 5:
            return {
                'fasting_average': np.mean([day['fasting_sugar'] for day in self.sugar_levels]),
                'post_meal_average': np.mean([day['post_meal_sugar'] for day in self.sugar_levels]),
                'fasting_levels': [day['fasting_sugar'] for day in self.sugar_levels],
                'post_meal_levels': [day['post_meal_sugar'] for day in self.sugar_levels],
                'timestamps': [day['timestamp'].split(' ')[0] for day in self.sugar_levels]
            }

        last_5_days = self.sugar_levels[-5:]
        fasting_averages = [day['fasting_sugar'] for day in last_5_days]
        post_meal_averages = [day['post_meal_sugar'] for day in last_5_days]
        timestamps = [day['timestamp'].split(' ')[0] for day in last_5_days]

        return {
            'fasting_average': np.mean(fasting_averages),
            'post_meal_average': np.mean(post_meal_averages),
            'fasting_levels': fasting_averages,
            'post_meal_levels': post_meal_averages,
            'timestamps': timestamps
        }
    
    def clear_data(self):
        self.sugar_levels = []

def check_blood_pressure(systolic, diastolic):
    """
    Evaluate blood pressure based on standard guidelines
    """
    if systolic < 120 and diastolic < 80:
        return "Normal", "green"
    elif 120 <= systolic <= 129 and diastolic < 80:
        return "Elevated", "yellow"
    elif (130 <= systolic <= 139) or (80 <= diastolic <= 89):
        return "Hypertension Stage 1", "orange"
    elif systolic >= 140 or diastolic >= 90:
        return "Hypertension Stage 2", "red"
    elif systolic > 180 or diastolic > 120:
        return "Hypertensive Crisis", "dark-red"
    
    return "Unable to Classify", "gray"

# Initialize trackers
sugar_tracker = SugarLevelTracker()
bp_readings = []

@app.route('/')
def index(section = None):
    if section:
        return redirect(url_for('static', filename=f'index.html#{section}'))
    return render_template('index.html')
    

@app.route('/health')
def health():
    return render_template('health.html')

@app.route('/about')
def about():
    return render_template('about.html')



# Remedy Assistant Routes
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

#-------------------------------------------text analyzer--------------------------------

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    text = data['text']
    result = analyzer.identify_conditions(text)
    
    return jsonify(result)


#-----------------------------------------------end--------------------------------------

# Sugar Level Routes
@app.route('/add_sugar_level', methods=['POST'])
def add_sugar_level():
    data = request.json
    sugar_tracker.add_sugar_level(
        data['fasting_sugar'], 
        data['post_meal_sugar']
    )
    return jsonify({"status": "success"})

@app.route('/get_averages', methods=['GET'])
def get_averages():
    averages = sugar_tracker.calculate_averages()
    return jsonify(averages)

@app.route('/get_healthy_range', methods=['GET'])
def get_healthy_range():
    return jsonify(sugar_tracker.healthy_range)

@app.route('/clear_sugar_data', methods=['POST'])
def clear_sugar_data():
    sugar_tracker.clear_data()
    return jsonify({"message": "Sugar level data cleared"})

# Blood Pressure Routes
@app.route('/record_bp', methods=['POST'])
def record_bp():
    try:
        # Get data from request
        data = request.json
        systolic = data.get('systolic')
        diastolic = data.get('diastolic')
        
        # Validate input
        if systolic is None or diastolic is None:
            return jsonify({"error": "Invalid input. Both systolic and diastolic values are required."}), 400
        
        if systolic <= 0 or diastolic <= 0 or systolic > 300 or diastolic > 300:
            return jsonify({"error": "Blood pressure values must be between 1 and 300 mmHg"}), 400
        
        # Get current timestamp
        timestamp = datetime.now()
        
        # Check blood pressure category
        category, status = check_blood_pressure(systolic, diastolic)
        
        # Create BP reading entry
        reading = {
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'systolic': systolic,
            'diastolic': diastolic,
            'category': category,
            'status': status
        }
        
        # Add to readings (keep only last 5 days)
        global bp_readings
        bp_readings.append(reading)
        five_days_ago = timestamp - timedelta(days=5)
        bp_readings = [r for r in bp_readings if datetime.strptime(r['timestamp'], '%Y-%m-%d %H:%M:%S') >= five_days_ago]
        
        return jsonify({
            'reading': reading,
            'readings': bp_readings
        })
    
    except ValueError:
        return jsonify({"error": "Invalid input. Please enter numeric values."}), 400
    except Exception as e:
        # Log the error in production
        app.logger.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@app.route('/get_readings', methods=['GET'])
def get_readings():
    return jsonify(bp_readings)

@app.route('/clear_readings', methods=['POST'])
def clear_readings():
    global bp_readings
    bp_readings = []
    return jsonify({"message": "Blood pressure readings cleared"})

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)

    
    