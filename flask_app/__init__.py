from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pymongo
from storygen import Story
from sshtunnel import SSHTunnelForwarder

app = Flask(__name__)

app.config['SECRET_KEY'] = '1A37BbcCJh67'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/<string:student_id>/<string:structure>", methods=['POST'])
def student_story_api(student_id, structure):
    try:
        citizenship_type = "1" if request.json['citizenship_type'] == "Yes" else "0"
    except:
        citizenship_type = '0'
    try:
        nation_of_citizenship_desc = "1" if request.json['nation_of_citizenship_desc'] == "Yes" else "0"
    except:
        nation_of_citizenship_desc = '0'
    try:
        current_age = "1" if request.json['current_age'] == "Yes" else "0"
    except:
        current_age = '0'
    try:
        primary_ethnicity = "1" if request.json['primary_ethnicity'] == "Yes" else "0"
    except:
        primary_ethnicity = '0'
    try:
        student_population_desc = "1" if request.json['student_population_desc'] == "Yes" else "0"
    except:
        student_population_desc = '0'
    try:
        student_population = "1" if request.json['student_population'] == "Yes" else "0"
    except:
        student_population = '0'
    try:
        admissions_population_desc = "1" if request.json['admissions_population_desc'] == "Yes" else "0"
    except:
        admissions_population_desc = '0'
    try:
        advisor_count = "1" if request.json['advisor_count'] == "Yes" else "0"
    except:
        advisor_count = '0'
    try:
        gpa = "1" if request.json['gpa'] == "Yes" else "0"
    except:
        gpa = '0'
    try:
        credits_attempted = "1" if request.json['credits_attempted'] == "Yes" else "0"
    except:
        credits_attempted = '0'
    try:
        credits_passed = "1" if request.json['credits_passed'] == "Yes" else "0"
    except:
        credits_passed = '0'
    try:
        academic_standing_desc = "1" if request.json['academic_standing_desc'] == "Yes" else "0"
    except:
        academic_standing_desc = '0'

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
    if selected_features is None:
        return {'message': 'There is no features selected', 'data': {}}, 404
    if structure is None:
        return {'message': 'There is no structure selected', 'data': {}}, 404

    MONGO_HOST = "REMOTE_IP_ADDRESS"
    MONGO_DB = "eager_la_db"
    MONGO_USER = "LOGIN"
    MONGO_PASS = "PASSWORD"
    print(student_id)
    print(structure)
    print('Connecting to pymongo database!!')

    server = SSHTunnelForwarder(
        "10.18.207.246",
        ssh_username="adoulat",
        ssh_password="Reset_my_password1986",
        remote_bind_address=('127.0.0.1', 27017)
    )

    server.start()

    client = pymongo.MongoClient('127.0.0.1', server.local_bind_port)  # server.local_bind_port is assigned local port
    db = client[MONGO_DB]
    col = db['students_data_cleaned_with_default_stories'].find({'student_id': student_id})
    student_story = Story(col[0], selected_features)

    if structure == "temporal":
        return jsonify(student_story.temporal_story), 201
    elif structure == "default":
        return jsonify(student_story.default_story), 201
    elif structure == "outcome":
        return jsonify(student_story.outcome_story), 201

from flask_app import routes
