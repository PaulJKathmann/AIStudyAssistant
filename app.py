#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from asyncio import wait
from flask import Flask, flash, redirect, render_template, request, url_for, session, jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from flask_session import Session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from chatbot.conversation_manager import conversation_manager
from chatbot.prompt_generator import prompt_generator
from chatbot.chatbot import Chatbot
from datetime import timedelta

 # This loads the variables from .env
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config.from_object(__name__)
Session(app)

client = MongoClient("mongodb+srv://kathmann:PRYXSXABxqM0johQ@cluster0.yqfrbpf.mongodb.net/?tls=true&tlsVersion=TLS1.2")
user_db = client.get_database("AiAssistant").User_Collection
course_db = client.get_database("AiAssistant").Course_Collection

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/chatbot')
def chatbot():
    course_code = request.args.get('course_code')
    course = course_db.find_one({'course_code':course_code})
    #topics = course['topics']
    if course:
        topics = course.get('topics', [])
        #return "Course not found", 404
    else:
        topics = ["File I/O in Java", "Java Collections", "Algorithm Analysis", "Stack and Queues in Java", "Binary Trees"]
    return render_template('pages/base.html', topics=topics)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'chatbot' in session:
        chatbot = session['chatbot']
    else:
        chatbot = Chatbot(name="paul", topic="Java Collections")
        session['chatbot'] = chatbot
    text = request.get_json().get("message")
    response, end = chatbot.get_response(text)

    # response = "hello"
    message = {"answer": response, "end": end}
    return jsonify(message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # Get relevant information from the form.
        name = form.name.data
        password = form.password.data

        # Check if the user exists in the database
        existing_user = user_db.find_one({'name': name})
        if existing_user:
            # Check if the password matches
            if check_password_hash(existing_user['password'], password):
                flash('Logged in successfully.')
                chatbot = Chatbot(existing_user['name'])
                session['chatbot'] = chatbot
                return redirect(url_for('home'))
            else:
                flash('Incorrect password.')
        else:
            flash('User does not exist.')
    return render_template('forms/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
     # Check if the user already exists
    if request.method == 'POST' and form.validate():
        # Check if the user already exists
        existing_user = user_db.find_one({'name': form.name.data})
        if existing_user is None and form.validate():
            # Hash the password for security
            hashpass = generate_password_hash(form.password.data, method='pbkdf2:sha512')

            # Insert the new user into the database
            user_db.insert_one({'name': form.name.data, 'password': hashpass, 'email': form.email.data})

            flash('Registration successful!')
            return redirect(url_for('login'))
        else:
            flash('User already exists. Please login.')
    
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@app.route('/logout')
def logout():
    return redirect(url_for('home'))

@app.route('/fetch_prompt', methods=['POST'])
def update_prompt():
    data = request.json
    topic_name = data['topicName']
    topic_description = data['topicDescription']
    course_code = data['course_code']
    print(f"topic_name {topic_name}, topic_description {topic_description}")

    # error handling in case the prompt name is invalid
    if not topic_name:
        print('Invalid prompt name')
        return jsonify({'message': 'Invalid prompt name'}), 400

    # Fetch the course from the database
    course = course_db.find_one({'course_code': course_code})
    if not course:
        print(f"Course not found: {course_code}")
        return jsonify({'message': f"Course not found {course_code}"}), 404
    
    # get the course topic
    for t in course['topics']:
        if t['topic_name'] == topic_name:
            topic = t
            break
        else:
            None
    if not topic:
        print(f"Topic not found: {topic_name}")
        return jsonify({'message': 'Topic not found'}), 404
    
    print(f"Topic found: {topic}")
    print("Updating prompt...\n\n")
    # setup a new chatbot instance since the prompt has changed
    chatbot = Chatbot(name="paul", topic=topic)
    session['chatbot'] = chatbot
    if chatbot and session['chatbot']:
        print(f"Chatbot prompt updated successfully: chatbot {chatbot}; session {session['chatbot']}")
    if topic:
        #full_prompt = prompt.get('full_prompt')
        chatbot.prompt = prompt_generator(chatbot.user).generate_prompt(topic)
        # Empty messages and conversation_cache
        chatbot.cm.clear_cm()
        # reinstantiate the conversation manager with new prompt
        chatbot.cm = conversation_manager(prompt=chatbot.prompt)
        session['chatbot'] = chatbot  # Reassign the modified chatbot to the session
        session.modified = True 
        print(f"Chatbot prompt updated successfully: {chatbot.prompt}")
        return jsonify({'message': 'Prompt updated successfully'}), 200
    else:
        return jsonify({'message': 'Prompt not found'}), 404


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
