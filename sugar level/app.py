from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import numpy as np
import json

app = Flask(__name__)
CORS(app)

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
            'post_meal_sugar': post_meal_sugar
        })

    def calculate_averages(self):
        if len(self.sugar_levels) == 0:
            return {
                'fasting_average': 0,
                'post_meal_average': 0,
                'fasting_levels': [],
                'post_meal_levels': []
            }
        elif len(self.sugar_levels) < 5:
            return {
                'fasting_average': np.mean([day['fasting_sugar'] for day in self.sugar_levels]),
                'post_meal_average': np.mean([day['post_meal_sugar'] for day in self.sugar_levels]),
                'fasting_levels': [day['fasting_sugar'] for day in self.sugar_levels],
                'post_meal_levels': [day['post_meal_sugar'] for day in self.sugar_levels]
            }


        last_5_days = self.sugar_levels[-5:]
        fasting_averages = [day['fasting_sugar'] for day in last_5_days]
        post_meal_averages = [day['post_meal_sugar'] for day in last_5_days]

        return {
            'fasting_average': np.mean(fasting_averages),
            'post_meal_average': np.mean(post_meal_averages),
            'fasting_levels': fasting_averages,
            'post_meal_levels': post_meal_averages
        }

sugar_tracker = SugarLevelTracker()

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True)
