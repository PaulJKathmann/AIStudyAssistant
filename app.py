#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from asyncio import wait
from flask import Flask, flash, redirect, render_template, request, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)


client = MongoClient("mongodb+srv://mikth:KWJHqejostbRNm8Z@cluster0.xn2i2bv.mongodb.net/")
db = client.get_database("AiAssistant").User_DB

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
    return render_template('pages/coursesLandingPage.html')

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # Get relevant information from the form.
        name = form.name.data
        password = form.password.data

        # Check if the user exists in the database
        existing_user = db.find_one({'name': name})
        if existing_user:
            # Check if the password matches
            if check_password_hash(existing_user['password'], password):
                flash('Logged in successfully.')
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
        existing_user = db.find_one({'name': form.name.data})
        if existing_user is None and request.method == 'POST' and form.validate():
            # Hash the password for security
            hashpass = generate_password_hash(form.password.data, method='pbkdf2:sha512')

            # Insert the new user into the database
            db.insert_one({'name': form.name.data, 'password': hashpass, 'email': form.email.data})

            flash('Registration successful!')
            return redirect(url_for('login'))
        else:
            flash('User already exists. Please login.')
    
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

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
