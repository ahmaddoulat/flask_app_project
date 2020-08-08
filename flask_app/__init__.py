from flask import Flask, jsonify, request
from flask import make_response
from flask_pymongo import PyMongo

from storygen.storygen import Story
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/eager_la_db"

mongo = PyMongo(app)

@app.route("/")
def index():
    return "Hello!!!"

@app.route("/<string:student_id>/<string:structure>", methods=['POST'])
def student_story_api(student_id, structure):
    features = json.loads(request.data)
    
    return "Something wrong"

    citizenship_type = "1" if features['citizenship_type'] == "Yes" else "0"
    nation_of_citizenship_desc = "1" if features['nation_of_citizenship_desc'] == "Yes" else "0"
    current_age = "1" if features['current_age'] == "Yes" else "0"
    primary_ethnicity = "1" if features['primary_ethnicity'] == "Yes" else "0"
    student_population_desc = "1" if features['student_population_desc'] == "Yes" else "0"
    student_population = "1" if features['student_population'] == "Yes" else "0"
    admissions_population_desc = "1" if features['admissions_population_desc'] == "Yes" else "0"
    advisor_count = "1" if features['advisor_count'] == "Yes" else "0"
    gpa = "1" if features['gpa'] == "Yes" else "0"
    credits_attempted = "1" if features['credits_attempted'] == "Yes" else "0"
    credits_passed = "1" if features['credits_passed'] == "Yes" else "0"
    academic_standing_desc = "1" if features['academic_standing_desc'] == "Yes" else "0"

    features_list = [
        citizenship_type,
        nation_of_citizenship_desc,
        current_age,
        primary_ethnicity,
        student_population_desc,
        student_population,
        admissions_population_desc,
        advisor_count,
        gpa,
        credits_attempted,
        credits_passed,
        academic_standing_desc
    ]

    selected_features = ''.join(features_list)

    if student_id is None:
        return {'message': 'There is no student ID', 'data': {}}, 404
    if structure is None:
        return {'message': 'There is no structure selected', 'data': {}}, 404

    student = mongo.db.students_data_cleaned.find({{'student_id': int(student_id)}})

    student_story = Story(student, selected_features)

    if structure == "temporal":
        return jsonify(student_story.temporal_story), 201
    elif structure == "default":
        return jsonify(student_story.default_story), 201
    elif structure == "outcome":
        return jsonify(student_story.outcome_story), 201
    elif structure == "test":
        return jsonify(selected_features), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0')
