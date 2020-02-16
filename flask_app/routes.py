from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import sha256_crypt
import pymongo
from storygen.storygen import Story
from sshtunnel import SSHTunnelForwarder

from flask_app import app, db
from flask_app.models import User, Post
from flask_app.forms import PostForm

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

@app.route("/")
def index():
    db.create_all()
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@app.route("/about")
def about():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('register.html')

    else:
        # Create user object to insert into SQL
        passwd1 = request.form.get('password1')
        passwd2 = request.form.get('password2')

        if passwd1 != passwd2 or passwd1 == None:
            flash('Password Error!', 'danger')
            return render_template('register.html')

        hashed_pass = sha256_crypt.encrypt(str(passwd1))

        new_user = User(
            username=request.form.get('username'),
            email=request.form.get('username'),
            password=hashed_pass)

        if user_exsists(new_user.username, new_user.email):
            flash('User already exsists!', 'danger')
            return render_template('register.html')
        else:
            # Insert new user into SQL
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            flash('Account created!', 'success')
            return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    else:
        username = request.form.get('username')
        password_candidate = request.form.get('password')

        # Query for a user with the provided username
        result = User.query.filter_by(username=username).first()

        # If a user exsists and passwords match - login
        if result is not None and sha256_crypt.verify(password_candidate, result.password):

            # Init session vars
            login_user(result)
            flash('Logged in!', 'success')
            return redirect(url_for('index'))

        else:
            flash('Incorrect Login!', 'danger')
            return render_template('login.html')


@app.route("/logout")
def logout():
    logout_user()
    flash('Logged out!', 'success')
    return redirect(url_for('index'))


# Check if username or email are already taken
def user_exsists(username, email):
    # Get all Users in SQL
    users = User.query.all()
    for user in users:
        if username == user.username or email == user.email:
            return True

    # No matching user
    return False

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))
