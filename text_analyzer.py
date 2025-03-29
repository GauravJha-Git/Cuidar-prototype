# text_analyzer.py
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download necessary NLTK data (uncomment first time)
# nltk.download('punkt')
# nltk.download('stopwords')

class MedicalTextAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        
        # Common symptoms by system
        self.symptom_keywords = {
            "headache": ["headache", "migraine", "head pain", "tension headache", "pressure in head"],
            "common cold": ["runny nose", "stuffy nose", "sneezing", "sore throat", "congestion", "cough"],
            "fever": ["fever", "high temperature", "chills", "sweating", "hot", "feverish"],
            "upset stomach": ["nausea", "vomiting", "diarrhea", "stomach pain", "indigestion", "stomach ache"],
            "acne": ["pimples", "breakouts", "skin blemishes", "blackheads", "whiteheads"],
            "allergic reaction": ["itchy skin", "rash", "hives", "swelling", "redness", "watery eyes"],
            "constipation": ["difficulty passing stool", "hard stool", "infrequent bowel movements", "bloating", "straining"],
            "eye strain": ["tired eyes", "burning eyes", "blurry vision", "dry eyes", "eye discomfort"],
            "dry skin": ["flaky skin", "rough patches", "itchy skin", "cracked skin", "scaling"],
            "motion sickness": ["nausea while traveling", "dizziness", "vomiting", "cold sweats", "lightheadedness"],
            "dandruff": ["itchy scalp", "flaky scalp", "dry scalp", "scalp irritation", "white flakes"],
            "sore muscles": ["muscle pain", "muscle stiffness", "body ache", "muscle cramps", "soreness"],
            "toothache": ["tooth pain", "cavity", "gum pain", "sensitive teeth", "jaw pain"],
            "sunburn": ["red skin", "burnt skin", "peeling skin", "painful skin", "blistering"],
            "sleeplessness": ["difficulty sleeping", "restlessness", "insomnia", "waking up frequently", "tossing and turning"],
            "ear pain": ["earache", "blocked ear", "ear infection", "ringing in ear", "sharp ear pain"],
            "snoring": ["noisy breathing", "sleep disturbance", "dry mouth", "sore throat in morning", "gasping for air"],
            "anemia": ["fatigue", "pale skin", "shortness of breath", "dizziness", "weakness"],
            "dehydration": ["dry mouth", "dark urine", "dizziness", "fatigue", "increased thirst"],
            "stress": ["anxiety", "nervousness", "irritability", "difficulty concentrating", "head tension"],
            "back pain": ["pain in back", "strain in back", "muscle stretch of back", "pain back"]

        }
    
    def preprocess_text(self, text):
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        
        # Tokenize
        word_tokens = word_tokenize(text)
        
        # Remove stopwords
        filtered_words = [word for word in word_tokens if word not in self.stop_words]
        
        return filtered_words
    
    def identify_conditions(self, text):
        """
        Analyzes text to identify potential medical conditions.
        Returns a list of potential conditions found.
        """
        words = self.preprocess_text(text)
        text_lower = text.lower()
        
        found_conditions = []
        
        # Check for symptom keywords in the original text
        for condition, keywords in self.symptom_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if condition not in found_conditions:
                        found_conditions.append(condition)
        
        # Look for phrases that indicate time
        time_patterns = [
            r'for (\d+) (day|days|week|weeks|month|months)',
            r'since (yesterday|last week|last month)',
            r'started (\d+) (day|days|week|weeks|month|months) ago'
        ]
        
        duration_matches = []
        for pattern in time_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                duration_matches.extend(matches)
        
        return {
            "conditions": found_conditions,
            "duration": duration_matches,
            "original_words": words
        }

# Example usage:
# analyzer = MedicalTextAnalyzer()
# analysis = analyzer.identify_conditions("I've had a terrible headache for 3 days and feeling nauseous")
# print(analysis)